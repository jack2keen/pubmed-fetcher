# papers/fetcher.py
from Bio import Entrez
from bs4 import BeautifulSoup

Entrez.email = "youremail@example.com"  # Replace with your real email

def fetch_pubmed_ids(query: str, max_results: int = 100):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def fetch_pubmed_details(ids):
    handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
    records = Entrez.read(handle)
    articles = []

    for article in records['PubmedArticle']:
        medline = article['MedlineCitation']
        article_data = medline.get('Article', {})

        item = {
            "pmid": medline.get('PMID', ''),
            "title": article_data.get('ArticleTitle', ''),
            "pub_date": _extract_date(article_data),
            "authors": _extract_authors(article_data),
            "corresponding_email": ""
        }

        for author in item['authors']:
            if author["email"]:
                item["corresponding_email"] = author["email"]
                break

        articles.append(item)
    return articles

def _extract_date(article_data):
    pub_date = article_data.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {})
    return pub_date.get("Year", pub_date.get("MedlineDate", ""))

def _extract_authors(article_data):
    author_list = []
    for author in article_data.get("AuthorList", []):
        name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
        affils = author.get("AffiliationInfo", [])
        affil = affils[0]["Affiliation"] if affils else ""
        email = ""
        if "@" in affil:
            email = affil.split()[-1].strip('.,;()')
        author_list.append({"author": name, "affiliation": affil, "email": email})
    return author_list
