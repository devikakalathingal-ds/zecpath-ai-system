from fastapi import FastAPI
import os

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
        # Read
        text = read_resume(file_path)

        # Clean
        cleaned_text = clean_text(text)
        normalized_text = normalize_text(cleaned_text)

        # Sections
        sections = classify_sections(normalized_text)

        # Education
        education = extract_education(normalized_text)

        # Certifications
        certifications = extract_certifications(normalized_text)

        # Skills
        skill_extractor = SkillExtractor()
        skills = skill_extractor.extract_skills(normalized_text)

        # Experience
        experience = extract_experience(normalized_text)

        # ATS (FIXED)
        job_desc = "Python developer AWS backend data analytics"

        ats_score, matched_skills, missing_skills = calculate_ats_score(
            skills,
            job_desc
        )

        # Relevance
        relevance = check_education_relevance(education, "Data Scientist")

        # Entities
        entities = extract_entities(normalized_text)

        return {
            "sections": sections,
            "education": education,
            "certifications": certifications,
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
# TERMINAL DEBUG MODE
# =========================
if __name__ == "__main__":
    result = process_resume("resume1.txt")

    print("\n===== RESUME ANALYSIS =====\n")

    print("📚 EDUCATION:")
    for edu in result.get("education", []):
        print("-", edu.get("degree"), "-", edu.get("graduation_year"))

    print("\n🧠 SKILLS:")
    skills = result.get("skills", {})
    for category, items in skills.items():
        for item in items:
            print("-", item["skill"], "(confidence:", item["confidence"], ")")

    print("\n💼 EXPERIENCE:")
    print(result.get("experience", []))

    print("\n📊 ATS SCORE:")
    print(result.get("ats_score"))

    print("\n🏷 MATCHED:")
    print(result.get("matched_skills"))

    print("\n❌ MISSING:")
    print(result.get("missing_skills"))

    print("\n============================\n")