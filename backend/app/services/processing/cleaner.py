"""
Content Cleaner — Clean HTML and extract readable text.

Handles:
- Removing scripts, styles, and non-content elements
- Extracting clean, readable text
- Normalizing whitespace
"""

import re
from bs4 import BeautifulSoup


class ContentCleaner:
    """Cleans raw HTML content into readable text."""

    # Elements that typically don't contain useful content
    NOISE_TAGS = [
        "script", "style", "nav", "footer", "header", "aside",
        "noscript", "iframe", "form", "button", "svg",
    ]

    def clean_html(self, html: str) -> str:
        """
        Convert raw HTML to clean, readable text.

        Args:
            html: Raw HTML string

        Returns:
            Cleaned text content
        """
        soup = BeautifulSoup(html, "lxml")

        # Remove noise elements
        for tag in self.NOISE_TAGS:
            for element in soup.find_all(tag):
                element.decompose()

        # Extract text
        text = soup.get_text(separator="\n", strip=True)

        # Normalize whitespace
        text = self._normalize_whitespace(text)

        return text

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace while preserving paragraph structure."""
        # Replace multiple newlines with double newline (paragraph break)
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Replace multiple spaces with single space
        text = re.sub(r"[ \t]+", " ", text)
        # Strip leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split("\n")]
        # Remove empty lines that aren't paragraph breaks
        cleaned_lines = []
        prev_empty = False
        for line in lines:
            if line == "":
                if not prev_empty:
                    cleaned_lines.append("")
                prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False

        return "\n".join(cleaned_lines).strip()
