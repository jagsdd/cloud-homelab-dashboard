import os

DATABASE_URL = os.environ["DATABASE_URL"]

PORT = os.getenv("PORT", "5000")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
