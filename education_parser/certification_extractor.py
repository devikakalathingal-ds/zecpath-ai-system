CERTIFICATION_KEYWORDS = [
    "certified", "certification", "AWS", "Google", "Microsoft",
    "Coursera", "Udemy", "edX"
]

def extract_certifications(text):
    certifications = []

    lines = text.split("\n")

    for line in lines:
        for word in CERTIFICATION_KEYWORDS:
            if word.lower() in line.lower():
                certifications.append(line.strip())

    return certifications