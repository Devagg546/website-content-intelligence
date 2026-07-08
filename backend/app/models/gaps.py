"""
Gaps models — Schemas for content gap detection and SEO issues.
"""

from pydantic import BaseModel, Field


class GapItem(BaseModel):
    """A single content gap or SEO issue."""

    url: str = Field(..., description="Page URL with the issue")
    title: str = Field(default="", description="Page title (if available)")
    issue: str = Field(default="", description="Description of the issue")
    severity: str = Field(
        default="medium",
        description="Issue severity: low | medium | high | critical",
    )


class DuplicatePair(BaseModel):
    """A pair of pages with highly similar content."""

    url_a: str = Field(..., description="First page URL")
    url_b: str = Field(..., description="Second page URL")
    similarity_score: float = Field(
        ..., ge=0.0, le=1.0, description="Content similarity score"
    )


class GapsResponse(BaseModel):
    """Content gap detection report."""

    missing_title: list[GapItem] = Field(
        default_factory=list, description="Pages missing title tags"
    )
    missing_meta_description: list[GapItem] = Field(
        default_factory=list, description="Pages missing meta descriptions"
    )
    missing_h1: list[GapItem] = Field(
        default_factory=list, description="Pages missing H1 tags"
    )
    thin_content: list[GapItem] = Field(
        default_factory=list, description="Pages with thin content (below threshold)"
    )
    duplicate_content: list[DuplicatePair] = Field(
        default_factory=list, description="Pages with highly similar content"
    )
    orphan_pages: list[GapItem] = Field(
        default_factory=list, description="Pages with no internal links"
    )
    total_issues: int = Field(default=0, description="Total number of issues detected")
