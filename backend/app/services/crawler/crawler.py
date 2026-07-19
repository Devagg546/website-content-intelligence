"""
Web Crawler — BFS-based website crawler.
Crawls a website starting from a root URL, following internal links
using breadth-first search. Uses PageParser and LinkExtractor.
"""

import uuid
import requests
from collections import deque
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from app.config import settings
from app.services.crawler.parser import PageParser
from app.services.crawler.link_extractor import LinkExtractor


class CrawlJob:
    """Represents a single crawl job with its state and progress."""

    def __init__(self, url: str, max_pages: int = None):
        self.job_id: str = str(uuid.uuid4())
        self.root_url: str = url
        self.max_pages: int = max_pages or settings.max_crawl_pages
        self.status: str = "queued"
        self.pages_crawled: int = 0
        self.pages_total: int = 0
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.error_message: Optional[str] = None


class WebCrawler:
    """BFS web crawler using requests, PageParser and LinkExtractor."""

    def __init__(self):
        self.parser = PageParser()
        self.link_extractor = LinkExtractor()

    def fetch_html(self, url: str) -> Optional[str]:
        """Fetch raw HTML from a URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def crawl(self, job: CrawlJob) -> list[dict]:
        """
        Execute a crawl job using breadth-first search.
        Returns list of page data dictionaries.
        """
        parsed_start = urlparse(job.root_url)
        base_domain = parsed_start.netloc

        visited = set()
        queue = deque([job.root_url])
        all_pages = []

        job.status = "in_progress"
        job.started_at = datetime.now()

        print(f"Starting crawl: {job.root_url}")
        print(f"Max pages: {job.max_pages}")
        print("-" * 50)

        while queue and len(visited) < job.max_pages:
            url = queue.popleft()

            if url in visited:
                continue

            print(f"Crawling ({len(visited) + 1}/{job.max_pages}): {url}")

            # Fetch raw HTML
            html = self.fetch_html(url)
            if html is None:
                visited.add(url)
                continue

            # Parse page content using Sarvesh's PageParser
            page_data = self.parser.parse(html, url)

            # Add crawl date
            page_data["crawl_date"] = str(datetime.now().date())

            # Extract internal links using Sarvesh's LinkExtractor
            new_links = self.link_extractor.extract_internal_links(
                html, url, base_domain
            )

            # Save discovered links so we can build the internal_links table later
            page_data["outgoing_links"] = list(new_links)

            all_pages.append(page_data)

            for link in new_links:
                if link not in visited:
                    queue.append(link)

            visited.add(url)
            job.pages_crawled = len(all_pages)

        job.status = "completed"
        job.completed_at = datetime.now()

        print("-" * 50)
        print(f"Crawl complete. Pages crawled: {len(all_pages)}")

        return all_pages