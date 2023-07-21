import requests

EXCLUDED_BOTS: list[str] = ["AutoModerator", "RemindMeBot"]
HEADERS = {'User-Agent': 'My User Agent 1.0'}


def fetch_subreddit_posts(subreddit: str, num_posts: int = 10,
                          sort_by: str = "top", time_frame: str = "day"):
    if sort_by == 'top':
        response = requests.get(
            f"https://www.reddit.com/r/{subreddit}/{sort_by}.json?t={time_frame}&limit={num_posts}",
            headers=HEADERS)
    else:
        response = requests.get(
            f"https://www.reddit.com/r/{subreddit}/{sort_by}.json?limit={num_posts}",
            headers=HEADERS)

    posts: list[dict] = []

    if response.status_code == 200:

        for post in response.json()['data']['children']:
            data: dict = post["data"]
            if data["author"] not in EXCLUDED_BOTS:
                posts.append(
                    {
                        "posts_id": data["id"],
                        "title": data["title"],
                        "body": data["selftext"],
                        "upvote_ratio": data["upvote_ratio"],
                        "comments": list[str]
                    }
                )
        return posts
    else:
        return f"Unable to retrieve posts, Status code: {response.status_code}"


print(fetch_subreddit_posts("india", sort_by="hot"))
