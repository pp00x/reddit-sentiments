from os import environ
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = environ["DATABASE_URL"]
REDIS_URL: str = environ["REDIS_URL"]
OPENAI_API_KEY: str = environ["OPENAI_API_KEY"]