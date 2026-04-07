def calculate_ats_score(resume_skills, job_description):
    """
    Calculates ATS score based on skill matching with job description.

    Returns:
        score (float): percentage score
        matched (list): skills found in job description
        missing (list): skills not found in job description
    """

    # If no skills found in resume
    if not resume_skills:
        return 0.0, [], []

    jd = job_description.lower()

    # Normalize job description (remove spaces/newlines)
    jd_compact = jd.replace(" ", "").replace("\n", "")

    matched = []
    missing = []

    for skill in resume_skills:
        skill_compact = skill.lower().replace(" ", "")

        if skill_compact in jd_compact:
            matched.append(skill)
        else:
            missing.append(skill)

    # Avoid division by zero
    if len(resume_skills) == 0:
        score = 0.0
    else:
        score = (len(matched) / len(resume_skills)) * 100

    return round(score, 2), matched, missing