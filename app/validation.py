ALLOWED_STATUSES = {"online", "offline", "maintenance"}

def validate_server_create(data):
    if not data:
        return "No input data provided"

    name = data.get("name")
    if not name or not name.strip():
        return "Name is required"

    status = data.get("status")
    if status and status not in ALLOWED_STATUSES:
        return f"Invalid status. Must be one of {sorted(ALLOWED_STATUSES)}"
    
    return None

def validate_server_update(data):
    if not data:
        return "No input data provided"
    
    status = data.get("status")
    if status and status not in ALLWED_STATUSES:
        return f"Invalid status. Must be one of {sorted(ALLOWED_STATUSES)}"
    
    return None
    