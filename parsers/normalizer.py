import re

def normalize_text(text):
    text = text.lower()

    # Sections
    sections = ["skills", "experience", "education"]
    for section in sections:
        text = re.sub(rf"\b{section}\b", f"\n\n{section}\n", text)

    # Break skills into lines (simple logic)
    text = re.sub(r"skills\s+([a-z\s]+?)\s+experience", 
                  lambda m: "skills\n" + "\n".join(m.group(1).split()) + "\n\nexperience", 
                  text)

    # Email & phone
    text = re.sub(r"(email:)", r"\n\1", text)
    text = re.sub(r"(phone:)", r"\n\1", text)

    return text.strip()