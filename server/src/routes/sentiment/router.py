from fastapi import APIRouter
from .models import Sentiment
from src.database import Session

sentiment_router: APIRouter = APIRouter()


@sentiment_router.get("/sentiment/r/{subreddit}")
async def get_sentiment(subreddit: str):
    return subreddit
