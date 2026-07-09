from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    if not MONGO_URI:
        raise ValueError("MONGO_URI is missing")

    if not DATABASE_NAME:
        raise ValueError("DATABASE_NAME is missing")

settings = Settings()