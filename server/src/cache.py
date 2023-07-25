import json
from src.env_vars import REDIS_URL
from src.database import class_mapper
from redis.asyncio import Redis
from datetime import date

redis_client: Redis = Redis.from_url(REDIS_URL, encoding="utf-8",
                                     decode_responses=True)


def date_json(obj):
    if isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")

async def cache_analysis(subreddit, sentiment_analysis):
    columns = class_mapper(sentiment_analysis.__class__).columns.keys()
    data = {column: getattr(sentiment_analysis, column) for column in columns}
    await redis_client.set(subreddit, json.dumps(data, default=date_json))


async def get_cached_analysis(subreddit):
    return json.loads(await redis_client.get(subreddit))
