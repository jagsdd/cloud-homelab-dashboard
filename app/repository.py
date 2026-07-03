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

def update_server(server_id, data):    
    conn, cursor = get_db()

    cursor.execute("SELECT id, name, status FROM servers WHERE id = %s", (server_id,))
    
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None
    
    name = data.get("name", row[1])
    status = data.get("status", row[2])

    cursor.execute("UPDATE servers SET name = %s, status = %s WHERE id = %s", (name, status, server_id))

    conn.commit()
    conn.close()

    return {
        "id": server_id,
        "name": name,
        "status": status
    }

def create_server(data):
    conn, cursor = get_db()

    name = data["name"]
    status = data.get("status", "unknown")

    cursor.execute(
        "INSERT INTO servers (name, status) VALUES (%s, %s) RETURNING id",
        (name, status)
    )

    server_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return {
        "id": server_id,
        "name": name,
        "status": status
    }
