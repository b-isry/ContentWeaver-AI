from pydantic import BaseModel, HttpUrl
from typing import List, Optional

# This model defines the structure of the data
# the frontend will send when requesting a newsletter.
class UserPreferencesRequest(BaseModel):
    keywords: List[str]  # A list of strings, e.g., ["AI", "LLM"]
    rss_feed_urls: List[HttpUrl] # A list of valid HTTP/HTTPS URLs
    preferred_tone: Optional[str] = "informative" # An optional string, defaults to "informative"

    # Example of how this data might look in JSON:
    # {
    #   "keywords": ["AI in healthcare", "GPT-4"],
    #   "rss_feed_urls": ["http://somefeed.com/rss", "https://another.com/feed.xml"],
    #   "preferred_tone": "enthusiastic"
    # }

# This model defines the structure of the data
# the backend will send back as a response.
class NewsletterResponse(BaseModel):
    user_id: Optional[str] = None # Example, might not need this for now
    newsletter_content: str # The main generated newsletter text
    # You could add more fields later, like a list of sources used.