"""
Create the SQLAlchemy engine
Create database sessions
Give repositories access to the database

"""

"""
database.py
1. Read DATABASE_URL from config
2. Create SQLAlchemy engine
3. Create SessionLocal
4. Provide get_db()
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import config


engine = create_engine(config.database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()