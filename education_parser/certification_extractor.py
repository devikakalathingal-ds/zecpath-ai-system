import re

CERT_KEYWORDS = ["coursera", "udemy", "edx", "aws", "google", "microsoft"]

def extract_certifications(text):

    if not text:
        return []

    text_lower = text.lower()

    match = re.search(
        r"certifications?(.*?)(experience|education|skills|$)",
        text_lower,
        re.DOTALL
    )

    if not match:
        return []

    section = match.group(1)

    lines = [l.strip() for l in section.split("\n") if l.strip()]

    certs = []

    for line in lines:
        for key in CERT_KEYWORDS:
            if key in line:
                certs.append(line.strip())
                break

    return list(set(certs))