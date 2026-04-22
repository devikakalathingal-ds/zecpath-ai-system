def calculate_ats_score(resume_skills, job_description):
    """
    Calculates ATS score based on skill matching with job description.
    Returns:
        score (float)
        matched (list)
        missing (list)
    """

    if not resume_skills:
        return 0.0, [], []

    jd = job_description.lower()

    matched = []
    missing = []

    # Flatten skills from your extractor
    flat_skills = []

    if isinstance(resume_skills, dict):
        for category in resume_skills.values():
            for item in category:
                flat_skills.append(item["skill"])
    else:
        flat_skills = resume_skills

    for skill in flat_skills:
        if skill.lower() in jd:
            matched.append(skill)
        else:
            missing.append(skill)

    score = (len(matched) / len(flat_skills)) * 100 if flat_skills else 0.0

    return round(score, 2), matched, missing