"""
Tests for crawler service components.
"""

import pytest
from app.services.crawler.parser import PageParser
from app.services.crawler.link_extractor import LinkExtractor


class TestPageParser:
    """Tests for the HTML page parser."""

    def setup_method(self):
        self.parser = PageParser()

    def test_extract_title(self):
        """Test title extraction from HTML."""
        html = "<html><head><title>Test Page Title</title></head><body></body></html>"
        result = self.parser.parse(html, "https://example.com")
        assert result["title"] == "Test Page Title"

    def test_extract_meta_description(self):
        """Test meta description extraction."""
        html = '<html><head><meta name="description" content="Test description"></head><body></body></html>'
        result = self.parser.parse(html, "https://example.com")
        assert result["meta_description"] == "Test description"

    def test_extract_h1(self):
        """Test H1 extraction."""
        html = "<html><body><h1>Main Heading</h1></body></html>"
        result = self.parser.parse(html, "https://example.com")
        assert result["h1"] == "Main Heading"

    def test_extract_body_text(self):
        """Test body text extraction with noise removal."""
        html = """
        <html>
        <body>
            <nav>Navigation</nav>
            <main><p>This is the main content.</p></main>
            <footer>Footer text</footer>
            <script>console.log('noise');</script>
        </body>
        </html>
        """
        result = self.parser.parse(html, "https://example.com")
        assert "main content" in result["body_text"]
        assert "console.log" not in result["body_text"]


class TestLinkExtractor:
    """Tests for the link extractor."""

    def setup_method(self):
        self.extractor = LinkExtractor()

    def test_extract_internal_links(self):
        """Test internal link extraction."""
        html = """
        <html><body>
            <a href="/about">About</a>
            <a href="https://example.com/contact">Contact</a>
            <a href="https://external.com/page">External</a>
        </body></html>
        """
        links = self.extractor.extract_internal_links(
            html, "https://example.com/page", "example.com"
        )
        assert "https://example.com/about" in links
        assert "https://example.com/contact" in links
        assert "https://external.com/page" not in links

    def test_skip_file_extensions(self):
        """Test that non-page file links are skipped."""
        html = '<html><body><a href="/file.pdf">PDF</a></body></html>'
        links = self.extractor.extract_internal_links(
            html, "https://example.com", "example.com"
        )
        assert len(links) == 0
