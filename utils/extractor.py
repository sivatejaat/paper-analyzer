import os
import pdfplumber
import pandas as pd
from config import TABLES_PATH
import logger
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: Extracted text.
    """
    try:
        logger.info(f"Starting text extraction for {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages):
                logger.info(f"Extracting text from page {i + 1}/{len(pdf.pages)}")
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if not text.strip():
                raise Exception("No extractable text found in the PDF.")
            return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_main_table(pdf_path, output_filename):
    """
    Extracts the main results table from a PDF and saves it as a CSV.
    Args:
        pdf_path (str): Path to the PDF file.
        output_filename (str): Output filename for the CSV.
    Returns:
        str: Path to the saved CSV file or None if no table is found.
    """
    os.makedirs(TABLES_PATH, exist_ok=True)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            tables = []
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)

            if tables:
                # Combine all tables into a single DataFrame
                all_tables = []
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)
                
                if all_tables:
                    combined_table = pd.concat(all_tables, ignore_index=True)
                    output_path = os.path.join(TABLES_PATH, output_filename)
                    combined_table.to_csv(output_path, index=False)
                    return output_path
        return None
    except Exception as e:
        raise Exception(f"Error extracting table from PDF: {str(e)}")
