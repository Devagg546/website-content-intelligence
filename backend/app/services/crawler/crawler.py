"""
Web Crawler — BFS-based website crawler using Playwright.

Crawls a website starting from a root URL, following internal links
using breadth-first search. Stops when max_pages is reached or
all discoverable pages have been visited.
"""

import asyncio
import uuid
from collections import deque
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from app.config import settings
from app.services.crawler.parser import PageParser
from app.services.crawler.link_extractor import LinkExtractor


class CrawlJob:
    """Represents a single crawl job with its state and progress."""

    def __init__(self, url: str, max_pages: int = 500):
        self.job_id: str = str(uuid.uuid4())
        self.root_url: str = url
        self.max_pages: int = max_pages
        self.status: str = "queued"  # queued | in_progress | completed | failed
        self.pages_crawled: int = 0
        self.pages_total: int = 0
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.error_message: Optional[str] = None


class WebCrawler:
    """
    BFS web crawler using Playwright for page rendering
    and BeautifulSoup for content extraction.
    """

    def __init__(self):
        self.parser = PageParser()
        self.link_extractor = LinkExtractor()

    async def crawl(self, job: CrawlJob, db_conn) -> None:
        """
        Execute a crawl job using breadth-first search.

        Algorithm:
        1. Start from root URL
        2. Add all internal links to a queue
        3. Visit each link, extract content, add new links
        4. Stop at max_pages or when queue is empty
        5. Use a set() to avoid visiting the same URL twice

        Args:
            job: The CrawlJob instance with configuration
            db_conn: SQLite database connection for storing results
        """
        # TODO: Implement BFS crawl logic
        # 1. Initialize Playwright browser (headless)
        # 2. Create visited set and page queue (deque)
        # 3. Parse root_url domain for internal link filtering
        # 4. BFS loop:
        #    a. Dequeue URL
        #    b. Visit with Playwright
        #    c. Extract content with BeautifulSoup (via parser)
        #    d. Extract internal links (via link_extractor)
        #    e. Store page data in SQLite
        #    f. Add new internal links to queue
        #    g. Update job progress
        # 5. Update job status to completed/failed
        pass

    async def _visit_page(self, url: str) -> Optional[dict]:
        """
        Visit a single page using Playwright and extract its content.

        Returns:
            Dict with page data (url, title, meta_description, h1, body_text, etc.)
            or None if the page couldn't be loaded.
        """
        # TODO: Implement Playwright page visit
        # 1. Navigate to URL with timeout
        # 2. Wait for page load
        # 3. Get page HTML content
        # 4. Parse with BeautifulSoup via self.parser
        # 5. Return structured page data
        pass

    def _is_internal_link(self, link: str, root_domain: str) -> bool:
        """Check if a link belongs to the same domain as the root URL."""
        try:
            parsed = urlparse(link)
            return parsed.netloc == root_domain or parsed.netloc == ""
        except Exception:
            return False
