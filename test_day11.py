import os

from education_parser.education_extractor import extract_education
from education_parser.certification_extractor import extract_certifications
from education_parser.relevance_logic import check_education_relevance


RESUME_FOLDER = "resumes"


def read_resume(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# 👉 CHANGE ONLY THIS VALUE WHEN NEEDED
file_name = "resume1.txt"   # 👈 MANUALLY SET FILE HERE


file_path = os.path.join(RESUME_FOLDER, file_name)

text = read_resume(file_path)

education = extract_education(text)
certifications = extract_certifications(text)
relevance = check_education_relevance(education, "Data Scientist")


print("\n==============================")
print("📄 Resume File:", file_name)
print("==============================")

print("\n📚 Education:")
print(education)

print("\n📜 Certifications:")
print(certifications)

print("\n🎯 Relevance Score:")
print(relevance)