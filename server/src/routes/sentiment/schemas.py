from pydantic import BaseModel
from typing import List


class AnalysisResponse(BaseModel):
    id: int
    subreddit: str
    sentiment: str
    reasoning: str
    date: str
    posts_data: List
