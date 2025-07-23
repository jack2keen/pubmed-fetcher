# cli.py
import typer
import logging
import csv
from papers.fetcher import fetch_pubmed_ids, fetch_pubmed_details
from papers.utils import is_non_academic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(query: str, file: str = "results.csv", debug: bool = False):
    if debug:
        logger.setLevel(logging.DEBUG)

    logger.info(f"Query: {query}")
    logger.debug(f"Searching PubMed for query: {query}")
    ids = fetch_pubmed_ids(query)
    logger.info(f"Found {len(ids)} PubMed IDs.")
    if not ids:
        logger.warning("No results found. Exiting.")
        with open(file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "PubmedID", "Title", "Publication Date",
                "Non-academic Author(s)", "Company Affiliation(s)",
                "Corresponding Author Email"
            ])
            writer.writeheader()
        return


    logger.debug(f"Fetching details for {len(ids)} PubMed IDs")
    articles = fetch_pubmed_details(ids)

    all_results = []
    for article in articles:
        non_acads = []
        companies = []

        for a in article['authors']:
            if is_non_academic(a['affiliation']):
                non_acads.append(a['author'])
                companies.append(a['affiliation'])

        if non_acads:
            all_results.append({
                "PubmedID": article["pmid"],
                "Title": article["title"],
                "Publication Date": article["pub_date"],
                "Non-academic Author(s)": "; ".join(non_acads),
                "Company Affiliation(s)": "; ".join(companies),
                "Corresponding Author Email": article["corresponding_email"]
            })

    with open(file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "PubmedID", "Title", "Publication Date",
            "Non-academic Author(s)", "Company Affiliation(s)",
            "Corresponding Author Email"
        ])
        writer.writeheader()
        writer.writerows(all_results)

    logger.info(f"✅ Found {len(all_results)} non-academic entries. Saved to {file}.")

if __name__ == "__main__":
    typer.run(main)
