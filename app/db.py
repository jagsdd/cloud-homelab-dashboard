import psycopg2

from app.config import DATABASE_URL

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    return conn, cursor
