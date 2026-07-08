"""
Search models — Schemas for content search operations.
"""

from typing import Literal

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Request schema for content search."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Search query string",
        examples=["spa wellness"],
    )
    search_type: Literal["keyword", "semantic", "hybrid"] = Field(
        default="hybrid",
        description="Type of search: keyword, semantic, or hybrid",
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of results to return",
    )


class SearchResult(BaseModel):
    """A single search result."""

    page_title: str = Field(..., description="Title of the matching page")
    url: str = Field(..., description="URL of the matching page")
    snippet: str = Field(..., description="Relevant text snippet with match context")
    score: float = Field(default=0.0, description="Relevance score")


class SearchResponse(BaseModel):
    """Response schema for search results."""

    results: list[SearchResult] = Field(default_factory=list)
    total: int = Field(default=0, description="Total number of matching results")
    query: str = Field(default="", description="The original search query")
    search_type: str = Field(default="hybrid", description="Search type used")
