import os
from flask import Flask, jsonify
from utils.summarizer import summarize_text, summarize_text_in_chunks
from utils.extractor import extract_text_from_pdf, extract_main_table
# from utils.logger import setup_logger
from config import PAPERS_PATH, SUMMARIES_PATH, TABLES_PATH
import logging

app = Flask(__name__)
# logger = setup_logger()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("paper_analyzer")

@app.route('/process_all', methods=['POST'])
def process_all_papers():
    try:
        os.makedirs(SUMMARIES_PATH, exist_ok=True)
        os.makedirs(TABLES_PATH, exist_ok=True)

        processed_papers = []

        for filename in os.listdir(PAPERS_PATH):
            if filename.endswith(".pdf"):
                logger.info(f"Processing file: {filename}")
                pdf_path = os.path.join(PAPERS_PATH, filename)

                try:
                    # Extract text and summarize in chunks
                    text = extract_text_from_pdf(pdf_path)
                    summary = summarize_text_in_chunks(text, chunk_size=3000)

                    # Save summary
                    summary_path = os.path.join(SUMMARIES_PATH, filename.replace(".pdf", ".txt"))
                    with open(summary_path, "w") as summary_file:
                        summary_file.write(summary)

                    # Extract main results table
                    table_path = extract_main_table(pdf_path, filename.replace(".pdf", ".csv"))

                    processed_papers.append({
                        "filename": filename,
                        "summary_path": summary_path,
                        "table_path": table_path if table_path else "No table found"
                    })
                except Exception as e:
                    logger.error(f"Error processing {filename}: {str(e)}")  # Correct usage
                    processed_papers.append({
                        "filename": filename,
                        "error": str(e)
                    })

        return jsonify({"processed_papers": processed_papers}), 200
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")  # Correct usage
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(debug=True)
