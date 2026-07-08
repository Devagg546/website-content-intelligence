"""
Pytest configuration and shared fixtures.
"""

import sqlite3
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.sqlite_db import init_database


@pytest.fixture(scope="session")
def test_client():
    """Create a FastAPI test client for integration tests."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db_connection(tmp_path):
    """Create an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    # Create tables
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            title TEXT DEFAULT '',
            meta_description TEXT DEFAULT '',
            h1 TEXT DEFAULT '',
            body_text TEXT DEFAULT '',
            canonical_url TEXT,
            word_count INTEGER DEFAULT 0,
            crawl_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            crawl_job_id TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE crawl_jobs (
            job_id TEXT PRIMARY KEY,
            root_url TEXT NOT NULL,
            status TEXT DEFAULT 'queued',
            max_pages INTEGER DEFAULT 500,
            pages_crawled INTEGER DEFAULT 0,
            pages_total INTEGER DEFAULT 0,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT
        )
    """)
    conn.commit()

    yield conn
    conn.close()
