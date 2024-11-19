from requests_html import HTMLSession
import requests
from requests.exceptions import ConnectionError

s = HTMLSession()

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

file = open('input_file.txt','r')
ids = file.readlines()

for pmc in ids:
    try:
        pmcid = pmc.strip()
        print(pmcid)
        base_url = 'https://pubmed.ncbi.nlm.nih.gov/'

        r = s.get(base_url+pmcid+'/',headers=headers,timeout=5)
        pdf_url = r.html.find('a.int-view',first=True).attrs['href']
        print(pdf_url)
    except ConnectionError as e:
        pass
        out = open('ConnectionError_pcmids.txt','a')
        out.write(pmcid+'\n')