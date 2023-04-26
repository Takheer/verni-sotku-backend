import os
import psycopg2

from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'],
            port=os.environ['DB_PORT'] if os.environ['DB_PORT'] else 5432)
    return conn