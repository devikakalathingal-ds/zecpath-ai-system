import PyPDF2
import json
from parsers.section_classifier import classify_sections


def extract_text_from_pdf(pdf_path):
    text = ""

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

    return text


resume_path = "resumes/sample_resume.pdf"

# Extract text
resume_text = extract_text_from_pdf(resume_path)

# Classify
sections = classify_sections(resume_text)

# Save to JSON file
with open("outputs/section_output.json", "w", encoding="utf-8") as f:
    json.dump(sections, f, indent=4)

print("Section classification completed and saved to outputs/section_output.json ✅")