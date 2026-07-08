"""
Shared API dependencies.

Provides dependency injection for database sessions,
vector store clients, and service instances.
"""

from app.db.sqlite_db import get_db_connection
from app.db.vector_store import get_vector_store


def get_db():
    """Dependency: yields a SQLite database connection."""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


def get_chroma():
    """Dependency: returns the ChromaDB collection instance."""
    return get_vector_store()
