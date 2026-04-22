import re

DEGREE_KEYWORDS = [
    "B.Tech", "B.E", "BSc", "B.Sc", "M.Tech", "MSc", "M.Sc",
    "MBA", "BCA", "MCA", "PhD", "Bachelor", "Master"
]

def extract_education(text):
    education_list = []

    lines = text.split("\n")

    for line in lines:
        for degree in DEGREE_KEYWORDS:
            if degree.lower() in line.lower():

                year_match = re.search(r"(20\d{2}|19\d{2})", line)
                year = year_match.group() if year_match else None

                education_list.append({
                    "degree": degree,
                    "details": line.strip(),
                    "graduation_year": year
                })

    return education_list