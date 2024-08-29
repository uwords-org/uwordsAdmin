import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL Admin
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

# SYSTEM
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
FASTAPI_SECRET = os.environ.get("FASTAPI_SECRET")
ADMIN_SECRET = os.environ.get("ADMIN_SECRET")
SERVICE_TOKEN = os.environ.get("SERVICE_TOKEN")
