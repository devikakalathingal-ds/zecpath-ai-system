from fastapi import FastAPI
import os
import json
from datetime import datetime

from parsers.resume_reader import read_resume
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text
from parsers.section_classifier import classify_sections

from education_parser.education_extractor import extract_education
from education_parser.certification_extractor import extract_certifications
from education_parser.relevance_logic import check_education_relevance

from skill_engine.skill_extractor import SkillExtractor

from utils.entity_extractor import extract_entities
from utils.ats_scorer import calculate_ats_score
from utils.academic_profile_builder import build_academic_profile

from experience_parser import extract_experience


app = FastAPI()

RESUME_FOLDER = "resumes"


@app.get("/")
def home():
    return {"message": "Backend running successfully 🚀"}


def process_resume(file_name: str):

    file_path = os.path.join(RESUME_FOLDER, file_name)

    print("Looking for:", file_path)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    try:
        # READ
        text = read_resume(file_path)

        # CLEAN
        cleaned_text = clean_text(text)
        normalized_text = normalize_text(cleaned_text)

        # SECTIONS
        sections = classify_sections(normalized_text)

        # EXTRACTION
        education = extract_education(normalized_text)
        certifications = extract_certifications(normalized_text)

        # ACADEMIC PROFILE
        academic_profile = build_academic_profile(education, certifications)

        # SKILLS
        skill_extractor = SkillExtractor()
        skills = skill_extractor.extract_skills(normalized_text)

        # EXPERIENCE
        experience = extract_experience(normalized_text)

        # ATS SCORE
        job_desc = "Python developer AWS backend data analytics"

        ats_score, matched_skills, missing_skills = calculate_ats_score(
            skills,
            job_desc
        )

        # RELEVANCE (CLEAN)
        relevance = check_education_relevance(education, "Data Scientist")

        if isinstance(relevance, list):
            relevance = sum(item.get("relevance_score", 0) for item in relevance)

        # ENTITIES
        entities = extract_entities(normalized_text)

        return {
            "sections": sections,
            "education": education,
            "certifications": certifications,
            "academic_profile": academic_profile,
            "skills": skills,
            "experience": experience,
            "ats_score": ats_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "relevance": relevance,
            "entities": entities
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/analyze/{filename}")
def analyze_resume(filename: str):
    return process_resume(filename)


# =========================
# TERMINAL MODE (FINAL)
# =========================
if __name__ == "__main__":

    file_name = "resume1.txt"

    print(f"{datetime.now()} - ZecpathAI - INFO - Logging System Initialized.")
    print(f"Enter resume file path: resumes/{file_name}")
    print("Extracting resume...")

    print(f"{datetime.now()} - ZecpathAI - INFO - Starting extraction for: resumes/{file_name}")

    result = process_resume(file_name)

    if "error" in result:
        print("❌ Error:", result["error"])
        exit()

    print(f"{datetime.now()} - ZecpathAI - INFO - Successfully extracted resume.")

    # CLEAN SECTIONS
    sections = result.get("sections", {})
    if isinstance(sections, dict):
        clean_sections = [k.lower() for k, v in sections.items() if v.strip()]
    else:
        clean_sections = sections

    print("📑 Sections detected:", clean_sections)
    print("📊 Structured Resume Created\n")

    print("✅ Extraction Completed!")

    # -------------------------
    # SAVE RESUME OUTPUT
    # -------------------------
    os.makedirs("output", exist_ok=True)

    with open("output/resume_output.json", "w") as f:
        json.dump(result, f, indent=4)

    print("📄 Saved to: output/resume_output.json")

    # SKILLS
    skills_data = result.get("skills", {})
    found_skills = []

    for category, items in skills_data.items():
        for item in items:
            found_skills.append(item["skill"])

    print("🧠 Found Skills:", found_skills)

    # ATS SCORE
    ats_score = result.get("ats_score", 0)
    print(f"⭐ ATS Score: {ats_score}/100\n")

    # -------------------------
    # SCREENING RESULT (SAVE)
    # -------------------------
    print("🤖 AI Screening Result")

    screening_result = {
        "matched_skills": result.get("matched_skills"),
        "score": ats_score,
        "percentage": float(ats_score),
        "decision": "Selected" if ats_score >= 70 else "Rejected"
    }

    print(screening_result)

    os.makedirs("reports", exist_ok=True)

    with open("reports/screening_result.json", "w") as f:
        json.dump(screening_result, f, indent=4)

    print("📊 Screening report saved: reports/screening_result.json")

    # -------------------------
    # ACADEMIC PROFILE
    # -------------------------
    print("\n🎓 Structured Academic Profile:")
    print(json.dumps(result.get("academic_profile"), indent=4))

    # -------------------------
    # RELEVANCE
    # -------------------------
    print("\n⭐ Education Relevance Score:", result.get("relevance"))

    # -------------------------
    # EXPERIENCE
    # -------------------------
    print("\n💼 Experience Details:")
    print(result.get("experience"))

    print("\n⭐ Total Experience: 0 years")

    print("\n============================\n")