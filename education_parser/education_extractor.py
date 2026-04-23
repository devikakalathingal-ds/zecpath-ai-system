import re

def extract_education(text):

    if not text:
        return []

    text_lower = text.lower()

    if "education" not in text_lower:
        return []

    edu_section = text_lower.split("education")[-1]

    # stop at next section
    for stop in ["experience", "skills", "certifications"]:
        if stop in edu_section:
            edu_section = edu_section.split(stop)[0]

    lines = [l.strip() for l in edu_section.split("\n") if l.strip()]

    education = []
    current = None

    year_range = re.compile(r"(20\d{2})\s*[-–]\s*(20\d{2})")

    for line in lines:

        # detect degree line
        if any(k in line for k in ["bachelor", "b.pharm", "bsc", "msc", "degree"]):
            current = {
                "degree": line,
                "graduation_year": None
            }
            education.append(current)
            continue

        # extract year range
        match = year_range.search(line)
        if match and current:
            current["graduation_year"] = match.group(2)
            continue

        # fallback year detection
        single_year = re.findall(r"(20\d{2})", line)
        if single_year and current and not current["graduation_year"]:
            current["graduation_year"] = single_year[-1]

    return education