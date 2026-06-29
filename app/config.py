import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/dashboard"
)

PORT = os.getenv("PORT", "5000")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
