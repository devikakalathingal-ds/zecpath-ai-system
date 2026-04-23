# utils/academic_profile_builder.py

def build_academic_profile(education_list, certifications):

    profile = {
        "education": [],
        "certifications": []
    }

    # -------------------------
    # EDUCATION
    # -------------------------
    for edu in education_list:
        profile["education"].append({
            "degree": edu.get("degree", ""),
            "institution": edu.get("institution", ""),
            "graduation_year": edu.get("graduation_year", "")
        })

    # -------------------------
    # CERTIFICATIONS
    # -------------------------
    seen = set()  # avoid duplicates

    for cert in certifications:
        clean_cert = cert.strip()

        if clean_cert and clean_cert.lower() not in seen:
            seen.add(clean_cert.lower())

            profile["certifications"].append({
                "name": clean_cert,
                "issuer": detect_issuer(clean_cert)
            })

    return profile


# -------------------------
# HELPER FUNCTION
# -------------------------
def detect_issuer(cert):

    cert = cert.lower()

    if "coursera" in cert:
        return "Coursera"
    elif "udemy" in cert:
        return "Udemy"
    elif "aws" in cert:
        return "AWS"
    elif "google" in cert:
        return "Google"
    elif "microsoft" in cert:
        return "Microsoft"
    elif "edx" in cert:
        return "edX"
    else:
        return "Unknown"