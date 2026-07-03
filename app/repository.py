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

def delete_server(server_id):
    conn, cursor = get_db()

    cursor.execute("DELETE FROM servers WHERE id = %s", (server_id,))

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted
