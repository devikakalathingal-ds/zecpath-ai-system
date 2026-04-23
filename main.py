import os
import json
from datetime import datetime
import numpy as np

from fastapi import FastAPI

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------
# PARSERS (your existing structure)
# -------------------------
from parsers.resume_reader import read_resume
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text
from parsers.section_classifier import classify_sections

from education_parser.education_extractor import extract_education
from education_parser.certification_extractor import extract_certifications
from experience_parser import extract_experience

from skill_engine.skill_extractor import SkillExtractor
from utils.entity_extractor import extract_entities
from utils.ats_scorer import calculate_ats_score
from utils.academic_profile_builder import build_academic_profile


# -------------------------
# FASTAPI APP
# -------------------------
app = FastAPI()

RESUME_FOLDER = "resumes"
JD_FOLDER = "Job Description"


# -------------------------
# MODEL
# -------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    return model.encode(text)


def cosine_score(a, b):
    return cosine_similarity([a], [b])[0][0]


# -------------------------
# SAFE JSON
# -------------------------
def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(i) for i in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    return obj


# -------------------------
# LOAD JD
# -------------------------
def load_single_jd(file_name):
    path = os.path.join(JD_FOLDER, file_name)

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return {"name": file_name, "text": f.read()}


# -------------------------
# PIPELINE
# -------------------------
def process_resume(file_name):

    file_path = os.path.join(RESUME_FOLDER, file_name)

    if not os.path.exists(file_path):
        return {"error": "Resume not found"}

    # RAW TEXT
    raw_text = read_resume(file_path)

    # CLEANING
    cleaned_text = clean_text(raw_text)
    normalized_text = normalize_text(cleaned_text)

    # SECTION CLASSIFICATION
    sections = classify_sections(normalized_text)

    # -------------------------
    # SKILLS (FIXED HERE)
    # -------------------------
    skill_extractor = SkillExtractor()
    skills = skill_extractor.extract_skills(normalized_text)

    # -------------------------
    # EDUCATION
    # -------------------------
    education = extract_education(raw_text)

    # -------------------------
    # CERTIFICATIONS
    # -------------------------
    certifications = extract_certifications(raw_text)

    # -------------------------
    # EXPERIENCE (FIXED MODULE)
    # -------------------------
    experience = extract_experience(raw_text)

    # -------------------------
    # ENTITIES
    # -------------------------
    entities = extract_entities(raw_text)

    academic_profile = build_academic_profile(education, certifications)

    # -------------------------
    # ATS SCORE
    # -------------------------
    jd_keywords = "Drug safety pharmacovigilance clinical data analysis Python SQL"

    ats_score, matched_skills, missing_skills = calculate_ats_score(
        skills,
        jd_keywords
    )

    # -------------------------
    # JOB DESCRIPTION
    # -------------------------
    jd = load_single_jd("Drug Safety Scientist.txt")

    if jd is None:
        return {"error": "Job Description not found"}

    resume_emb = get_embedding(normalized_text)
    jd_emb = get_embedding(jd["text"])

    embedding_score = cosine_score(resume_emb, jd_emb) * 100

    # -------------------------
    # FINAL SCORE
    # -------------------------
    final_score = (ats_score * 0.45) + (embedding_score * 0.55)

    decision = "Selected" if final_score >= 55 else "Rejected"

    result = {
        "resume_file": file_name,
        "job_description": jd["name"],

        "skills": skills,
        "education": education,
        "certifications": certifications,
        "experience": experience,
        "entities": entities,
        "academic_profile": academic_profile,

        "ats_score": float(ats_score),
        "embedding_score": float(embedding_score),
        "final_score": float(final_score),
        "decision": decision
    }

    return make_json_safe(result)


# -------------------------
# API ENDPOINT
# -------------------------
@app.get("/analyze/{filename}")
def analyze_resume(filename: str):
    return process_resume(filename)


# -------------------------
# RUN MODE
# -------------------------
if __name__ == "__main__":

    file_name = "resume6.txt"

    print(f"{datetime.now()} - ZecpathAI Started 🚀")

    result = process_resume(file_name)

    print("\n📄 Resume:", result["resume_file"])
    print("📄 Job:", result["job_description"])

    print("\n🧠 Skills:", json.dumps(result["skills"], indent=2))
    print("\n🎓 Education:", json.dumps(result["education"], indent=2))
    print("\n💼 Experience:", json.dumps(result["experience"], indent=2))
    print("\n🏷 Entities:", json.dumps(result["entities"], indent=2))

    print("\n⭐ ATS Score:", result["ats_score"])
    print("📊 Embedding Score:", result["embedding_score"])
    print("🏁 Final Score:", result["final_score"])
    print("🎯 Decision:", result["decision"])

    os.makedirs("output", exist_ok=True)

    with open("output/resume_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("\n📁 Saved: output/resume_output.json")