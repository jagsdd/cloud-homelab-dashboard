from app.validation import validate_server_create, validate_server_update
from app.repository import create_server, update_server

def create_server_service(data):

    if not data:
        return ({"error": "Invalid JSON"}, 400)

    error = validate_server_create(data)
    if error:
        return ({"error": error}, 400)
    
    result = create_server(data)

    return ({"message": "server added", "server": result}, 201)


def update_server_service(server_id, data):

    if not data:
        return ({"error": "Invalid JSON"}, 400)

    error = validate_server_update(data)
    if error:
        return ({"error": error}, 400)
    
    result = update_server(server_id, data)

    if result is None:
        return ({"error": "server not found"}, 404)
    
    return ({"message": "server updated", "server": result}, 200)