from .env_vars import REDIS_URL
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from .routes.sentiment.router import sentiment_router
from redis import asyncio as aioredis

app: FastAPI = FastAPI()


@app.on_event("startup")
async def startup():
    redis_client = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_client)


app.include_router(sentiment_router)
