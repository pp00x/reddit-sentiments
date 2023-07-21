from fastapi import FastAPI
from .routes.sentiment.router import sentiment_router

app: FastAPI = FastAPI()

app.include_router(sentiment_router)