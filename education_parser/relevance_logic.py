def normalize_degree(degree):
    degree = degree.lower()

    if "b.tech" in degree or "b.e" in degree:
        return "Bachelor of Technology"
    elif "m.tech" in degree:
        return "Master of Technology"
    elif "bsc" in degree:
        return "Bachelor of Science"
    elif "msc" in degree:
        return "Master of Science"

    return degree.title()


def check_education_relevance(education_list, job_role):

    relevant_fields = {
        "Data Scientist": ["computer", "data", "statistics", "ai", "machine learning"],
        "Software Engineer": ["computer", "software", "it", "information"]
    }

    results = []

    for edu in education_list:
        score = 0
        details = edu["details"].lower()

        for keyword in relevant_fields.get(job_role, []):
            if keyword in details:
                score += 1

        results.append({
            "degree": edu["degree"],
            "relevance_score": score
        })

    return results