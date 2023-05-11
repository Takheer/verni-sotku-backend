import os
import psycopg2

from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

DB_HOST=os.environ["DB_HOST"]
DB_NAME=os.environ["DB_NAME"]
DB_USERNAME=os.environ['DB_USERNAME']
DB_PASSWORD=os.environ['DB_PASSWORD']
DB_PORT=os.environ['DB_PORT'] if os.environ['DB_PORT'] else 5432

def get_sa_connection():
    engine_url = "postgresql://{}:{}@{}:{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    is_dev = DB_HOST == "localhost"
    engine = create_engine(engine_url, echo=is_dev)
    return engine

def get_db_connection():
    conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'],
            port=os.environ['DB_PORT'] if os.environ['DB_PORT'] else 5432)
    return conn