import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_article(text):
    prompt = f"""
    Summarize the following article in 2-3 paragraphs. Then extract relevant hashtags and trending keywords:\n\n
    Article:\n{text}\n
    Output format:\n
    Summary:\n<summary>\n\n
    Hashtags:\n#UAV #Drones\n
    Keywords:\nDrone tech, DGCA
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=600
    )

    return response['choices'][0]['message']['content']
