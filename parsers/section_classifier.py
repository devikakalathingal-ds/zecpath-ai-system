import re

def classify_sections(text):
    sections = {
        "Skills": "",
        "Work Experience": "",
        "Education": "",
        "Projects": "",
        "Certifications": "",
        "Others": ""
    }

    current_section = "Others"

    # Keywords for detecting sections
    section_keywords = {
        "Skills": ["skills", "technical skills"],
        "Work Experience": ["experience", "work experience", "employment history"],
        "Education": ["education", "academic background"],
        "Projects": ["projects", "project"],
        "Certifications": ["certifications", "certification"]
    }

    lines = text.split("\n")

    for line in lines:
        clean_line = line.strip().lower()

        found_section = False

        for section, keywords in section_keywords.items():
            for keyword in keywords:
                if keyword in clean_line:
                    current_section = section
                    found_section = True
                    break
            if found_section:
                break

        if not found_section:
            sections[current_section] += line + "\n"

    return sections