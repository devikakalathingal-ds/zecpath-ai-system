import time
from parsers.resume_reader import extract_text
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text

file_path = "sample_resume.pdf"   # Put your resume file in main project folder

start = time.time()

raw_text = extract_text(file_path)
cleaned_text = clean_text(raw_text)
normalized_text = normalize_text(cleaned_text)

end = time.time()

print("Raw Length:", len(raw_text))
print("Cleaned Length:", len(cleaned_text))
print("Processing Time:", end - start)

# Save output
with open("data/extracted_resumes/output.txt", "w", encoding="utf-8") as f:
    f.write(normalized_text)
print("Resume processed successfully!")