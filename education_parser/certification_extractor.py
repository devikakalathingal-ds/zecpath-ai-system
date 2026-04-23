import re

CERTIFICATION_KEYWORDS = [
    "aws", "google", "microsoft", "coursera", "udemy", "edx"
]

def extract_certifications(text):

    certifications = []

    text_lower = text.lower()

    # Extract certification section
    match = re.search(r"certifications?:?(.*)", text_lower, re.DOTALL)

    if match:
        section_text = match.group(1)

        # STEP 1: Split by commas, newlines etc.
        parts = re.split(r",|\n|•|-|\|", section_text)

        for part in parts:
            part = part.strip()

            # STEP 2: Further split if multiple certs in same line
            split_parts = re.split(r"(aws|google|microsoft|coursera|udemy|edx)", part)

            temp = ""
            for sp in split_parts:
                sp = sp.strip()
                if not sp:
                    continue

                if sp in CERTIFICATION_KEYWORDS:
                    if temp:
                        certifications.append(temp.strip())
                    temp = sp
                else:
                    temp += " " + sp

            if temp:
                certifications.append(temp.strip())

    # REMOVE DUPLICATES + CLEAN
    clean_list = []
    seen = set()

    for cert in certifications:
        if len(cert) > 5 and cert not in seen:
            clean_list.append(cert)
            seen.add(cert)

    return clean_list