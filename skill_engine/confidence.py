# confidence.py

def calculate_confidence(text, skill):
    """
    Calculate confidence score based on how many times
    the skill appears in the resume text.
    """

    count = text.count(skill)

    if count >= 3:
        return 0.95
    elif count == 2:
        return 0.85
    elif count == 1:
        return 0.75
    else:
        return 0.0