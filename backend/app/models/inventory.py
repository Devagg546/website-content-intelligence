"""
Inventory models — Schemas for content inventory dashboard.
"""

from pydantic import BaseModel, Field


class KeywordStat(BaseModel):
    """Keyword frequency statistic."""

    keyword: str = Field(..., description="The keyword")
    count: int = Field(..., description="Number of occurrences")
    pages: int = Field(default=0, description="Number of pages containing this keyword")


class PageStat(BaseModel):
    """Page-level statistic for largest/smallest pages."""

    url: str = Field(..., description="Page URL")
    title: str = Field(default="", description="Page title")
    word_count: int = Field(..., description="Number of words")


class InventoryResponse(BaseModel):
    """Content inventory report with aggregate statistics."""

    total_pages: int = Field(default=0, description="Total number of crawled pages")
    total_words: int = Field(default=0, description="Total word count across all pages")
    avg_content_length: float = Field(
        default=0.0, description="Average words per page"
    )
    top_keywords: list[KeywordStat] = Field(
        default_factory=list, description="Most frequently used keywords"
    )
    largest_pages: list[PageStat] = Field(
        default_factory=list, description="Pages with most content"
    )
    smallest_pages: list[PageStat] = Field(
        default_factory=list, description="Pages with least content"
    )
