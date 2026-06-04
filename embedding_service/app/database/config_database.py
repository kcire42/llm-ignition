import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

env_path = BASE_DIR / ".env"

load_dotenv(env_path)

class Config:
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = int(os.getenv("POSTGRES_PORT"))
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    