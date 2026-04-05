import requests
import time
import os
import json
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

hacker_news_url = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}
MAX_PER_CATEGORY = 25
LIMIT = 500
# Setup a robust session with retries
# The purpose of this code is to create a persistent and 
# resilient network connection for making API requests.
# Instead of opening a new connection for every single request, 
# it uses a Session object to improve performance and adds a "safety net" 
# for handling network errors.

def get_session():
    session = requests.Session()
    # Retry strategy: wait 1s, 2s, 4s... on failure
    retries = Retry(
        total=5, 
        backoff_factor=1, 
        status_forcelist=[429, 500, 502, 503, 504]
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.headers.update(HEADERS)
    return session

session = get_session()

KEYWORDS = {
    "technology": ["ai", "software", "programming", "developer", "github", "open source"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def fetch_top_ids(limit):
    try:
        # Use session instead of requests
        res = session.get(f"{hacker_news_url}/topstories.json", timeout=15)
        res.raise_for_status()
        return res.json()[:limit]
    except Exception as e:
        print(f"Error fetching top IDs: {e}")
        return []

def fetch_story(story_id):
    try:
        res = session.get(f"{hacker_news_url}/item/{story_id}.json", timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None

# This method identifies keywords within the title and associates them 
# with the corresponding story ID
def categorize(title):
    title_lower = title.lower()
    for category, keywords in KEYWORDS.items():
        if any(kword in title_lower for kword in keywords):
            return category
    return "general"

# Aggregates story data into keyword-based categories 
# and persists the collection to disk.
def fetch_story_IDs(id_list):
    collected = {key: [] for key in KEYWORDS}
    seen_ids = set()
    
    print(f"Starting data collection for {len(id_list)} IDs...")

    for story_id in id_list:
        # Check if we already filled all categories to stop early
        if all(len(collected[c]) >= MAX_PER_CATEGORY for c in KEYWORDS):
            break

        story = fetch_story(story_id)
        
        # Add a tiny sleep to be polite to the server and prevent SSL drops
        time.sleep(0.1) 

        if not story or "title" not in story or story_id in seen_ids:
            continue

        category = categorize(story["title"])
        
        if category != 'general' and len(collected[category]) < MAX_PER_CATEGORY:
            record = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "category": category,
                "author": story.get("by", "unknown")
            }
            collected[category].append(record)
            seen_ids.add(story_id)
            

    # Final logic for saving
    all_stories = [item for sublist in collected.values() for item in sublist]
    os.makedirs("data", exist_ok=True)
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Storing file name as Json format
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_stories, f, indent=2)

    # Print the results of all stories, filename 
    # and summary of category wise stoies
    print(f"Collected {len(all_stories)} stories")
    print(f"Saved to {filename}")
    print("\nSummary Results:")
    for cat, items in collected.items():
        print(f"{cat}: {len(items)}")

# Execution
top_ids = fetch_top_ids(LIMIT)
if top_ids:
    fetch_story_IDs(top_ids)