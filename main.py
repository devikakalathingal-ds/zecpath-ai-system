import os
import json
import shutil
import uuid
from datetime import datetime
import numpy as np

from fastapi import FastAPI, UploadFile, File, Query
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
# FAIRNESS
# =========================
from scoring.fairness import calculate_fairness_score


# =========================
# FASTAPI APP
# =========================
app = FastAPI()

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# MODEL (SAFE LOADING)
# =========================
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded successfully")
except Exception as e:
    print("⚠️ Model loading failed:", e)
    model = None


def get_embedding(text):
    if model:
        return model.encode(text)
    return np.zeros(384)  # fallback vector


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
def process_resume(file_path, job_description):

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
    # STEP 7: SEMANTIC SCORE
    # -------------------------
    resume_emb = get_embedding(normalized_text)
    jd_emb = get_embedding(job_description)

    embedding_score = cosine_score(resume_emb, jd_emb)

    # -------------------------
    # STEP 8: ATS SCORE
    # -------------------------
    final_score, breakdown = calculate_final_score(
        skills=skills,
        experience=experience,
        education=education,
        embedding_score=embedding_score,
        jd_text=job_description,
        role="general"
    )

    decision = "Selected" if final_score >= 55 else "Rejected"

    # -------------------------
    # STEP 9: FAIRNESS
    # -------------------------
    fairness_score, matched_skills, bias_flags = calculate_fairness_score(
        resume_text=normalized_text,
        jd_text=job_description
    )

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
        "decision": decision,

        "fairness_score": fairness_score,
        "matched_skills": matched_skills,
        "bias_flags": bias_flags
    }

    return make_json_safe(result)


# =========================
# UPLOAD API
# =========================
@app.post("/upload")
def upload_resume(file: UploadFile = File(...)):

    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "file_path": file_path
    }


# =========================
# ANALYZE API
# =========================
@app.post("/analyze")
def analyze_resume(
    file_path: str = Query(...),
    job_description: str = Query(...)
):
    result = process_resume(file_path, job_description)

    return {
        "status": "success",
        "data": result
    }


# =========================
# RUN MODE
# =========================
if __name__ == "__main__":
    print(f"{datetime.now()} - ATS API Started 🚀")