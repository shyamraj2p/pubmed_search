import requests
import xml.etree.ElementTree as ET
import csv
import time
import re
import argparse
from concurrent.futures import ThreadPoolExecutor

PUBMED_API_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
COMPANY_KEYWORDS = ["pharma", "biotech", "therapeutics", "biosciences", "medtech", "inc", "ltd", "corp", "gmbh"]
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def fetch_pubmed_papers(query, max_results=50, debug=False):
    search_url = f"{PUBMED_API_BASE}esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "xml", "retmax": max_results}
    response = requests.get(search_url, params=params)
    
    if response.status_code != 200:
        print(f"Error: PubMed API returned status code {response.status_code}")
        return []

    try:
        root = ET.fromstring(response.content)
        paper_ids = [id_elem.text for id_elem in root.findall(".//Id")]
        if debug:
            print(f"Found {len(paper_ids)} paper IDs.")
        return paper_ids
    except ET.ParseError:
        print("Error parsing XML from PubMed response")
        return []

def fetch_paper_details(paper_id, debug=False):
    fetch_url = f"{PUBMED_API_BASE}efetch.fcgi"
    params = {"db": "pubmed", "id": paper_id, "retmode": "xml"}

    delay = 2
    max_retries = 5

    for attempt in range(max_retries):
        response = requests.get(fetch_url, params=params)

        if response.status_code == 429:
            if debug:
                print(f"Rate limit exceeded for {paper_id}, retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2
            continue

        if response.status_code != 200:
            print(f"Error fetching paper {paper_id}: HTTP {response.status_code}")
            return None

        try:
            root = ET.fromstring(response.content)
            break
        except ET.ParseError:
            print(f"Error parsing XML for paper {paper_id}")
            return None
    else:
        return None

    paper_details = {
        "PubmedID": paper_id,
        "Title": "",
        "Publication Date": "",
        "Non-academic Authors": [],
        "Company Affiliations": [],
        "Corresponding Author Email": ""
    }

    title_elem = root.find(".//ArticleTitle")
    if title_elem is not None:
        paper_details["Title"] = title_elem.text

    date_elem = root.find(".//PubDate/Year")
    if date_elem is not None:
        paper_details["Publication Date"] = date_elem.text

    authors = root.findall(".//Author")
    for author in authors:
        affiliation_elem = author.find(".//Affiliation")
        if affiliation_elem is not None:
            affiliation = affiliation_elem.text.lower()
            if any(keyword in affiliation for keyword in COMPANY_KEYWORDS):
                last_name = author.find("LastName")
                if last_name is not None:
                    paper_details["Non-academic Authors"].append(last_name.text)
                paper_details["Company Affiliations"].append(affiliation)

        if affiliation_elem is not None:
            emails = re.findall(EMAIL_REGEX, affiliation_elem.text)
            if emails:
                paper_details["Corresponding Author Email"] = emails[0]

    if debug:
        print(f"Fetched paper {paper_id}: {paper_details}")

    return paper_details if paper_details["Company Affiliations"] else None

def save_results_to_csv(results, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {filename}")

def print_results(results):
    for paper in results:
        print("\n" + "="*80)
        print(f"PubMed ID: {paper['PubmedID']}")
        print(f"Title: {paper['Title']}")
        print(f"Publication Date: {paper['Publication Date']}")
        print(f"Non-academic Authors: {', '.join(paper['Non-academic Authors']) if paper['Non-academic Authors'] else 'N/A'}")
        print(f"Company Affiliations: {', '.join(paper['Company Affiliations']) if paper['Company Affiliations'] else 'N/A'}")
        print(f"Corresponding Author Email: {paper['Corresponding Author Email'] if paper['Corresponding Author Email'] else 'N/A'}")
        print("="*80)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed with company-affiliated authors.",
        epilog="""
Examples:
  1️⃣ Run interactively:
     python pubmed_fetcher.py
     
  2️⃣ Fetch papers using a query:
     python pubmed_fetcher.py "COVID-19[Title] AND Nature[Journal]"
     
  3️⃣ Save results to a CSV file:
     python pubmed_fetcher.py "COVID-19[Title] AND Nature[Journal]" -f results.csv
     
  4️⃣ Enable debug mode:
     python pubmed_fetcher.py "COVID-19[Title] AND Nature[Journal]" -d
     
  5️⃣ Display this help message:
     python pubmed_fetcher.py -h
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("query", nargs="?", help="PubMed search query (optional, will prompt if not provided)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file (default: print to console)")
    
    args = parser.parse_args()

    print("   -h or --help  : Display usage instructions")
    print("   -d or --debug : Print debug information during execution")
    print("   -f or --file  : Save results to a CSV file instead of printing\n")

    if not args.query:
        args.query = input("Enter your PubMed query: ").strip()

    paper_ids = fetch_pubmed_papers(args.query, debug=args.debug)

    if not paper_ids:
        print("No papers found for the given query.")
        return

    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        fetched_details = list(executor.map(lambda pid: fetch_paper_details(pid, args.debug), paper_ids))

    results = [paper for paper in fetched_details if paper is not None]

    if not results:
        print("No relevant papers found.")
        return

    if args.file:
        save_results_to_csv(results, args.file)
    else:
        print_results(results)

if __name__ == "__main__":
    main()
