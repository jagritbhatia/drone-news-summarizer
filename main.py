import os
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GEN_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not GEN_API_KEY or not NEWS_API_KEY:
    raise Exception("API keys not found. Please check your .env file.")

# Initialize Gemini client, picks up API key from environment variable or pass explicitly
client = genai.Client(api_key=GEN_API_KEY)

def fetch_drone_news():
    url = (
        "https://newsapi.org/v2/everything?"
        "q=drone OR UAV OR DGCA&"
        "language=en&"
        "sortBy=publishedAt&"
        "pageSize=5&"
        f"apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    if data.get("status") != "ok":
        raise Exception("Failed to fetch news: " + str(data))
    articles = data.get("articles", [])
    results = []
    for article in articles:
        results.append({
            "title": article.get("title"),
            "link": article.get("url"),
            "date": article.get("publishedAt"),
            "image": article.get("urlToImage"),
            "content": article.get("content") or article.get("description") or ""
        })
    return results

def summarize_article(article_text):
    if not article_text.strip():
        return "No content available to summarize.\n\nHashtags: #Drones #UAV #Tech"

    prompt = (
        "Summarize the following drone industry news article into 2-3 concise paragraphs. "
        "Then provide 3 relevant hashtags.\n\n"
        f"Article Text:\n{article_text}\n\n"
        "Summary and hashtags:"
    )

    # Create a chat session with the model gemini-2.5-flash
    chat = client.chats.create(
        model="gemini-2.5-flash",
        history=[],
    )
    # Send the prompt message wrapped in Part
    response = chat.send_message(types.Part(text=prompt))
    
    return response.text.strip()

def format_social_post(summary_text, article):
    lines = summary_text.split("\n")
    hashtags = ""
    summary_lines = []
    for line in lines:
        if line.lower().startswith("hashtags:"):
            hashtags = line.split(":", 1)[1].strip()
        else:
            summary_lines.append(line)
    summary = " ".join(summary_lines).strip()

    post = (
        f"🚀 Latest Drone News Update 🚁\n\n"
        f"{summary}\n\n"
        f"{hashtags}\n\n"
        f"Read more: {article['link']}\n"
        f"#DroneNews #UAV #Tech"
    )
    return post

def main():
    print("Fetching latest drone news...")
    articles = fetch_drone_news()
    print(f"Found {len(articles)} articles.\n")

    for i, article in enumerate(articles, 1):
        print(f"Article {i}: {article['title']}\nPublished on: {article['date']}")
        print(f"Link: {article['link']}")
        print(f"Image URL: {article['image']}\n")

        summary = summarize_article(article['content'])
        print("Summary & Hashtags:")
        print(summary)

        post = format_social_post(summary, article)
        print("\nSocial Media Post:\n")
        print(post)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
