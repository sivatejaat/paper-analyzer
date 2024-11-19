from metapub import FindIt
import requests
import os
from time import sleep

# Initialize success and failure logs
successes = []
failures = []

# Function to download paper using DOI or URL
def download_paper(pmid, doi=None, url=None):
    if url:  # Use the URL if available
        try:
            print(f"Attempting to download paper using URL: {url}")
            response = requests.get(url, stream=True)
            if response.headers.get('Content-Type') == 'application/pdf':
                os.makedirs('data/papers', exist_ok=True)  # Ensure output directory exists
                filename = f"data/papers/paper_{pmid}.pdf"
                with open(filename, 'wb') as pdf_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        pdf_file.write(chunk)
                print(f"Downloaded: {filename}")
                successes.append(pmid)
                return
            else:
                print(f"Failed to download from URL: {url}. Received non-PDF content.")
        except Exception as e:
            print(f"Error downloading paper using URL for PMID: {pmid}, Error: {e}")

    if doi:  # Fallback to using SciHub with DOI
        mirrors = [
            "https://sci-hub.st",
            "https://sci-hub.ru",
            "https://sci-hub.mksa.top"
        ]
        for mirror in mirrors:
            scihub_url = f"{mirror}/{doi}"
            try:
                print(f"Attempting to download paper using DOI: {doi} from {scihub_url}")
                response = requests.get(scihub_url, timeout=10)
                if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
                    os.makedirs('data/papers', exist_ok=True)
                    filename = f"data/papers/paper_{pmid}.pdf"
                    with open(filename, 'wb') as pdf_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            pdf_file.write(chunk)
                    print(f"Downloaded: {filename}")
                    successes.append(pmid)
                    return
                else:
                    print(f"Failed to download from DOI: {doi} at {mirror} (Status Code: {response.status_code})")
            except Exception as e:
                print(f"Error accessing {mirror} for DOI: {doi}. Error: {e}")
            sleep(2)  # Delay to avoid rate-limiting

    print(f"Failed to download paper for PMID: {pmid}")
    failures.append(pmid)

# Read PMIDs from input file
with open('data/URL/input_file.txt', 'r') as file:
    pmids = [line.strip() for line in file]

# Log output to a file
output_file = 'data/URL/output_log.txt'
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as out:
    for pmid in pmids:
        try:
            src = FindIt(pmid)
            doi = src.doi
            url = src.url

            # Log DOI and URL
            out.write(f"PMID: {pmid}\nDOI: {doi}\nURL: {url}\n\n")
            print(f"PMID: {pmid}, DOI: {doi}, URL: {url}")

            # Download the paper using URL or DOI
            download_paper(pmid, doi=doi, url=url)
        except Exception as e:
            out.write(f"Error processing PMID {pmid}: {e}\n\n")
            print(f"Error processing PMID {pmid}: {e}")

# Log successes and failures
with open('data/URL/successes.txt', 'w') as success_file:
    success_file.write("\n".join(successes))
    print(f"Successes logged: {len(successes)} papers downloaded.")

with open('data/URL/failures.txt', 'w') as failure_file:
    failure_file.write("\n".join(failures))
    print(f"Failures logged: {len(failures)} papers failed.")
