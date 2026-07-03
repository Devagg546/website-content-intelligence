"""
Crawl Repository — CRUD operations for crawl jobs in SQLite.
"""

import sqlite3
from datetime import datetime
from typing import Optional


class CrawlRepository:
    """Data access layer for crawl jobs."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_job(self, job_id: str, root_url: str, max_pages: int = 500) -> None:
        """Create a new crawl job record."""
        self.conn.execute(
            """
            INSERT INTO crawl_jobs (job_id, root_url, status, max_pages, started_at)
            VALUES (?, ?, 'queued', ?, ?)
            """,
            (job_id, root_url, max_pages, datetime.utcnow().isoformat()),
        )
        self.conn.commit()

    def update_status(
        self,
        job_id: str,
        status: str,
        pages_crawled: int = None,
        pages_total: int = None,
        error_message: str = None,
    ) -> None:
        """Update the status and progress of a crawl job."""
        updates = ["status = ?"]
        params = [status]

        if pages_crawled is not None:
            updates.append("pages_crawled = ?")
            params.append(pages_crawled)

        if pages_total is not None:
            updates.append("pages_total = ?")
            params.append(pages_total)

        if error_message is not None:
            updates.append("error_message = ?")
            params.append(error_message)

        if status == "completed" or status == "failed":
            updates.append("completed_at = ?")
            params.append(datetime.utcnow().isoformat())

        params.append(job_id)

        self.conn.execute(
            f"UPDATE crawl_jobs SET {', '.join(updates)} WHERE job_id = ?",
            params,
        )
        self.conn.commit()

    def get_job(self, job_id: str) -> Optional[dict]:
        """Get a crawl job by its ID."""
        cursor = self.conn.execute(
            "SELECT * FROM crawl_jobs WHERE job_id = ?", (job_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def list_jobs(self, limit: int = 20) -> list[dict]:
        """List recent crawl jobs ordered by start time."""
        cursor = self.conn.execute(
            "SELECT * FROM crawl_jobs ORDER BY started_at DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]
