from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from src.routes.sentiment.router import sentiment_router
from src.cache import redis_client

app: FastAPI = FastAPI()


@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis_client)


app.include_router(sentiment_router)
