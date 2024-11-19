from metapub import FindIt

# Read the PMIDs from the text file
with open('data/URL/input_file.txt', 'r') as file:
    pmids = [line.strip() for line in file]

# Process each PMID
for pmid in pmids:
    try:
        src = FindIt(pmid)
        print(f"PMID: {pmid}")
        print(f"DOI: {src.doi}")
        print(f"URL: {src.url}")
    except Exception as e:
        print(f"Error processing PMID {pmid}: {e}")
