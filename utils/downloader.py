import os
import requests
from config import PAPERS_PATH

def download_paper(url, filename):
    os.makedirs(PAPERS_PATH, exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(PAPERS_PATH, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    raise Exception(f"Failed to download paper: {url}")
