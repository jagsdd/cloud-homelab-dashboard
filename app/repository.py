from app.db import get_db

def get_all_servers():
    conn, cursor = get_db()
    
    cursor.execute("SELECT id, name, status FROM servers")
    rows = cursor.fetchall()
    
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "status": row[2],
        }
        for row in rows
    ]

