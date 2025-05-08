from fastapi import FastAPI
from .models import UserPreferencesRequest, NewsletterResponse
from .core.data_fetcher import fetch_articles_from_feeds
from dotenv import load_dotenv
import os


load_dotenv()
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN environment variable not set.")

app = FastAPI()

@app.get("/")
async def read_root():

    return {"message": "Hello World from ContentWeaver AI Backend!"}

@app.get("/ping")
async def ping_pong():
    return {"ping": "pong!"}

@app.post("/generate-newsletter", response_model=NewsletterResponse)
async def create_newsletter(preferences: UserPreferencesRequest):
    print(f"Received preferences: {preferences.dict()}")

    if not preferences.keywords:
        raise HTTPException(status_code=400, detail="Keywords cannot be empty")
    if not preferences.rss_feed_urls:
        raise HTTPException(status_code=400, detail="RSS feed URLs cannot be empty")

    print("Fetching articles...")

    feed_urls_str = [str(url) for url in preferences.rss_feed_urls]
    fetched_articles = await asyncio.to_thread(fetch_articles_from_feeds, feed_urls_str, scrape_content=False)


    if not fetched_articles:
        print("No articles fetched.")

        return NewsletterResponse(newsletter_content="No articles found matching the feeds.")

    print(f"Fetched {len(fetched_articles)} articles.")

    # --- RAG and LLM logic will go here NEXT ---

    article_titles = [article.get('title', 'No Title') for article in fetched_articles]
    current_output = f"Based on keywords: {', '.join(preferences.keywords)}\n"
    current_output += f"Tone: {preferences.preferred_tone}\n"
    current_output += f"Fetched {len(fetched_articles)} articles:\n" + "\n".join(f"- {title}" for title in article_titles)
    current_output += "\n\n[RAG & LLM processing pending...]"

    return NewsletterResponse(newsletter_content=current_output)

import asyncio