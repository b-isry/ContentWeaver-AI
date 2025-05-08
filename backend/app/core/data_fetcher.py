import feedparser
import requests
from bs4 import BeautifulSoup
import time
import uuid
from typing import List, Dict, Any

def scrape_article_content(url: str) -> str | None: 
    try:
        headers = {'User-Agent': 'ContentWeaverBot/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        main_content = soup.find('article') or soup.find('main')
        if main_content:
            return ' '.join(main_content.stripped_strings)[:5000]
        paragraphs = soup.find_all('p')
        return ' '.join(p.get_text() for p in paragraphs)[:5000]
    except Exception as e:
        print(f"Scraping Error for {url}: {e}")
        return None

def fetch_articles_from_feeds(feed_urls: List[str], scrape_content: bool = False) -> List[Dict[str, Any]]:
    articles = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                article_data = {
                    "id": str(uuid.uuid4()),
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "N/A"),
                    "summary_from_feed": entry.get("summary", ""),
                    "content": entry.get("content", [{"value": entry.get("summary", "")}])[0].get("value", entry.get("summary", ""))
                }
                if scrape_content:
                    print(f"Attempting to scrape: {article_data['link']}")
                    full_content = scrape_article_content(article_data['link'])
                    if full_content:
                        article_data['content'] = full_content
                    time.sleep(1) 

                articles.append(article_data)
            print(f"Fetched {len(feed.entries)} entries from {url}")
            time.sleep(0.5) 
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")
    return articles
