"""
Page Repository — CRUD operations for crawled pages in SQLite.
"""

import sqlite3
from typing import Optional


class PageRepository:
    """Data access layer for crawled pages."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert_page(self, page_data: dict) -> int:
        """
        Insert a new crawled page into the database.

        Args:
            page_data: Dict with url, title, meta_description, h1,
                       body_text, canonical_url, word_count, crawl_job_id

        Returns:
            The ID of the inserted row
        """
        cursor = self.conn.execute(
            """
            INSERT OR REPLACE INTO pages
            (url, title, meta_description, h1, body_text, canonical_url, word_count, crawl_job_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                page_data.get("url", ""),
                page_data.get("title", ""),
                page_data.get("meta_description", ""),
                page_data.get("h1", ""),
                page_data.get("body_text", ""),
                page_data.get("canonical_url"),
                page_data.get("word_count", 0),
                page_data.get("crawl_job_id"),
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_page_by_id(self, page_id: int) -> Optional[dict]:
        """Get a single page by its ID."""
        cursor = self.conn.execute("SELECT * FROM pages WHERE id = ?", (page_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_page_by_url(self, url: str) -> Optional[dict]:
        """Get a single page by its URL."""
        cursor = self.conn.execute("SELECT * FROM pages WHERE url = ?", (url,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def list_pages(
        self,
        page: int = 1,
        per_page: int = 20,
        search: str = None,
    ) -> tuple[list[dict], int]:
        """
        List pages with pagination and optional search filter.

        Returns:
            Tuple of (page list, total count)
        """
        offset = (page - 1) * per_page

        if search:
            count_query = "SELECT COUNT(*) FROM pages WHERE title LIKE ? OR url LIKE ?"
            search_param = f"%{search}%"
            cursor = self.conn.execute(count_query, (search_param, search_param))
            total = cursor.fetchone()[0]

            cursor = self.conn.execute(
                "SELECT * FROM pages WHERE title LIKE ? OR url LIKE ? ORDER BY id LIMIT ? OFFSET ?",
                (search_param, search_param, per_page, offset),
            )
        else:
            cursor = self.conn.execute("SELECT COUNT(*) FROM pages")
            total = cursor.fetchone()[0]

            cursor = self.conn.execute(
                "SELECT * FROM pages ORDER BY id LIMIT ? OFFSET ?",
                (per_page, offset),
            )

        pages = [dict(row) for row in cursor.fetchall()]
        return pages, total

    def count_pages(self) -> int:
        """Get total number of crawled pages."""
        cursor = self.conn.execute("SELECT COUNT(*) FROM pages")
        return cursor.fetchone()[0]

    def get_all_pages(self) -> list[dict]:
        """Get all pages (for analysis operations)."""
        cursor = self.conn.execute("SELECT * FROM pages")
        return [dict(row) for row in cursor.fetchall()]
