"""
Page models — Schemas for crawled page data.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PageResponse(BaseModel):
    """Full details of a single crawled page."""

    id: int = Field(..., description="Page ID in the database")
    url: str = Field(..., description="Full URL of the page")
    title: str = Field(default="", description="Page title tag content")
    meta_description: str = Field(default="", description="Meta description content")
    h1: str = Field(default="", description="First H1 tag content")
    body_text: str = Field(default="", description="Extracted body text content")
    canonical_url: Optional[str] = Field(None, description="Canonical URL if present")
    crawl_date: Optional[datetime] = Field(None, description="When the page was crawled")
    word_count: int = Field(default=0, description="Number of words in body text")


class PageListResponse(BaseModel):
    """Paginated list of crawled pages."""

    pages: list[PageResponse] = Field(default_factory=list)
    total: int = Field(default=0, description="Total number of pages")
    page: int = Field(default=1, description="Current page number")
    per_page: int = Field(default=20, description="Items per page")
