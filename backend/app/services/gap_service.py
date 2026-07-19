"""
Gap Detection Service — Identify content gaps and SEO issues.

Detects:
- Missing page titles
- Missing meta descriptions
- Missing H1 tags
- Thin content (below word count threshold)
- Duplicate content (high text similarity)
- Orphan pages (no internal links pointing to them)
"""

from difflib import SequenceMatcher

from app.models.gaps import GapsResponse, GapItem, DuplicatePair


class GapService:
    """Detects content gaps, SEO issues, and quality problems."""

    THIN_CONTENT_THRESHOLD = 100  # words
    DUPLICATE_SIMILARITY_THRESHOLD = 0.85

    def detect_gaps(self, db_conn) -> GapsResponse:
        """
        Run all gap detection checks and compile a report.
        """
        missing_title = self._find_missing_titles(db_conn)
        missing_meta = self._find_missing_meta_descriptions(db_conn)
        missing_h1 = self._find_missing_h1(db_conn)
        thin = self._find_thin_content(db_conn)
        duplicates = self._find_duplicate_content(db_conn)
        orphans = self._find_orphan_pages(db_conn)

        total = (
            len(missing_title)
            + len(missing_meta)
            + len(missing_h1)
            + len(thin)
            + len(duplicates)
            + len(orphans)
        )

        return GapsResponse(
            missing_title=missing_title,
            missing_meta_description=missing_meta,
            missing_h1=missing_h1,
            thin_content=thin,
            duplicate_content=duplicates,
            orphan_pages=orphans,
            total_issues=total,
        )

    def _find_missing_titles(self, db_conn) -> list[GapItem]:
        """Find pages with empty or missing title tags."""
        cursor = db_conn.cursor()
        cursor.execute(
            "SELECT url, title FROM pages WHERE title IS NULL OR title = '' OR title = 'No title found'"
        )
        rows = cursor.fetchall()
        return [
            GapItem(url=row["url"], title="", issue="Missing page title", severity="high")
            for row in rows
        ]

    def _find_missing_meta_descriptions(self, db_conn) -> list[GapItem]:
        """Find pages with empty or missing meta descriptions."""
        cursor = db_conn.cursor()
        cursor.execute(
            """
            SELECT url, title FROM pages
            WHERE meta_description IS NULL OR meta_description = ''
               OR meta_description = 'No meta description found'
            """
        )
        rows = cursor.fetchall()
        return [
            GapItem(
                url=row["url"],
                title=row["title"] or "",
                issue="Missing meta description",
                severity="medium",
            )
            for row in rows
        ]

    def _find_missing_h1(self, db_conn) -> list[GapItem]:
        """Find pages with empty or missing H1 tags."""
        cursor = db_conn.cursor()
        cursor.execute(
            "SELECT url, title FROM pages WHERE h1 IS NULL OR h1 = '' OR h1 = 'No H1 found'"
        )
        rows = cursor.fetchall()
        return [
            GapItem(
                url=row["url"], title=row["title"] or "", issue="Missing H1 tag", severity="medium"
            )
            for row in rows
        ]

    def _find_thin_content(self, db_conn) -> list[GapItem]:
        """Find pages with content below the word count threshold."""
        cursor = db_conn.cursor()
        cursor.execute(
            "SELECT url, title, word_count FROM pages WHERE word_count < ? AND word_count > 0",
            (self.THIN_CONTENT_THRESHOLD,),
        )
        rows = cursor.fetchall()
        return [
            GapItem(
                url=row["url"],
                title=row["title"] or "",
                issue=f"Thin content: only {row['word_count']} words (recommended: {self.THIN_CONTENT_THRESHOLD}+)",
                severity="low",
            )
            for row in rows
        ]

    def _find_duplicate_content(self, db_conn) -> list[DuplicatePair]:
        """
        Find pages with highly similar content.
        Optimized: only compares pages with similar word counts (within 20%),
        since pages with very different lengths can never be near-duplicates.
        This avoids the O(n²) full-comparison cost on large sites.
        """
        cursor = db_conn.cursor()
        cursor.execute(
            "SELECT url, body_text, word_count FROM pages WHERE body_text IS NOT NULL AND body_text != ''"
        )
        rows = cursor.fetchall()

        pages = [(row["url"], row["body_text"], row["word_count"] or 0) for row in rows]

        # Sort by word count so similar-length pages sit near each other
        pages.sort(key=lambda p: p[2])

        duplicates = []
        n = len(pages)

        for i in range(n):
            url_a, text_a, count_a = pages[i]
            if count_a == 0:
                continue

            sample_a = text_a[:2000]

            # Only look forward at pages with word count within 20% of this one
            for j in range(i + 1, n):
                url_b, text_b, count_b = pages[j]

                # Since sorted by word count, once the gap is too big, stop looking further
                if count_b > count_a * 1.2:
                    break

                if count_b < count_a * 0.8:
                    continue

                sample_b = text_b[:2000]
                similarity = SequenceMatcher(None, sample_a, sample_b).ratio()

                if similarity >= self.DUPLICATE_SIMILARITY_THRESHOLD:
                    duplicates.append(
                        DuplicatePair(url_a=url_a, url_b=url_b, similarity_score=round(similarity, 3))
                    )

        return duplicates

    def _find_orphan_pages(self, db_conn) -> list[GapItem]:
        """
        Find pages that have no internal links pointing to them.
        Requires the internal_links table to be populated during crawl.
        """
        cursor = db_conn.cursor()
        cursor.execute(
            """
            SELECT p.url, p.title FROM pages p
            WHERE p.url NOT IN (SELECT DISTINCT target_url FROM internal_links)
            """
        )
        rows = cursor.fetchall()
        return [
            GapItem(
                url=row["url"],
                title=row["title"] or "",
                issue="No internal links point to this page (orphan page)",
                severity="low",
            )
            for row in rows
        ]