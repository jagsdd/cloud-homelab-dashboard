from app.validation import validate_server_create, validate_server_update
from app.repository import (
    create_server,
    update_server,
    delete_server,
    get_all_servers,
    get_server
)
import logging
from app.metrics import servers_created_total

logger = logging.getLogger(__name__)


def create_server_service(data):

    if not data:
        return ({"error": "Invalid JSON"}, 400)

    error = validate_server_create(data)
    if error:
        return ({"error": error}, 400)
    
    result = create_server(data)
    servers_created_total.inc()

    logger.info("Server created: id=%s name=%s", result["id"], result["name"])

    return ({"message": "server added", "server": result}, 201)


def update_server_service(server_id, data):

    if not data:
        return ({"error": "Invalid JSON"}, 400)

    error = validate_server_update(data)
    if error:
        return ({"error": error}, 400)
    
    result = update_server(server_id, data)

    if result is None:
        logger.warning("Server update failed: id=%s not found", server_id)
        return ({"error": "server not found"}, 404)

    logger.info(
        "Server updated: id=%s name=%s status=%s",
        result["id"],
        result["name"],
        result["status"]
    )
    
    return ({"message": "server updated", "server": result}, 200)

def delete_server_service(server_id):
    deleted = delete_server(server_id)

    if not deleted:
        logger.warning("Server deletion failed: id=%s not found", server_id)
        return ({"error": "server not found"}, 404)

    logger.info("Server deleted: id=%s", server_id)
    return ({"message": "server deleted"}, 200)

def get_all_servers_service():
    return (get_all_servers(), 200)

def get_server_service(server_id):
    server = get_server(server_id)

    if server is None:
        return ({"error": "server not found"}, 404)
    
    return ({"server": server}, 200)


