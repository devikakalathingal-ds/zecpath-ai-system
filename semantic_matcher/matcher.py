from embedding import get_embedding
from similarity import get_similarity
import PyPDF2

# ----------------------------
# READ FILE FUNCTIONS
# ----------------------------

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# ----------------------------
# FILE PATHS (MANUAL INPUT)
# ----------------------------

resume_path = "resumes/resume4.txt"   # change this anytime
jd_path = "Job Description/Drug Safety Scientist.txt"


# ----------------------------
# LOAD RESUME
# ----------------------------

if resume_path.endswith(".txt"):
    resume_text = read_txt(resume_path)
elif resume_path.endswith(".pdf"):
    resume_text = read_pdf(resume_path)
else:
    raise ValueError("Unsupported resume format")


# ----------------------------
# LOAD JOB DESCRIPTION
# ----------------------------

job_description = read_txt(jd_path)


# ----------------------------
# EMBEDDINGS
# ----------------------------

resume_embedding = get_embedding(resume_text)
jd_embedding = get_embedding(job_description)


# ----------------------------
# SIMILARITY SCORE
# ----------------------------

score = get_similarity(resume_embedding, jd_embedding)


# ----------------------------
# OUTPUT
# ----------------------------

print("\n--- RESULT ---")
print("Resume:", resume_path)
print("Job Description:", jd_path)
print("Similarity Score:", round(score, 2))


# ----------------------------
# FINAL CLASSIFICATION
# ----------------------------

if score >= 0.75:
    print("Result: 🔥 Strong Match")
elif score >= 0.5:
    print("Result: 👍 Moderate Match")
else:
    print("Result: ❌ Low Match")