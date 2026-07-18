"""
SQLite Database Manager — Connection management and table initialization.

Creates and manages the SQLite database for storing:
- Crawled page metadata
- Crawl job status and history
"""

import sqlite3
from pathlib import Path

from app.config import settings


def init_database() -> None:
    """
    Initialize the SQLite database and create tables if they don't exist.
    Called during application startup via lifespan.
    """
    db_path = Path(settings.sqlite_db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # ── Pages Table ──────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            title TEXT DEFAULT '',
            meta_description TEXT DEFAULT '',
            h1 TEXT DEFAULT '',
            body_text TEXT DEFAULT '',
            canonical_url TEXT,
            word_count INTEGER DEFAULT 0,
            crawl_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            crawl_job_id TEXT,
            FOREIGN KEY (crawl_job_id) REFERENCES crawl_jobs(job_id)
        )
    """)

    # ── Crawl Jobs Table ─────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crawl_jobs (
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

    # ── Internal Links Table (for orphan page detection) ─────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internal_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT NOT NULL,
            target_url TEXT NOT NULL,
            crawl_job_id TEXT,
            FOREIGN KEY (crawl_job_id) REFERENCES crawl_jobs(job_id)
        )
    """)

    # ── Indexes ──────────────────────────────────────────────────────
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pages_url ON pages(url)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pages_crawl_job ON pages(crawl_job_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_target ON internal_links(target_url)")

    conn.commit()
    conn.close()


def get_db_connection() -> sqlite3.Connection:
    """
    Create and return a new SQLite database connection.
    Uses Row factory for dict-like row access.
    """
    conn = sqlite3.connect(str(Path(settings.sqlite_db_path)), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent read performance
    return conn
