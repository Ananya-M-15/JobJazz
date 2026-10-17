import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def normalize_database_url(url: str | None) -> str:
    """
    Normalize database connection URLs for SQLAlchemy.
    - Converts legacy 'postgres://' scheme to 'postgresql://'
    - Converts legacy 'postgresql+psycopg2://' to standard 'postgresql://' (using psycopg v3)
    - Preserves query parameters like '?sslmode=require' for Neon / managed PostgreSQL
    """
    if not url:
        return "postgresql://postgres:postgres@localhost:5432/jobjazz"

    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    elif url.startswith("postgresql+psycopg2://"):
        return url.replace("postgresql+psycopg2://", "postgresql://", 1)

    return url


DATABASE_URL = normalize_database_url(os.getenv("DATABASE_URL"))

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
