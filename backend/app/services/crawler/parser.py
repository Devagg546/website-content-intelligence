"""
Page Parser — Extract structured content from HTML using BeautifulSoup.

Extracts:
- Page title
- Meta description
- H1 text
- Body text (cleaned)
- Canonical URL
"""

from typing import Optional

from bs4 import BeautifulSoup


class PageParser:
    """Parses raw HTML and extracts structured page content."""

    def parse(self, html: str, url: str) -> dict:
        """
        Parse HTML content and extract structured data.

        Args:
            html: Raw HTML string
            url: The URL of the page (for reference)

        Returns:
            Dict with extracted page data:
            {
                "url": str,
                "title": str,
                "meta_description": str,
                "h1": str,
                "body_text": str,
                "canonical_url": str | None,
            }
        """
        soup = BeautifulSoup(html, "lxml")

        return {
            "url": url,
            "title": self._extract_title(soup),
            "meta_description": self._extract_meta_description(soup),
            "h1": self._extract_h1(soup),
            "body_text": self._extract_body_text(soup),
            "canonical_url": self._extract_canonical(soup),
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the page title from <title> tag."""
        title_tag = soup.find("title")
        return title_tag.get_text(strip=True) if title_tag else ""

    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description content."""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            return meta["content"].strip()
        return ""

    def _extract_h1(self, soup: BeautifulSoup) -> str:
        """Extract the first H1 tag's text content."""
        h1_tag = soup.find("h1")
        return h1_tag.get_text(strip=True) if h1_tag else ""

    def _extract_body_text(self, soup: BeautifulSoup) -> str:
        """
        Extract clean body text by removing scripts, styles,
        navigation, and other non-content elements.
        """
        # Remove non-content elements
        for element in soup.find_all(
            ["script", "style", "nav", "footer", "header", "aside", "noscript"]
        ):
            element.decompose()

        # Get text content
        body = soup.find("body")
        if body:
            text = body.get_text(separator=" ", strip=True)
            # Clean up extra whitespace
            return " ".join(text.split())
        return ""

    def _extract_canonical(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract canonical URL from <link rel='canonical'>."""
        canonical = soup.find("link", attrs={"rel": "canonical"})
        if canonical and canonical.get("href"):
            return canonical["href"].strip()
        return None
