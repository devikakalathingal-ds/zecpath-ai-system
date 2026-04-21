import re
import fitz  # PyMuPDF
from datetime import datetime


# ---------------- FILE TEXT EXTRACTION ---------------- #

def extract_text(file_path):

    # If PDF
    if file_path.endswith(".pdf"):
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        return text

    # If TXT
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    else:
        return ""


# ---------------- EXPERIENCE EXTRACTION ---------------- #

def extract_experience(text):

    experience_list = []

    pattern = r"(?P<role>[A-Za-z ]+)\s+at\s+(?P<company>[A-Za-z ]+)\s+\((?P<start>\w+ \d{4})\s*-\s*(?P<end>\w+ \d{4}|Present)\)"

    matches = re.finditer(pattern, text)

    for match in matches:
        role = match.group("role").strip()
        company = match.group("company").strip()
        start = match.group("start")
        end = match.group("end")

        duration = calculate_duration(start, end)

        experience_list.append({
            "role": role,
            "company": company,
            "start_date": start,
            "end_date": end,
            "duration_years": round(duration, 2)
        })

    return experience_list


# ---------------- DURATION CALCULATION ---------------- #

def calculate_duration(start, end):

    start_date = datetime.strptime(start, "%b %Y")

    if end.lower() == "present":
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end, "%b %Y")

    return (end_date - start_date).days / 365


def calculate_total_experience(experience_list):

    total = sum(exp["duration_years"] for exp in experience_list)
    return round(total, 2)


# ---------------- RELEVANCE CALCULATION ---------------- #

def calculate_relevance(job_description, experience_list):

    jd_words = set(job_description.lower().split())

    score = 0
    max_score = len(experience_list) * 100

    for exp in experience_list:
        role_words = set(exp["role"].lower().split())

        if jd_words.intersection(role_words):
            score += 100

    if max_score == 0:
        return 0

    return round((score / max_score) * 100, 2)


# ---------------- MAIN EXECUTION ---------------- #

if __name__ == "__main__":

    resume_path = "resumes/sample_resume.pdf"
    jd_path = "Job Description/Aggregate Report Writer.txt"

    # Extract resume text
    resume_text = extract_text(resume_path)

    # Extract JD text
    jd_text = extract_text(jd_path)

    # Extract experience
    experience = extract_experience(resume_text)

    print("Extracted Experience:")
    print(experience)

    total = calculate_total_experience(experience)
    print("Total Experience:", total, "years")

    relevance_score = calculate_relevance(jd_text, experience)
    print("Relevance Score:", relevance_score, "%")