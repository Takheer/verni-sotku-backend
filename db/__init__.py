import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase


class Base(DeclarativeBase):
    pass


load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
pg_url = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
engine = create_engine(pg_url)


def create_db_and_tables():
    Base.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
