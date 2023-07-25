from sqlalchemy.orm import declarative_base, DeclarativeBase
from sqlalchemy import (
    Column, Text, BigInteger, Identity, CheckConstraint, Date, text, Enum
)

from sqlalchemy.dialects.postgresql import JSONB

from src.database import engine

Base: DeclarativeBase = declarative_base()


class Sentiment(Base):

    __tablename__ = "sentiments"

    id: BigInteger = Column(
        BigInteger,
        Identity(always=True),
        primary_key=True
    )

    subreddit: Text = Column(
        Text,
        CheckConstraint(text("subreddit ~ '^[A-Za-z0-9_]{1,18}$'")),
        nullable=False
    )

    sentiment: Enum = Column(
        Enum("positive", "negative", "neutral", name="sentiment_enum"),
        nullable=False
    )
    reasoning: Text = Column(
        Text,
        nullable=False
    )

    date: Date = Column(
        Date,
        default=text("(current_date AT TIME ZONE 'UTC')::date")
    )

    posts_data: JSONB = Column(JSONB, nullable=False)


Base.metadata.create_all(engine)
