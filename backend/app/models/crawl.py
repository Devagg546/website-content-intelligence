"""
Crawl models — Request/response schemas for crawl operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class CrawlRequest(BaseModel):
    """Request schema for starting a new crawl job."""

    url: str = Field(
        ...,
        description="The root URL of the website to crawl",
        examples=["https://www.oberoihotels.com"],
    )
    max_pages: int = Field(
        default=500,
        ge=1,
        le=500,
        description="Maximum number of pages to crawl",
    )


class CrawlResponse(BaseModel):
    """Response schema returned when a crawl job is created."""

    job_id: str = Field(..., description="Unique identifier for the crawl job")
    status: str = Field(..., description="Current status of the crawl job")
    message: str = Field(..., description="Human-readable status message")


class CrawlStatusResponse(BaseModel):
    """Response schema for crawl job status queries."""

    job_id: str = Field(..., description="Unique identifier for the crawl job")
    status: str = Field(
        ...,
        description="Job status: queued | in_progress | completed | failed",
    )
    pages_crawled: int = Field(default=0, description="Number of pages crawled so far")
    pages_total: int = Field(default=0, description="Total pages discovered")
    started_at: Optional[datetime] = Field(None, description="When the crawl started")
    completed_at: Optional[datetime] = Field(None, description="When the crawl finished")
    error_message: Optional[str] = Field(None, description="Error details if failed")


class CrawlJobSummary(BaseModel):
    """Summary of a crawl job for history listing."""

    job_id: str
    url: str
    status: str
    pages_crawled: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
