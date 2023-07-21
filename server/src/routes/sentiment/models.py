from sqlalchemy.orm import declarative_base, DeclarativeBase
from sqlalchemy import (
    Column, Text, BigInteger, Identity, CheckConstraint, Date, text, Enum
)
from src.database import engine

Base: DeclarativeBase = declarative_base()


class Sentiment(Base):

    __tablename__ = "sentiment"

    id = Column(
        BigInteger,
        Identity(always=True),
        primary_key=True
    )

    subreddit = Column(
        Text,
        CheckConstraint(text("subreddit ~ '^[A-Za-z0-9_]{1, 18}$'")),
        nullable=False
    )

    sentiment = Column(
        Enum("positive", "negative", "neutral", name="sentiment_enum"),
        nullable=False
    )
    reasoning = Column(
        Text,
        nullable=False
    )

    date = Column(
        Date,
        default=text("(current_date AT TIME ZONE 'UTC')::date")
    )


Base.metadata.create_all(engine)
