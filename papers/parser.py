def extract_non_academic_authors(article: dict) -> list[str]:
    non_academic = []

    authors = article.get("Authors", [])
    for author in authors:
        name = author.get("Name", "")
        affiliation = author.get("Affiliation", "")
        email = author.get("Email", "")

        if (
            any(keyword in affiliation.lower() for keyword in ["inc", "llc", "gmbh", "pvt", "ltd", "company", "corporation", "corp"])
            or any(domain in email.lower() for domain in ["@gmail.", "@yahoo.", "@hotmail.", "@outlook."])
        ):
            non_academic.append(f"{name} ({affiliation})")

    return non_academic




def extract_authors_and_affiliations(pubmed_article):
    """
    Extracts authors and their affiliations from a single PubMed article.
    Returns a list of dicts with author name, email, and affiliation.
    """
    article = pubmed_article["MedlineCitation"]["Article"]
    author_list = article.get("AuthorList", [])
    result = []

    for author in author_list:
        name = []
        if "ForeName" in author:
            name.append(author["ForeName"])
        if "LastName" in author:
            name.append(author["LastName"])
        full_name = " ".join(name)

        affiliations = author.get("AffiliationInfo", [])
        for aff in affiliations:
            result.append({
                "author": full_name,
                "affiliation": aff.get("Affiliation", ""),
                "email": extract_email(aff.get("Affiliation", ""))
            })

    return result


def extract_email(affiliation_text):
    """
    Extracts an email address from an affiliation string using a simple heuristic.
    """
    import re
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation_text)
    return match.group(0) if match else None
