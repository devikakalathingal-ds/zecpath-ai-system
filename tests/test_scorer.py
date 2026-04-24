from ats_engine.scorer import calculate_final_score


def test_scorer():

    print("\n==============================")
    print(" ATS SCORER TEST STARTED")
    print("==============================\n")

    # -------------------------
    # SAMPLE INPUT DATA
    # -------------------------

    skills = [
        {"skill": "python"},
        {"skill": "sql"},
        {"skill": "machine learning"}
    ]

    experience = [
        "worked on python backend development",
        "data analysis and ML projects"
    ]

    education = [
        {"degree": "bachelor of pharmacy"}
    ]

    jd_text = "python developer with sql and machine learning experience"

    embedding_score = 0.72

    # -------------------------
    # CALL SCORER
    # -------------------------

    final_score, breakdown = calculate_final_score(
        skills=skills,
        experience=experience,
        education=education,
        embedding_score=embedding_score,
        jd_text=jd_text,
        role="software_engineer"
    )

    # -------------------------
    # OUTPUT
    # -------------------------

    print("FINAL SCORE:", final_score)
    print("\nBREAKDOWN:")
    print(breakdown)

    print("\n==============================")
    print(" TEST COMPLETED SUCCESSFULLY")
    print("==============================\n")


if __name__ == "__main__":
    test_scorer()