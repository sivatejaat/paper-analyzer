import re

# File containing the URLs
file_path = "urls.txt"

# Read URLs from the file
with open(file_path, "r") as file:
    pubmed_urls = [line.strip() for line in file if line.strip()]  # Remove whitespace and empty lines

# Regular expression to extract the PMID from the URL
pmid_pattern = r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)/"

# Extract PMIDs
pmids = [re.search(pmid_pattern, url).group(1) for url in pubmed_urls if re.search(pmid_pattern, url)]

# Save PMIDs to a text file
with open("input_file.txt", "w") as file:
    file.write("\n".join(pmids))

print(f"Extracted {len(pmids)} PMIDs and saved to 'input_file.txt'.")
