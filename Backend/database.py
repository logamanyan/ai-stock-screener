from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import urllib.parse
import os

DB_USER = "postgres"
DB_PASSWORD = "Logamanyan@15"   
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "stock_screener"

encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

DATABASE_URL = os.environ.get("DATABASE_URL", f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
