from app.validation import validate_server_create
from app.repository import create_server

def create_server_service(data):

    if not data:
        return ({"error": "Invalid JSON"}, 400)

    error = validate_server_create(data)
    if error:
        return ({"error": error}, 400)
    
    result = create_server(data)

    return ({"message": "server added", "server": result}, 201)