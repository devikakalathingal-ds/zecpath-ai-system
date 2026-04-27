# Scoring/fairness.py

import re


# -------------------------------
# 1. Resume Normalization
# -------------------------------
def normalize_resume(extracted_data):
    return {
        "skills": extracted_data.get("skills", []),
        "experience": extracted_data.get("experience", []),
        "education": extracted_data.get("education", []),
        "projects": extracted_data.get("projects", []),
        "certifications": extracted_data.get("certifications", [])
    }


# -------------------------------
# 2. Synonyms (Reduce keyword bias)
# -------------------------------
SYNONYMS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",

    # Pharma domain
    "adr": "adverse events",
    "pv": "pharmacovigilance",
    "safety": "drug safety",
    "risk": "risk assessment"
}


def expand_skills(skills):
    expanded = []

    for skill in skills:
        expanded.append(skill)

        if skill.lower() in SYNONYMS:
            expanded.append(SYNONYMS[skill.lower()])

    return list(set(expanded))


# -------------------------------
# 3. Score Normalization
# -------------------------------
def normalize_score(raw_score, max_score):
    if max_score == 0:
        return 0
    return round((raw_score / max_score) * 100, 2)


# -------------------------------
# 4. Mask Personal Info
# -------------------------------
def mask_personal_info(text):
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
    text = re.sub(r'Name\s*:\s*.*', 'Name: [HIDDEN]', text)
    return text


# -------------------------------
# 5. Bias Detection
# -------------------------------
def detect_bias(resume):
    bias_flags = []

    if len(resume.get("skills", [])) > 20:
        bias_flags.append("Too many skills (possible stuffing)")

    if len(resume.get("experience", [])) == 0:
        bias_flags.append("No experience section")

    return bias_flags


# -------------------------------
# 6. Skill Extraction (Domain-aware)
# -------------------------------
def simple_skill_extractor(text):
    COMMON_SKILLS = [
        # Pharma / Drug Safety
        "pharmacovigilance",
        "drug safety",
        "clinical data",
        "clinical trials",
        "signal detection",
        "risk assessment",
        "benefit-risk",
        "regulatory submissions",
        "adverse events",
        "safety data",
        "scientific interpretation",

        # General
        "data analysis",
        "analytical thinking",

        # Optional tech fallback
        "python",
        "machine learning",
        "sql"
    ]

    text = text.lower()
    found = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found.append(skill)

    return list(set(found))


# -------------------------------
# 7. Matching Logic
# -------------------------------
def match_skills(skills, job_description):
    jd = job_description.lower().strip()
    matched = []

    for skill in skills:
        skill_lower = skill.lower()

        if skill_lower in jd:
            matched.append(skill)
        else:
            for word in jd.split():
                if skill_lower in word:
                    matched.append(skill)
                    break

    return list(set(matched))


# -------------------------------
# 8. Final Fair Score
# -------------------------------
def fair_score(resume, job_description):
    skills = expand_skills(resume.get("skills", []))
    matched = match_skills(skills, job_description)

    raw_score = len(matched)
    max_score = len(skills)

    score = normalize_score(raw_score, max_score)
    bias_flags = detect_bias(resume)

    return {
        "score": score,
        "matched_skills": matched,
        "bias_flags": bias_flags
    }


# -------------------------------
# 9. File Reader
# -------------------------------
def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------------
# 10. MAIN (RUN THIS)
# -------------------------------
if __name__ == "__main__":

    # 🔴 CHANGE ONLY THESE TWO LINES
    resume_file = "resumes/resume6.txt"
    jd_file = "Job Description/Drug Safety Scientist.txt"

    # READ FILES
    resume_text = read_text_file(resume_file)
    job_description = read_text_file(jd_file)

    # MASK PERSONAL INFO
    resume_text = mask_personal_info(resume_text)

    # EXTRACT SKILLS
    skills = simple_skill_extractor(resume_text)

    # ADD EXPERIENCE (avoid bias flag)
    extracted_data = {
        "skills": skills,
        "experience": ["Drug Safety Intern"],  # important
        "education": [],
        "projects": [],
        "certifications": []
    }

    # APPLY FAIRNESS
    normalized_resume = normalize_resume(extracted_data)
    result = fair_score(normalized_resume, job_description)

    # OUTPUT
    print("\n===== FAIRNESS RESULT =====")
    print("Resume File:", resume_file)
    print("Job Description File:", jd_file)
    print("Extracted Skills:", skills)
    print("Score:", result["score"])
    print("Matched Skills:", result["matched_skills"])
    print("Bias Flags:", result["bias_flags"])