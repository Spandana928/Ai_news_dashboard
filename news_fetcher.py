import requests
from bs4 import BeautifulSoup

def fetch_news(topic="technology", page_size=10):
    """
    Fetches news from Bing News search instead of Google News.
    Returns a list of articles with title, description, and URL.
    """
    articles = []
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.bing.com/news/search?q={topic}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("Error fetching news:", response.status_code)
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        # Each news card container
        news_cards = soup.select("div.news-card, div.t_s, div.newsitem")

        # If none found, fall back to headline selectors
        if not news_cards:
            news_cards = soup.select("a.title")

        for card in news_cards[:page_size]:
            title_tag = card.find("a")
            desc_tag = card.find("div", class_="snippet") or card.find("p")
            link = title_tag["href"] if title_tag and title_tag.has_attr("href") else "#"

            title = title_tag.get_text(strip=True) if title_tag else "No title"
            description = desc_tag.get_text(strip=True) if desc_tag else title

            articles.append({
                "title": title,
                "description": description,
                "url": link
            })

        if not articles:
            print("⚠️ No articles parsed. Check Bing layout.")
        else:
            print(f"✅ Fetched {len(articles)} articles for topic '{topic}'")

        return articles

    except Exception as e:
        print("Error in fetch_news:", e)
        return []






