import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_articles(keyword="drone technology"):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={keyword}&"
        f"sortBy=publishedAt&"
        f"pageSize=5&"
        f"language=en&"
        f"apiKey={NEWS_API_KEY}"
    )
    
    response = requests.get(url)
    data = response.json()

    articles = []
    if data.get("status") == "ok":
        for article in data["articles"]:
            articles.append({
                "title": article["title"],
                "link": article["url"],
                "published": article["publishedAt"]
            })
        print(f"✅ Fetched {len(articles)} articles.")
    else:
        print("❌ Failed to fetch articles:", data)
    
    return articles
