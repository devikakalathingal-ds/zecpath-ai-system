"""
Zecpath ATS Scoring Engine - FINAL CONSOLIDATED VERSION
(No external dependencies, production-ready)
"""

# =====================================================
# ROLE WEIGHTS
# =====================================================

ROLE_WEIGHTS = {
    "software_engineer": {
        "skill": 0.40,
        "experience": 0.30,
        "education": 0.10,
        "semantic": 0.20
    },
    "data_scientist": {
        "skill": 0.35,
        "experience": 0.25,
        "education": 0.15,
        "semantic": 0.25
    },
    "fresher": {
        "skill": 0.50,
        "experience": 0.10,
        "education": 0.20,
        "semantic": 0.20
    },
    "ml_engineer": {
        "skill": 0.40,
        "experience": 0.20,
        "education": 0.15,
        "semantic": 0.25
    }
}

# =====================================================
# SKILL KNOWLEDGE BASE (CATEGORY SYSTEM)
# =====================================================

SKILL_CATEGORIES = {
    "programming": ["python", "java", "c++", "javascript"],
    "data": ["sql", "excel", "power bi", "tableau"],
    "ml_ai": ["machine learning", "deep learning", "ai", "nlp"],
    "web": ["react", "node", "html", "css"],
    "analysis": ["data analysis", "statistics", "reporting"],
    "healthcare": ["pharmacovigilance", "drug safety", "clinical", "medical"]
}

# =====================================================
# SAFE NORMALIZER
# =====================================================

def normalize(score):
    if score is None:
        return 0
    return max(0, min(float(score), 100))

# =====================================================
# SKILL SCORE (CATEGORY BASED)
# =====================================================

def skill_score(skills, jd_text):

    if not skills:
        return 0

    jd_text = jd_text.lower()
    matched_categories = set()

    for s in skills:

        if isinstance(s, dict):
            skill = s.get("skill", "").lower()
        else:
            skill = str(s).lower()

        if not skill:
            continue

        for category, skill_list in SKILL_CATEGORIES.items():
            if any(skill in item or item in skill for item in skill_list):
                matched_categories.add(category)

    return (len(matched_categories) / len(SKILL_CATEGORIES)) * 100

# =====================================================
# EXPERIENCE SCORE (IMPROVED INTELLIGENCE)
# =====================================================

def experience_score(experience, jd_text):

    if not experience:
        return 0

    jd_text = jd_text.lower()
    total_score = 0

    for exp in experience:

        if isinstance(exp, dict):
            role = exp.get("role", "").lower()
            company = exp.get("company", "").lower()
            details = " ".join(exp.get("details", [])).lower()
        else:
            role = ""
            company = ""
            details = str(exp).lower()

        text = f"{role} {company} {details}"

        score = 0

        # JD overlap
        for word in ["drug", "safety", "clinical", "data", "analysis"]:
            if word in text and word in jd_text:
                score += 2

        # role relevance
        if any(x in text for x in ["intern", "analyst", "scientist"]):
            score += 3

        # pharma boost
        if any(x in text for x in ["pharmacovigilance", "drug safety"]):
            score += 5

        # detail depth
        if len(details.split()) > 10:
            score += 2

        total_score += min(score * 10, 60)

    return min(total_score, 100)

# =====================================================
# EDUCATION SCORE
# =====================================================

def education_score(education, jd_text):

    if not education:
        return 0

    for edu in education:
        degree = edu.get("degree", "").lower()

        if "pharmacy" in degree:
            return 70
        if "master" in degree:
            return 100

    return 40

# =====================================================
# SEMANTIC SCORE
# =====================================================

def semantic_score(embedding_score):
    return normalize(embedding_score * 100)

# =====================================================
# FINAL SCORE CALCULATION
# =====================================================

def calculate_final_score(
    skills,
    experience,
    education,
    embedding_score,
    jd_text,
    role="software_engineer"
):

    weights = ROLE_WEIGHTS.get(role, ROLE_WEIGHTS["software_engineer"])

    skill = normalize(skill_score(skills, jd_text))
    exp = normalize(experience_score(experience, jd_text))
    edu = normalize(education_score(education, jd_text))
    sem = semantic_score(embedding_score)

    final = (
        skill * weights["skill"] +
        exp * weights["experience"] +
        edu * weights["education"] +
        sem * weights["semantic"]
    )

    explanation = []

    if skill >= 60:
        explanation.append("Strong skill match")
    else:
        explanation.append("Skill gap detected")

    if exp >= 60:
        explanation.append("Relevant experience found")
    else:
        explanation.append("Experience is weak or missing")

    if edu >= 60:
        explanation.append("Education aligns with role")

    if sem >= 70:
        explanation.append("High semantic similarity")

    return round(final, 2), {
        "skill": skill,
        "experience": exp,
        "education": edu,
        "semantic": sem,
        "weights": weights,
        "explanation": explanation
    }