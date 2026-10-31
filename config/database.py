"""Shared database connection settings for the local project."""

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.engine import Engine

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "hamburg_mobility_urban_new"
DB_DRIVER = "postgresql+psycopg"


def create_database_engine(username: str, password: str) -> Engine:
    """Create an SQLAlchemy engine using credentials supplied at runtime."""
    if not username.strip():
        raise ValueError("Database username must not be empty.")

    if not password:
        raise ValueError("Database password must not be empty.")

    db_url = URL.create(
        drivername=DB_DRIVER,
        username=username,
        password=password,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )

    return create_engine(db_url, pool_pre_ping=True)
