"""
Inventory Service — Content inventory analytics and statistics.

Generates comprehensive content inventory reports including:
- Total pages and word counts
- Top keywords and term frequency
- Largest and smallest pages
- Average content length
"""

import re
from collections import Counter

from app.models.inventory import InventoryResponse, KeywordStat, PageStat

# Common English words to exclude from keyword analysis - they add no meaning
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "up", "about", "into", "through", "during",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "should", "could", "may", "might",
    "must", "can", "this", "that", "these", "those", "i", "you", "he", "she",
    "it", "we", "they", "what", "which", "who", "whom", "as", "if", "then",
    "so", "than", "too", "very", "just", "not", "no", "yes", "your", "our",
    "their", "its", "his", "her", "all", "each", "more", "most", "other",
    "some", "such", "only", "own", "same", "here", "there", "when", "where",
    "how", "why", "us", "also",
}


class InventoryService:
    """Generates content inventory reports from crawled data."""

    def generate_report(self, db_conn) -> InventoryResponse:
        """
        Generate a complete content inventory report.

        Args:
            db_conn: SQLite database connection

        Returns:
            InventoryResponse with all statistics
        """
        return InventoryResponse(
            total_pages=self._count_pages(db_conn),
            total_words=self._total_word_count(db_conn),
            avg_content_length=self._avg_content_length(db_conn),
            top_keywords=self._extract_top_keywords(db_conn),
            largest_pages=self._get_largest_pages(db_conn),
            smallest_pages=self._get_smallest_pages(db_conn),
        )

    def _count_pages(self, db_conn) -> int:
        """Count total crawled pages."""
        cursor = db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pages")
        result = cursor.fetchone()
        return result[0] if result else 0

    def _total_word_count(self, db_conn) -> int:
        """Calculate total word count across all pages."""
        cursor = db_conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(word_count), 0) FROM pages")
        result = cursor.fetchone()
        return result[0] if result else 0

    def _avg_content_length(self, db_conn) -> float:
        """Calculate average content length (words per page)."""
        cursor = db_conn.cursor()
        cursor.execute("SELECT COALESCE(AVG(word_count), 0) FROM pages")
        result = cursor.fetchone()
        return round(result[0], 2) if result else 0.0

    def _extract_top_keywords(self, db_conn, limit: int = 20) -> list[KeywordStat]:
        """
        Extract most frequently used keywords across all pages.
        Uses simple word frequency analysis, excluding stop words.
        """
        cursor = db_conn.cursor()
        cursor.execute("SELECT body_text FROM pages")
        rows = cursor.fetchall()

        word_counter = Counter()
        page_counter = Counter()

        for row in rows:
            body_text = row[0] or ""
            words = re.findall(r"\b[a-zA-Z]{3,}\b", body_text.lower())
            words = [w for w in words if w not in STOP_WORDS]

            word_counter.update(words)
            page_counter.update(set(words))

        top_words = word_counter.most_common(limit)

        return [
            KeywordStat(keyword=word, count=count, pages=page_counter[word])
            for word, count in top_words
        ]

    def _get_largest_pages(self, db_conn, limit: int = 10) -> list[PageStat]:
        """Get pages with the highest word count."""
        cursor = db_conn.cursor()
        cursor.execute(
            "SELECT url, title, word_count FROM pages ORDER BY word_count DESC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
        return [
            PageStat(url=row[0], title=row[1] or "", word_count=row[2] or 0)
            for row in rows
        ]

    def _get_smallest_pages(self, db_conn, limit: int = 10) -> list[PageStat]:
        """Get pages with the lowest word count (excluding empty pages)."""
        cursor = db_conn.cursor()
        cursor.execute(
            "SELECT url, title, word_count FROM pages WHERE word_count > 0 ORDER BY word_count ASC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
        return [
            PageStat(url=row[0], title=row[1] or "", word_count=row[2] or 0)
            for row in rows
        ]