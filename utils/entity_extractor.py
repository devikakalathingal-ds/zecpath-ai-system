import re

def extract_entities(text):

    if not text:
        return {}

    data = {}

    # -------------------------
    # EMAIL
    # -------------------------
    email = re.findall(r'\S+@\S+', text)
    data["email"] = email[0] if email else None

    # -------------------------
    # PHONE
    # -------------------------
    phone = re.findall(r'\b\d{10}\b', text)
    data["phone"] = phone[0] if phone else None

    text_lower = text.lower()

    # -------------------------
    # SKILLS (SAFE MATCH)
    # -------------------------
    known_skills = [
        "python", "sql", "react",
        "machine learning", "data analysis",
        "excel", "power bi"
    ]

    data["skills"] = [
        skill for skill in known_skills
        if skill in text_lower
    ]

    # -------------------------
    # IMPORTANT RULE:
    # DO NOT PARSE EXPERIENCE / EDUCATION HERE
    # (already handled in main.py)
    # -------------------------

    return data