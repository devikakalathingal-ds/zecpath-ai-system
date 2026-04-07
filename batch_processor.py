import os
import csv

from parsers.resume_reader import extract_text
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text
from utils.entity_extractor import extract_entities

RESUME_FOLDER = "resumes"
OUTPUT_FOLDER = "outputs"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "results.csv")


def process_resumes():

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    results = []

    for file in os.listdir(RESUME_FOLDER):

        if file.endswith(".pdf") or file.endswith(".docx"):

            file_path = os.path.join(RESUME_FOLDER, file)

            raw_text = extract_text(file_path)
            cleaned_text = clean_text(raw_text)
            normalized_text = normalize_text(cleaned_text)

            entities = extract_entities(normalized_text)

            entities["file_name"] = file

            results.append(entities)

    if results:

        keys = results[0].keys()

        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)

        print("✅ Batch processing complete.")
        print("📄 Results saved to outputs/results.csv")

    else:
        print("⚠ No resumes found in resumes folder.")


if __name__ == "__main__":
    process_resumes()