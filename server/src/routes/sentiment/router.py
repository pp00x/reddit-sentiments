from fastapi import APIRouter, BackgroundTasks
from .models import Sentiment
from datetime import datetime
from src.database import Session
from src.service.sentiment_analyzer import analyze_and_store

sentiment_router: APIRouter = APIRouter()


@sentiment_router.get("/sentiment/r/{subreddit}")
async def get_sentiment(subreddit: str, background_tasks: BackgroundTasks):
    with Session() as session:
        sentiment_analysis = session.query(Sentiment).filter_by(subreddit=subreddit, date=datetime.utcnow().date()).first()
        if sentiment_analysis:
            print(sentiment_analysis)
            return sentiment_analysis
        else:
            background_tasks.add_task(analyze_and_store, session, Sentiment, subreddit)
            return ("Sentiment analysis not found, generating analysis now, try again in 5 seconds.")
