import os
import json
from datetime import datetime
import numpy as np

from fastapi import FastAPI, UploadFile, File
import shutil
import uuid

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# PARSERS
# =========================
from parsers.resume_reader import read_resume
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text
from parsers.section_classifier import classify_sections

from education_parser.education_extractor import extract_education
from education_parser.certification_extractor import extract_certifications
from experience_parser import extract_experience

from skill_engine.skill_extractor import SkillExtractor
from utils.entity_extractor import extract_entities
from utils.academic_profile_builder import build_academic_profile

# =========================
# ATS ENGINE
# =========================
from ats_engine.scorer import calculate_final_score

# =========================
# FASTAPI APP
# =========================
app = FastAPI()

RESUME_FOLDER = "resumes"

# =========================
# MODEL
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    return model.encode(text)


def cosine_score(a, b):
    return cosine_similarity([a], [b])[0][0]


# =========================
# SAFE JSON HANDLER
# =========================
def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(i) for i in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    return obj


# =========================
# MAIN PIPELINE
# =========================
def process_resume(file_path, jd_text=None):

    if not os.path.exists(file_path):
        return {"error": "Resume not found"}

    # -------------------------
    # STEP 1: READ + CLEAN
    # -------------------------
    raw_text = read_resume(file_path)
    cleaned_text = clean_text(raw_text)
    normalized_text = normalize_text(cleaned_text)

    classify_sections(normalized_text)

    # -------------------------
    # STEP 2: SKILLS
    # -------------------------
    skill_extractor = SkillExtractor()
    skills_raw = skill_extractor.extract_skills(normalized_text)

    skills = []

    if isinstance(skills_raw, dict):
        for key in ["technical", "business", "creative", "soft_skills"]:
            for item in skills_raw.get(key, []):
                if isinstance(item, dict):
                    skills.append(item.get("skill"))
                else:
                    skills.append(item)

    elif isinstance(skills_raw, list):
        for item in skills_raw:
            if isinstance(item, dict):
                skills.append(item.get("skill"))
            else:
                skills.append(item)

    skills = [s for s in skills if s]

    # -------------------------
    # STEP 3: EDUCATION
    # -------------------------
    education = extract_education(raw_text)

    # -------------------------
    # STEP 4: CERTIFICATIONS
    # -------------------------
    certifications = extract_certifications(raw_text)

    # -------------------------
    # STEP 5: EXPERIENCE
    # -------------------------
    experience = extract_experience(raw_text)

    # -------------------------
    # STEP 6: ENTITIES
    # -------------------------
    entities = extract_entities(raw_text)

    academic_profile = build_academic_profile(education, certifications)

    # -------------------------
    # STEP 7: JOB DESCRIPTION
    # -------------------------
    if jd_text is None:
        return {"error": "Job description is required"}

    # -------------------------
    # STEP 8: SEMANTIC SCORE
    # -------------------------
    resume_emb = get_embedding(normalized_text)
    jd_emb = get_embedding(jd_text)

    embedding_score = cosine_score(resume_emb, jd_emb)

    # -------------------------
    # STEP 9: ATS SCORING
    # -------------------------
    final_score, breakdown = calculate_final_score(
        skills=skills,
        experience=experience,
        education=education,
        embedding_score=embedding_score,
        jd_text=jd_text,
        role="software_engineer"
    )

    decision = "Selected" if final_score >= 55 else "Rejected"

    # -------------------------
    # FINAL OUTPUT
    # -------------------------
    result = {
        "resume_file": os.path.basename(file_path),
        "skills": skills,
        "education": education,
        "certifications": certifications,
        "experience": experience,
        "entities": entities,
        "academic_profile": academic_profile,
        "ats_breakdown": breakdown,
        "embedding_score": float(embedding_score * 100),
        "final_score": final_score,
        "decision": decision
    }

    return make_json_safe(result)


# =========================
# API 1: UPLOAD RESUME
# =========================
@app.post("/upload")
def upload_resume(file: UploadFile = File(...)):
    try:
        os.makedirs(RESUME_FOLDER, exist_ok=True)

        file_id = str(uuid.uuid4())

        # ✅ KEEP ORIGINAL EXTENSION
        file_ext = file.filename.split(".")[-1]
        file_path = os.path.join(RESUME_FOLDER, f"{file_id}.{file_ext}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "file_path": file_path
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# =========================
# API 2: ANALYZE RESUME
# =========================
@app.post("/analyze")
def analyze_resume(file_path: str, job_description: str):
    try:
        result = process_resume(file_path, job_description)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# RUN MODE (OPTIONAL)
# =========================
if __name__ == "__main__":

    print(f"{datetime.now()} - ATS API Started 🚀")

    test_file = os.path.join(RESUME_FOLDER, "resume6.txt")

    if os.path.exists(test_file):
        result = process_resume(test_file, "Looking for Python developer")

        print("\n⭐ Final Score:", result["final_score"])
        print("🎯 Decision:", result["decision"])

        os.makedirs("output", exist_ok=True)

        with open("output/resume_output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print("\n📁 Saved: output/resume_output.json")