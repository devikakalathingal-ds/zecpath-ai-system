import time
import os

from parsers.resume_reader import read_resume
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text


# Resume file (inside resumes folder)
file_path = os.path.join("resumes", "sample_resume.pdf")

start = time.time()

# Step 1: Read resume
raw_text = read_resume(file_path)

# Step 2: Clean text
cleaned_text = clean_text(raw_text)

# Step 3: Normalize text
normalized_text = normalize_text(cleaned_text)

end = time.time()

# Output stats
print("\n===== RESUME TEST OUTPUT =====\n")
print("Raw Length:", len(raw_text))
print("Cleaned Length:", len(cleaned_text))
print("Processing Time:", round(end - start, 4), "seconds")

# Ensure output folder exists
os.makedirs("data/extracted_resumes", exist_ok=True)

# Save output
output_path = "data/extracted_resumes/output.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(normalized_text)

print("\n✅ Resume processed successfully!")
print("Saved at:", output_path)