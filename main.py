import os
import shutil
import uuid
import gc
import time
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

from ats_engine.scorer import calculate_final_score
from scoring.fairness import calculate_fairness_score


# =========================
# APP
# =========================
app = FastAPI()

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# PERFORMANCE OPTIMIZATION (NEW)
# =========================
text_cache = {}

def get_cached_text(file_path):
    if file_path in text_cache:
        return text_cache[file_path]

    text = read_resume(file_path)
    text_cache[file_path] = text
    return text


def time_logger(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⚡ {func.__name__} took {end - start:.2f}s")
        return result
    return wrapper


# =========================
# MODEL
# =========================
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded")
except:
    model = None


def get_embedding(text):
    if model:
        return model.encode(text)
    return np.zeros(384)


def cosine_score(a, b):
    return cosine_similarity([a], [b])[0][0]


# =========================
# SAFE JSON
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
# MAIN PIPELINE (OPTIMIZED)
# =========================
@time_logger
def process_resume(file_path, job_description):

    if not os.path.exists(file_path):
        return {"error": "Resume not found"}

    # STEP 1: READ + CLEAN (CACHE OPTIMIZED)
    raw_text = get_cached_text(file_path)
    cleaned_text = clean_text(raw_text)
    normalized_text = normalize_text(cleaned_text)

    classify_sections(normalized_text)

    # STEP 2: SKILLS (OPTIMIZED DEDUPLICATION)
    skill_extractor = SkillExtractor()
    skills_raw = skill_extractor.extract_skills(normalized_text)

    skills = []

    if isinstance(skills_raw, dict):
        for key in ["technical", "business", "creative", "soft_skills"]:
            for item in skills_raw.get(key, []):
                skills.append(item.get("skill") if isinstance(item, dict) else item)

    elif isinstance(skills_raw, list):
        for item in skills_raw:
            skills.append(item.get("skill") if isinstance(item, dict) else item)

    skills = list(set([s for s in skills if s]))  # FAST CLEAN

    # STEP 3: OTHER EXTRACTIONS
    education = extract_education(raw_text)
    certifications = extract_certifications(raw_text)
    experience = extract_experience(raw_text)
    entities = extract_entities(raw_text)
    academic_profile = build_academic_profile(education, certifications)

    # STEP 4: EMBEDDINGS
    resume_emb = get_embedding(normalized_text)
    jd_emb = get_embedding(job_description)

    embedding_score = cosine_score(resume_emb, jd_emb)

    # STEP 5: SCORING
    final_score, breakdown = calculate_final_score(
        skills=skills,
        experience=experience,
        education=education,
        embedding_score=embedding_score,
        jd_text=job_description,
        role="general"
    )

    decision = "Selected" if final_score >= 55 else "Rejected"

    # STEP 6: FAIRNESS
    fairness_score, matched_skills, bias_flags = calculate_fairness_score(
        resume_text=normalized_text,
        jd_text=job_description
    )

    # MEMORY CLEANUP (IMPORTANT)
    gc.collect()

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
# RUN
# =========================
if __name__ == "__main__":
    print(f"{datetime.now()} - ATS API Started 🚀")