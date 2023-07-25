from dotenv import load_dotenv
from os import environ
from sqlalchemy.orm import sessionmaker, Session, class_mapper
from sqlalchemy import create_engine, Engine

load_dotenv()

engine: Engine = create_engine(environ["DATABASE_URL"], echo=True)

Session: sessionmaker[Session] = sessionmaker(bind=engine)

