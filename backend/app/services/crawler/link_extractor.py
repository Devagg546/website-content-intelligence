"""
Link Extractor — Discover internal links from parsed HTML.

Extracts all <a href="..."> links and filters to internal links
belonging to the same domain as the crawl root URL.
"""

from urllib.parse import urljoin, urlparse
from typing import Set

from bs4 import BeautifulSoup


class LinkExtractor:
    """Extracts and filters internal links from HTML content."""

    # File extensions to skip (not web pages)
    SKIP_EXTENSIONS = {
        ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
        ".mp4", ".mp3", ".avi", ".mov", ".zip", ".tar", ".gz",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".css", ".js", ".xml", ".json", ".ico",
    }

    # URL fragments/patterns to skip
    SKIP_PATTERNS = {
        "mailto:", "tel:", "javascript:", "ftp:", "#",
    }

    def extract_internal_links(
        self, html: str, page_url: str, root_domain: str
    ) -> Set[str]:
        """
        Extract all internal links from the HTML content.

        Args:
            html: Raw HTML string
            page_url: Current page URL (for resolving relative links)
            root_domain: Root domain to filter internal links

        Returns:
            Set of absolute internal link URLs
        """
        soup = BeautifulSoup(html, "lxml")
        internal_links = set()

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"].strip()

            # Skip non-HTTP links
            if any(href.startswith(pattern) for pattern in self.SKIP_PATTERNS):
                continue

            # Resolve relative URLs to absolute
            absolute_url = urljoin(page_url, href)

            # Remove fragment identifiers
            absolute_url = absolute_url.split("#")[0]

            # Remove trailing slash for consistency
            absolute_url = absolute_url.rstrip("/")

            # Skip if not internal
            if not self._is_internal(absolute_url, root_domain):
                continue

            # Skip non-page file extensions
            if self._has_skip_extension(absolute_url):
                continue

            internal_links.add(absolute_url)

        return internal_links

    def _is_internal(self, url: str, root_domain: str) -> bool:
        """Check if a URL belongs to the same domain."""
        try:
            parsed = urlparse(url)
            return parsed.netloc == root_domain
        except Exception:
            return False

    def _has_skip_extension(self, url: str) -> bool:
        """Check if the URL points to a non-page file type."""
        path = urlparse(url).path.lower()
        return any(path.endswith(ext) for ext in self.SKIP_EXTENSIONS)
