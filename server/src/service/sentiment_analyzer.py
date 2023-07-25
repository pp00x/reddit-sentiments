from dotenv import load_dotenv
import openai
from os import environ
from typing import Dict, List, Any
import json
from datetime import datetime
from .reddit_scrapper import main_data_fetcher


load_dotenv()

openai.api_key = environ["OPENAI_API_KEY"]

PROMPT = """
Analyze the overall sentiment of a subreddit based on data that will be provided by the user. The provided data is in the following JSON format: 

Posts sorted by top for the day:
[posts] 

Post id:
{{post_id}}

Post title: 
{{title}}

Post body:
{{body}}  

Post upvote ratio:
{{upvote_ratio}}

Post comments sorted by confidence:  
[post_comments]

Based on each post's data, please respond with:

- The overall sentiment of the subreddit (positive, negative or neutral)
- Detailed reasoning for why you categorized the sentiment that way
- Respond in JSON format as follows:",

    {
      "sentiment": "sentiment", 
      "reasoning": "reasoning",
    }
"""


async def analyze_data(data: List[Dict[str, Any]]):
    messages = [
        {"role": "system", "content": f"{PROMPT}"},
        {"role": "user", "content": f"{str(data)}"}
    ]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=messages)
    print(completion)
    return completion["choices"][0]["message"]["content"]


async def analyze_and_store(session, model_class, subreddit) -> None:
    posts_data = await main_data_fetcher(subreddit)
    analysis = json.loads(await analyze_data(posts_data), strict=False)
    sentiment_data = model_class()
    sentiment_data.subreddit = subreddit
    sentiment_data.sentiment = analysis["sentiment"]
    sentiment_data.reasoning = analysis["reasoning"]
    sentiment_data.date = datetime.utcnow().date()
    sentiment_data.posts_data = posts_data
    session.add(sentiment_data)
    session.commit()
