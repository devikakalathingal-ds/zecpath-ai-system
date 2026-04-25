"""
ranking_engine.py

Handles:
- Candidate ranking
- Decision assignment (Shortlist / Review / Reject)
- Top candidate selection
"""


def rank_candidates(candidates):
    """
    Sort candidates by score (highest first)
    """
    return sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)


def assign_decision(score, shortlist_threshold=75, reject_threshold=50):
    """
    Assign decision based on score
    """
    if score >= shortlist_threshold:
        return "SHORTLISTED"
    elif score >= reject_threshold:
        return "REVIEW"
    else:
        return "REJECTED"


def process_candidates(candidates):
    """
    Rank candidates and assign decisions
    """
    ranked_candidates = rank_candidates(candidates)

    for candidate in ranked_candidates:
        score = candidate.get("score", 0)
        candidate["decision"] = assign_decision(score)

    return ranked_candidates


def get_top_candidates(candidates, top_n=3):
    """
    Get top N candidates
    """
    ranked_candidates = rank_candidates(candidates)
    return ranked_candidates[:top_n]


# -------------------------
# TESTING (for beginners)
# -------------------------
if __name__ == "__main__":

    # Sample data
    candidates = [
        {"name": "Anu", "score": 85},
        {"name": "Rahul", "score": 72},
        {"name": "Meena", "score": 48},
        {"name": "Arjun", "score": 90}
    ]

    # Process candidates
    ranked = process_candidates(candidates)
    top = get_top_candidates(candidates, top_n=3)

    print("\n=== Ranked Candidates ===")
    for c in ranked:
        print(c)

    print("\n=== Top Candidates ===")
    for c in top:
        print(c)