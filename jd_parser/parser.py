import re
import json
import os


# ---------------------------
# SKILL EXTRACTION
# ---------------------------
def extract_skills(text):
    skills = [
        "python",
        "java",
        "sql",
        "excel",
        "machine learning",
        "power bi",
        "ml"
    ]

    found = []
    text = text.lower()

    for skill in skills:
        if skill in text:
            if skill == "ml":
                found.append("machine learning")
            else:
                found.append(skill)

    return list(set(found))


# ---------------------------
# EXPERIENCE EXTRACTION
# ---------------------------
def extract_experience(text):
    text = text.lower()

    # Match range: 2-5 years OR 2 to 5 years
    range_match = re.search(r'(\d+)\s*(?:-|to)\s*(\d+)\s*years', text)
    if range_match:
        return f"{range_match.group(1)}-{range_match.group(2)} years"

    # Match single: 3+ years OR 3 years
    single_match = re.search(r'(\d+)\+?\s*years', text)
    if single_match:
        return single_match.group()

    return "Not Found"


# ---------------------------
# ROLE EXTRACTION
# ---------------------------
def extract_role(text):
    text = text.lower()

    if "ml engineer" in text:
        return "ML Engineer"
    elif "data analyst" in text or "analyst" in text:
        return "Data Analyst"
    elif "software engineer" in text or "engineer" in text:
        return "Software Engineer"

    return "Not Found"


# ---------------------------
# EDUCATION EXTRACTION
# ---------------------------
def extract_education(text):
    text = text.lower()

    if "master" in text or "m.tech" in text:
        return "Master's Degree"
    elif "bachelor" in text or "b.tech" in text:
        return "Bachelor's Degree"

    return "Not Found"


# ---------------------------
# MAIN PARSER FUNCTION
# ---------------------------
def parse_jd(text):
    return {
        "role": extract_role(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }


# ---------------------------
# RUN SCRIPT
# ---------------------------
if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(BASE_DIR, "sample_jd.txt")
    output_path = os.path.join(BASE_DIR, "jd_output_samples.txt")

    # Read JD
    with open(input_path, "r") as file:
        jd_text = file.read()

    # Parse JD
    result = parse_jd(jd_text)

    print("\nParsed Job Description:\n")
    print(json.dumps(result, indent=2))

    # ---------------------------
    # SAFE MULTI-JD STORAGE
    # ---------------------------

    if os.path.exists(output_path):
        with open(output_path, "r") as file:
            try:
                existing_data = json.load(file)

                # If file contains single dict, convert to list
                if isinstance(existing_data, dict):
                    existing_data = [existing_data]

            except:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(result)

    with open(output_path, "w") as file:
        json.dump(existing_data, file, indent=2)

    print("\nJD appended successfully ✅")