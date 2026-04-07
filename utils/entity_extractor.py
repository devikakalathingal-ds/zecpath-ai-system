import re

def extract_entities(text):
    data = {}

    # Email
    email = re.findall(r'\S+@\S+', text)
    data["email"] = email[0] if email else None

    # Phone
    phone = re.findall(r'\b\d{10}\b', text)
    data["phone"] = phone[0] if phone else None

    # Initialize
    data["skills"] = []
    data["experience"] = None
    data["education"] = None

  # ✅ FORCE SKILL EXTRACTION (works always)

    known_skills = [
        "python",
        "sql",
        "machine learning",
        "data science",
        "deep learning",
        "excel",
        "power bi"
    ]

    text_lower = text.lower()

    skills_found = []

    text_compact = text_lower.replace(" ", "").replace("\n", "")

    skills_found=[]

    for skill in known_skills:
        skill_compact=skill.replace(" ","")

        if skill_compact in text_compact:
             skills_found.append(skill)

    data["skills"] = skills_found

    # -------- EXPERIENCE --------
    if "experience" in text_lower:
        exp_part = text_lower.split("experience")[1]

        if "education" in exp_part:
            exp_part = exp_part.split("education")[0]

        data["experience"] = exp_part.strip()

    # -------- EDUCATION --------
    if "education" in text_lower:
        edu_part = text_lower.split("education")[1]
        data["education"] = edu_part.strip()

    return data