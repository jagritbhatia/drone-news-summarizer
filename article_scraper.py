from newspaper import Article

def extract_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "image": article.top_image
        }
    except Exception as e:
        print(f"⚠️ Failed to extract article from {url}: {e}")
        return {"title": "", "text": "", "image": "", "error": str(e)}
