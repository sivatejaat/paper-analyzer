import os
import requests
from metapub import FindIt

# Function to fetch metadata and PDF URL using DOI
def fetch_paper(doi):
    base_url = "https://api.crossref.org/works/"
    try:
        response = requests.get(base_url + doi, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Extract title and URL
        title = data["message"]["title"][0]
        pdf_url = data["message"].get("link", [{}])[0].get("URL", "")
        return title, pdf_url
    except Exception as e:
        print(f"Error fetching DOI {doi}: {e}")
        return None, None

# Function to download PDF
def download_pdf(url, title, output_dir="papers"):
    if not url:
        print(f"No PDF URL found for {title}.")
        return
    try:
        os.makedirs(output_dir, exist_ok=True)
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()
        file_path = os.path.join(output_dir, f"{title}.pdf")
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {title}")
    except Exception as e:
        print(f"Failed to download {title}: {e}")

# Read the URLs/PMIDs from the input file
input_file = 'data/URL/input_file.txt'  # Replace with your file path
with open(input_file, 'r') as file:
    pmids = [line.strip() for line in file]

# Create output directory for papers
output_dir = "downloaded_papers"
os.makedirs(output_dir, exist_ok=True)

# Process each PMID
for pmid in pmids:
    try:
        # Find DOI using metapub
        src = FindIt(pmid)
        doi = src.doi
        if not doi:
            print(f"No DOI found for PMID: {pmid}")
            continue

        print(f"PMID: {pmid}")
        print(f"DOI: {doi}")
        
        # Fetch metadata and PDF URL
        title, pdf_url = fetch_paper(doi)
        if title and pdf_url:
            # Download the paper
            download_pdf(pdf_url, title, output_dir)
        else:
            print(f"Could not fetch metadata or PDF URL for DOI: {doi}")
    except Exception as e:
        print(f"Error processing PMID {pmid}: {e}")
