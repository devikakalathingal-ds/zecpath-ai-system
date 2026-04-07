import tkinter as tk
from tkinter import filedialog, messagebox

from parsers.resume_reader import extract_text
from parsers.text_cleaner import clean_text
from parsers.normalizer import normalize_text
from utils.entity_extractor import extract_entities
from utils.ats_scorer import calculate_ats_score


#  PUT YOUR FUNCTION HERE (TOP PART)
def upload_resume():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")]
    )

    if not file_path:
        return

    try:
        raw_text = extract_text(file_path)
        cleaned_text = clean_text(raw_text)
        normalized_text = normalize_text(cleaned_text)

        job_description = jd_text.get("1.0", tk.END).strip()

        if not job_description:
            messagebox.showwarning("Warning", "Please enter Job Description")
            return

        entities = extract_entities(normalized_text)
        resume_skills = entities.get("skills", [])

        ats_score, matched, missing = calculate_ats_score(resume_skills, job_description)

        output_text.delete("1.0", tk.END)

        output_text.insert(tk.END, "===== ATS SCORE =====\n")
        output_text.insert(tk.END, f"Score: {ats_score}%\n\n")

        output_text.insert(tk.END, "===== MATCHED SKILLS =====\n")
        for skill in matched:
            output_text.insert(tk.END, f"- {skill}\n")

        output_text.insert(tk.END, "\n===== MISSING SKILLS =====\n")
        for skill in missing:
            output_text.insert(tk.END, f"- {skill}\n")

        output_text.insert(tk.END, "\n===== RESUME PREVIEW =====\n")
        output_text.insert(tk.END, normalized_text[:2000])

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ✅ UI STARTS HERE
root = tk.Tk()
root.title("ZecPath AI - Resume Analyzer")
root.geometry("900x700")

title_label = tk.Label(root, text="ZecPath AI Resume Analyzer", font=("Arial", 16))
title_label.pack(pady=10)

# Job Description input
jd_label = tk.Label(root, text="Enter Job Description:")
jd_label.pack()

jd_text = tk.Text(root, height=8)
jd_text.pack(fill="x", padx=10, pady=5)

# Upload button
upload_button = tk.Button(root, text="Upload Resume", command=upload_resume)
upload_button.pack(pady=10)

# Output box
output_text = tk.Text(root, wrap="word")
output_text.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()