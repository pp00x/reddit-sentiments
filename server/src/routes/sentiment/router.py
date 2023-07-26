import json
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_limiter.depends import RateLimiter
from src.routes.sentiment.models import Sentiment
from datetime import datetime
from src.database import Session
from src.service.sentiment_analyzer import analyze_and_store
from src.cache import cache_analysis, get_cached_analysis
from src.routes.sentiment.schemas import AnalysisResponse


sentiment_router: APIRouter = APIRouter()


@sentiment_router.get("/sentiment/r/{subreddit}", response_model=AnalysisResponse, dependencies=[Depends(RateLimiter(times=6, seconds=60))])
async def get_sentiment(subreddit: str, background_tasks: BackgroundTasks):
    cached_sentiment_analysis = await get_cached_analysis(f"{subreddit}{datetime.utcnow().date()}")
    if cached_sentiment_analysis:
        return json.loads(cached_sentiment_analysis)
    else:
        with Session() as session:
            sentiment_analysis = session.query(Sentiment).filter_by(subreddit=subreddit, date=datetime.utcnow().date()).first()
            if sentiment_analysis:
                background_tasks.add_task(cache_analysis, f"{subreddit}{datetime.utcnow().date()}", sentiment_analysis)
                return sentiment_analysis
            else:
                background_tasks.add_task(analyze_and_store, session, Sentiment, subreddit)
                return {"response": "Sentiment analysis not found, generating analysis now if subreddit exists, check in 5 seconds."}
