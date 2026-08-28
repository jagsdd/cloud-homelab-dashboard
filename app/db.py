import psycopg2

from app.config import DATABASE_URL

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    return conn, cursor

def init_db():
    conn, cursor = get_db()
    
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS servers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                status VARCHAR(50)
                )""")
    
    conn.commit()
    conn.close()

def check_db_connection():
    try:
        conn, cursor = get_db()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return True
    except psycopg2.Error:
        return False
    

