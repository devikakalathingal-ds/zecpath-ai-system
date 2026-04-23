import re

def extract_experience(text):

    if not text:
        return []

    text_lower = text.lower()

    # must have experience section
    if "experience" not in text_lower:
        return []

    # isolate only experience section
    exp_section = text_lower.split("experience")[-1]

    # stop at next section if exists
    for stop_word in ["education", "skills", "certifications"]:
        if stop_word in exp_section:
            exp_section = exp_section.split(stop_word)[0]

    lines = [l.strip() for l in exp_section.split("\n") if l.strip()]

    experiences = []
    current = None

    for line in lines:

        line_lower = line.lower()

        # detect company
        if any(k in line_lower for k in ["ltd", "pvt", "limited", "company", "analytics", "healthcare"]):
            current = {
                "company": line,
                "role": "",
                "details": []
            }
            experiences.append(current)
            continue

        # detect role
        if current and any(k in line_lower for k in ["intern", "engineer", "analyst", "scientist", "developer"]):
            current["role"] = line
            continue

        # add details only if experience exists
        if current:
            current["details"].append(line)

    return experiences