from parsers.resume_reader import read_resume
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text

from skill_engine.skill_extractor import SkillExtractor
from utils.ats_scorer import calculate_ats_score
from utils.entity_extractor import extract_entities


# =========================
# FILES
# =========================

RESUME_FILE = "resumes/sample_resume.pdf"

JD_FILE = "Job Description/Drug Safety Auditor.txt"   # 👈 CHANGE THIS FILE NAME


# =========================
# LOAD RESUME
# =========================

print("\n===== LOADING RESUME =====\n")

raw_text = read_resume(RESUME_FILE)
cleaned_text = clean_text(raw_text)
normalized_text = normalize_text(cleaned_text)


# =========================
# SKILL EXTRACTION
# =========================

skill_extractor = SkillExtractor()
skills = skill_extractor.extract_skills(normalized_text)

print("\n===== EXTRACTED SKILLS =====")
print(skills)


# =========================
# ENTITY EXTRACTION
# =========================

entities = extract_entities(normalized_text)

print("\n===== ENTITIES =====")
print(entities)


# =========================
# LOAD JOB DESCRIPTION (ONLY ONE FILE)
# =========================

with open(JD_FILE, "r", encoding="utf-8") as f:
    jd_text = f.read()


# =========================
# ATS SCORE
# =========================

ats_score, matched, missing = calculate_ats_score(skills, jd_text)

print("\n==============================")
print("🔥 ATS RESULT FOR SINGLE JD")
print("==============================")

print("Job File:", JD_FILE)
print("ATS Score:", ats_score)
print("Matched Skills:", matched)
print("Missing Skills:", missing)

print("\n✅ Done!\n")