import openai
from config import OPENAI_API_KEY
from utils.logger import setup_logger  # Use setup_logger to configure logging

logger = setup_logger()  # Initialize logger

openai.api_key = OPENAI_API_KEY

def summarize_text(text):
    """
    Summarizes the given text using OpenAI's GPT API.
    Args:
        text (str): Text to summarize.
    Returns:
        str: Summary of the text.
    """
    try:
        logger.info("Starting text summarization")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant summarizing scientific papers."},
                {"role": "user", "content": f"Summarize the following text into approximately 250 words, focusing on the objectives, methods, and key findings:\n\n{text}"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise Exception(f"Error summarizing text: {str(e)}")


def summarize_text_in_chunks(text, chunk_size=3000):
    """
    Summarizes the given text by splitting it into chunks.
    """
    if not text.strip():
        return "No text available for summarization."

    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []
    
    for idx, chunk in enumerate(chunks):
        try:
            logger.info(f"Summarizing chunk {idx + 1}/{len(chunks)}")
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant summarizing scientific papers."},
                    {"role": "user", "content": f"Summarize the following text:\n\n{chunk}"}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            summaries.append(response['choices'][0]['message']['content'].strip())
        except Exception as e:
            logger.error(f"Error summarizing text chunk {idx + 1}: {str(e)}")
            summaries.append(f"Error summarizing chunk {idx + 1}.")
    
    return "\n\n".join(summaries).strip()
