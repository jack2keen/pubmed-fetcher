# PubMed Fetcher CLI

This is a command-line tool to search PubMed for research papers and identify papers with non-academic authors.

## Project Structure

- `cli.py`: Entry point for the command-line interface.
- `papers/fetcher.py`: Logic for querying PubMed and retrieving paper details.
- `papers/parser.py`: Functions for parsing author info and filtering non-academic ones.
- `papers/utils.py`: Utility functions used across the codebase.
- `pyproject.toml`: Project configuration and dependencies.

## How to Use

### Setup

1. Make sure Python 3.12+ and Poetry(https://python-poetry.org) are installed.
2. Clone the repository and install dependencies:

```bash
git clone https://github.com/jack2keen/pubmed-fetcher.git
cd pubmed-fetcher
poetry install
Run the CLI
bash
Copy
Edit
poetry run get-papers-list "your search query"
Optional flags:

--file or -f: Save the output to a CSV file.

--debug or -d: Print debug logs.

--help or -h: Show help message.

How Non-Academic Authors Are Identified
A simple set of heuristics is used:

Email domain doesn’t end with .edu, .ac, etc.

Affiliation text doesn't include terms like "university", "college", or "institute".

Tools and Libraries Used :

Typer
BioPython
BeautifulSoup
pandas
Poetry

Author
Somesh Kumar Patel – someshkumarp3@gmail.com