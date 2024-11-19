import openai
from config import OPENAI_API_KEY

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
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant summarizing scientific papers."},
                {"role": "user", "content": f"Summarize the following text into approximately 250 words:\n\n{text}"}
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
    
    Args:
        text (str): Text to summarize.
        chunk_size (int): Maximum number of tokens per chunk.
    
    Returns:
        str: Combined summary of all chunks.
    """
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []
    
    for chunk in chunks:
        try:
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
            raise Exception(f"Error summarizing text chunk: {str(e)}")
    
    return "\n\n".join(summaries)
