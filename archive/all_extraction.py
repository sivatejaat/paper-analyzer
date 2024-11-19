import os
import requests
from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

OUTPUT_DIR = "pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_pubmed_url(url):
    """Extract the base URL up to the PubMed ID."""
    parsed_url = urlparse(url)
    clean_url = f"https://{parsed_url.netloc}{parsed_url.path}"
    return clean_url

def download_pdf(url, output_path):
    """Download the PDF from the provided URL and save it."""
    response = requests.get(url, headers=HEADERS, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Downloaded: {output_path}")
    else:
        print(f"Failed to download PDF: {url}")

def get_full_text_link(pubmed_url):
    """Extract the full-text link from the PubMed page."""
    session = HTMLSession()
    response = session.get(pubmed_url, headers=HEADERS)
    if response.status_code == 200:
        full_text_section = response.html.find('div.full-text-links', first=True)
        if full_text_section:
            full_text_link = full_text_section.find('a', first=True)
            if full_text_link:
                return full_text_link.attrs['href']
    print(f"No full-text section found on PubMed page: {pubmed_url}")
    return None

def handle_pmc(url):
    """Download PDFs from PMC links."""
    session = HTMLSession()
    response = session.get(url, headers=HEADERS)
    if response.status_code == 200:
        pdf_link = response.html.find('a.pdf-link', first=True)
        if pdf_link:
            pdf_url = pdf_link.attrs['href']
            if not pdf_url.startswith('http'):
                pdf_url = urljoin(url, pdf_url)
            output_path = os.path.join(OUTPUT_DIR, os.path.basename(pdf_url))
            download_pdf(pdf_url, output_path)
        else:
            print(f"No PDF link found on PMC page: {url}")
    else:
        print(f"Failed to fetch PMC page: {url}")

def handle_ash_publications(url):
    """Handle ASH Publications pages specifically."""
    session = HTMLSession()
    response = session.get(url, headers=HEADERS)
    if response.status_code == 200:
        # Look for the PDF button
        pdf_link = response.html.find('a[href$=".pdf"]', first=True)
        if pdf_link:
            pdf_url = pdf_link.attrs['href']
            if not pdf_url.startswith('http'):
                pdf_url = urljoin(url, pdf_url)
            output_path = os.path.join(OUTPUT_DIR, os.path.basename(pdf_url))
            download_pdf(pdf_url, output_path)
        else:
            print(f"No PDF link found on ASH Publications page: {url}")
    else:
        print(f"Failed to fetch ASH Publications page: {url}")

def handle_publisher(url):
    """Scrape publisher site for PDF."""
    parsed_url = urlparse(url)
    if "ashpublications.org" in parsed_url.netloc:
        handle_ash_publications(url)
    else:
        print(f"Unhandled publisher domain: {parsed_url.netloc}")

def process_pubmed_link(pubmed_url):
    """Process each PubMed link."""
    clean_url = clean_pubmed_url(pubmed_url)
    print(f"Processing: {clean_url}")
    full_text_url = get_full_text_link(clean_url)
    if full_text_url:
        if "ncbi.nlm.nih.gov/pmc" in full_text_url:
            handle_pmc(full_text_url)
        else:
            handle_publisher(full_text_url)
    else:
        print(f"Skipping PubMed link: {clean_url}")

def main():
    input_file = "data/URL/urls.txt"  # Replace with your input file
    with open(input_file, "r") as file:
        links = file.readlines()

    for link in links:
        link = link.strip()
        if link:
            process_pubmed_link(link)

if __name__ == "__main__":
    main()
