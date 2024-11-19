
# PubMed Paper Analyzer

This application processes scientific papers in PDF format to:
- Extract text from all PDFs in the `papers` folder.
- Generate summaries using OpenAI GPT models.
- Extract tables of results (if available).

Summaries and tables are saved in designated output folders for further use.

---

## Features

1. **Batch Processing**: Automatically processes all PDFs in the `papers` folder.
2. **Summarization**: Creates concise summaries for scientific papers.
3. **Table Extraction**: Extracts results tables into CSV files (if tables exist in the PDF).
4. **Output Management**: Saves results in organized folders (`summaries/` and `tables/`).

---

## Folder Structure

```plaintext
pubmed_analyzer/
    ├── app.py                 # Main Flask application
    ├── utils/                 # Utility functions
    │   ├── summarizer.py      # Summarization logic
    │   ├── extractor.py       # PDF text and table extraction
    │   └── logger.py          # Logging utility
    ├── data/                  # Input and output folders
    │   ├── papers/            # Place input PDFs here
    │   ├── summaries/         # Summaries will be saved here
    │   └── tables/            # Tables will be saved here
    └── config.py              # Configuration for paths and API keys
```

---

## Requirements

### 1. Install Dependencies
Ensure you have Python 3.8+ installed. Install required libraries using:

```bash
pip install -r requirements.txt
```

**`requirements.txt`**:
```plaintext
flask
openai==0.28.0
pdfplumber
pandas
```

### 2. Set OpenAI API Key
Update your OpenAI API key in `config.py`:

```python
OPENAI_API_KEY = "your_openai_api_key_here"
```

---

## How to Run the Code

### 1. Place Input PDFs
- Add all the PDFs you want to process into the `data/papers` folder.

### 2. Start the Flask Server
Run the server using the command:

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000`.

### 3. Process All PDFs
You can process all the PDFs by sending a POST request to the `/process_all` endpoint.

#### Using Postman:
1. Open Postman and create a new request.
2. **Method**: `POST`
3. **URL**: `http://127.0.0.1:5000/process_all`
4. **Headers**:
   - Key: `Content-Type`
   - Value: `application/json`
5. Leave the body empty.
6. Click **Send**.

#### Using `curl`:
```bash
curl -X POST http://127.0.0.1:5000/process_all
```

---

## Output Files

### 1. Summaries
- Saved as `.txt` files in the `data/summaries/` folder.
- File names match the input PDF names (e.g., `sample-paper.txt`).

### 2. Tables
- Saved as `.csv` files in the `data/tables/` folder.
- File names match the input PDF names (e.g., `sample-paper.csv`).
- If no tables are found, a warning is logged.

---

## Code Explanation

### 1. `app.py`
The main Flask application:
- **`/process_all`**: Processes all PDFs in the `papers` folder.
    - Extracts text using `extract_text_from_pdf`.
    - Summarizes text in chunks using `summarize_text_in_chunks`.
    - Extracts tables using `extract_main_table`.
    - Saves summaries and tables in their respective folders.

### 2. `utils/summarizer.py`
Handles text summarization using OpenAI GPT:
- Splits large text into smaller chunks to avoid exceeding token limits.
- Combines chunk summaries into a single output.

### 3. `utils/extractor.py`
Processes PDFs:
- **Text Extraction**: Extracts text from PDFs using `pdfplumber`.
- **Table Extraction**: Extracts tables and combines them into CSV files.

### 4. `utils/logger.py`
Provides logging for debugging and progress tracking.

### 5. `config.py`
Configuration file for:
- File paths.
- OpenAI API key.

---

## Example Response

```json
{
    "processed_papers": [
        {
            "filename": "sample-paper.pdf",
            "summary_path": "data/summaries/sample-paper.txt",
            "table_path": "data/tables/sample-paper.csv"
        },
        {
            "filename": "another-paper.pdf",
            "summary_path": "data/summaries/another-paper.txt",
            "table_path": "No table found"
        }
    ]
}
```

---

## Known Limitations

1. **Non-Standard PDFs**:
   - Scanned PDFs may require OCR for text extraction.
2. **Large PDFs**:
   - Processing may take time for PDFs with extensive content.
3. **Table Detection**:
   - Tables spanning multiple pages might not be extracted perfectly.

---

Let me know if you have any issues running the application!
