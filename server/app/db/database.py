import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

load_dotenv()

password = quote_plus(os.getenv("DB_PASSWORD") or "")

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{password}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()