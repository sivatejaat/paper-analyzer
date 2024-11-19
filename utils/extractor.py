import os
import pdfplumber
import pandas as pd
from config import TABLES_PATH
from utils.logger import setup_logger  # Use setup_logger to configure logging

logger = setup_logger()  # Initialize logger

def extract_text_from_pdf(pdf_path):
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
                logger.warning(f"No extractable text found in {pdf_path}.")
                return ""
            return text
    except Exception as e:
        logger.error(f"Error extracting text from {pdf_path}: {str(e)}")  # Correct usage
        raise e




def extract_main_table(pdf_path, output_filename):
    os.makedirs(TABLES_PATH, exist_ok=True)
    try:
        logger.info(f"Starting table extraction for {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            tables = []
            for i, page in enumerate(pdf.pages):
                logger.info(f"Checking page {i + 1}/{len(pdf.pages)} for tables")
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)

            if tables:
                all_tables = []
                for idx, table in enumerate(tables):
                    try:
                        if len(table) > 1:  # Ensure table has header and data
                            df = pd.DataFrame(table[1:], columns=table[0])
                            all_tables.append(df)
                    except Exception as e:
                        logger.warning(f"Error processing table on page {idx + 1}: {str(e)}")

                if all_tables:
                    combined_table = pd.concat(all_tables, ignore_index=True)
                    output_path = os.path.join(TABLES_PATH, output_filename)
                    combined_table.to_csv(output_path, index=False)
                    logger.info(f"Table saved to {output_path}")
                    return output_path

            logger.warning(f"No tables found in {pdf_path}.")
            return None
    except Exception as e:
        logger.error(f"Error extracting table from {pdf_path}: {str(e)}")  # Correct usage
        return None

