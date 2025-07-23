import typer
import logging
from papers.fetcher import fetch_pubmed_ids, fetch_pubmed_details
from papers.parser import extract_non_academic_authors

app = typer.Typer()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.command()
def main(
    query: str,
    file: str = typer.Option(None, "--file", "-f", help="File to save results."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output."),
):
    """
    Search PubMed for a query and print/save papers with non-academic authors.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info(f"Query: {query}")
    ids = fetch_pubmed_ids(query)
    logger.info(f"Found {len(ids)} PubMed IDs.")

    if not ids:
        typer.echo("No articles found.")
        raise typer.Exit(code=0)

    logger.debug(f"Fetching details for {len(ids)} PubMed IDs")
    articles = fetch_pubmed_details(ids)

    all_results = []
    for article in articles:
        non_academic_authors = extract_non_academic_authors(article)
        if non_academic_authors:
            title = article.get("Title", "")
            all_results.append((title, non_academic_authors))

    if not all_results:
        typer.echo(" No non-academic authors found.")
        return

    if file:
        import csv
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Authors"])
            for title, authors in all_results:
                writer.writerow([title, "; ".join(authors)])
        typer.echo(f"Results saved to {file}")
    else:
        typer.echo(f"Found {len(all_results)} non-academic papers:")
        for title, authors in all_results:
            typer.echo(f"- {title}")
            for author in authors:
                typer.echo(f"    - {author}")

if __name__ == "__main__":
    app()
