import requests

def get_pmc_id_from_pmid(pmid):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
    params = {
        "dbfrom": "pubmed",  # Starting database (PubMed)
        "db": "pmc",        # Target database (PubMed Central)
        "id": pmid,         # PubMed ID
        "retmode": "json"   # Return mode (JSON for easy parsing)
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            # Extract PMC ID from the link set
            linksets = data.get("linksets", [])
            if linksets:
                pmc_ids = linksets[0].get("linksetdbs", [])[0].get("links", [])
                if pmc_ids:
                    return f"PMC{pmc_ids[0]}"  # PMC IDs are usually in this format
            return None
        except (KeyError, IndexError):
            print(f"Error parsing PMC ID for PMID {pmid}")
    else:
        print(f"Failed to fetch data for PMID {pmid}. Status code: {response.status_code}")
    return None

# Example usage
pmid = "37588232"  # Replace with your PMID
pmc_id = get_pmc_id_from_pmid(pmid)
if pmc_id:
    print(f"PMCID for PMID {pmid}: {pmc_id}")
else:
    print(f"No PMC ID found for PMID {pmid}")
