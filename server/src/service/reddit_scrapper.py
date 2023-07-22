import asyncio
import httpx
from typing import Dict, List, Any

EXCLUDED_BOTS: List[str] = ["AutoModerator", "RemindMeBot"]
HEADERS: Dict[str, str] = {'User-Agent': 'My User Agent 1.0'}

async def make_request(session: httpx.AsyncClient, url: str) -> Dict[str, Any]:
    """Make a request to a given url and return the JSON response."""
    response = await session.get(url, headers=HEADERS)
    response.raise_for_status()  # Raises an exception for non-200 status codes
    return response.json()

async def fetch_posts(session: httpx.AsyncClient, subreddit: str, num_posts: int = 10, sort_by: str = "top", time_frame: str = "day") -> List[Dict[str, Any]]:
    """Fetch posts from a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort_by}.json?t={time_frame}&limit={num_posts}" if sort_by == 'top' else f"https://www.reddit.com/r/{subreddit}/{sort_by}.json?limit={num_posts}"
    response = await make_request(session, url)

    posts = []
    for post in response['data']['children']:
        data = post["data"]
        if data["author"] not in EXCLUDED_BOTS:
            posts.append(
                {
                    "post_id": data["id"],
                    "title": data["title"],
                    "body": data["selftext"],
                    "upvote_ratio": data["upvote_ratio"],
                }
            )
    return posts

async def fetch_post_comments(session: httpx.AsyncClient, post_id: str, sort_by: str = "confidence", limit: int = 10) -> List[str]:
    """Fetch comments of a post."""
    url = f"https://www.reddit.com/comments/{post_id}.json?sort={sort_by}&limit={limit}"
    response = await make_request(session, url)

    comments = []
    for comment in response[1]["data"]["children"]:
        if comment["kind"] == "t1" and comment["data"]["author"] not in EXCLUDED_BOTS:
            comments.append(comment["data"]["body"])
    return comments

async def fetch_subreddit_posts(session: httpx.AsyncClient, subreddit: str) -> List[Dict[str, Any]]:
    """Main function to fetch posts and comments."""
    posts = await fetch_posts(session, subreddit)
    tasks = [fetch_post_comments(session, post["post_id"]) for post in posts]
    comments_list = await asyncio.gather(*tasks)

    for post, comments in zip(posts, comments_list):
        post["comments"] = comments

    return posts

# Usage
async def main_data_fetcher(subreddit) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as session:
        data = await fetch_subreddit_posts(session, subreddit)
        return data

