def is_non_academic(affiliation: str) -> bool:
    """
    Simple heuristic to classify an author as non-academic based on affiliation text.
    """
    if not affiliation:
        return False

    affiliation_lower = affiliation.lower()

    academic_keywords = [
        "university", "college", "institute of technology", "school of", "department of", "center for",
        "hospital", "faculty", "dept.", "dept ", "academic", "research institute", "graduate", "education"
    ]

    # If any academic keyword is in the affiliation, consider them academic
    for keyword in academic_keywords:
        if keyword in affiliation_lower:
            return False

    # Otherwise, assume they may be corporate/non-academic
    return True
