from parsers.resume_reader import extract_text
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text
from utils.entity_extractor import extract_entities
from utils.ats_scorer import calculate_ats_score

# 1. Give your resume file
pdf_file = "sample_resume.pdf"

# 2. Job Description (you can also load this from a file later)
job_description = """
We are looking for a Data Analyst with strong skills in Python, SQL,
data visualization (Tableau/Power BI), and basic Machine Learning.
The candidate should have experience in handling datasets,
data cleaning, and generating insights.
"""

try:
    # 3. Extract raw text
    raw_text = extract_text(pdf_file)

    # 4. Clean text
    cleaned_text = clean_text(raw_text)

    # 5. Normalize text
    normalized_text = normalize_text(cleaned_text)

    print("\n===== NORMALIZED TEXT =====\n")
    print(normalized_text)
    print("\n===========================\n") 

    # 6. Extract entities
    entities = extract_entities(normalized_text)

    print("Entities found in PDF:")
    for key, value in entities.items():
        print(f"{key}: {value}")

    # 7. Calculate ATS Score
    ats_score = calculate_ats_score(normalized_text, job_description)

    print("\n===== ATS SCORE =====")
    print(ats_score)

except Exception as e:
    print("Error:", e)