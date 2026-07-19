"""
Insights models — Schemas for AI-generated content intelligence.
"""

from pydantic import BaseModel, Field


class TopicItem(BaseModel):
    """A topic identified in the website content."""

    name: str = Field(..., description="Topic name")
    page_count: int = Field(default=0, description="Number of pages covering this topic")
    sample_urls: list[str] = Field(
        default_factory=list, description="Sample page URLs for this topic"
    )


class DistributionItem(BaseModel):
    """Content distribution by topic."""

    topic: str = Field(..., description="Topic name")
    percentage: float = Field(
        ..., ge=0.0, le=100.0, description="Percentage of total content"
    )
    page_count: int = Field(default=0, description="Number of pages")


class EntityGroup(BaseModel):
    """A group of frequently mentioned entities."""

    name: str = Field(..., description="Entity name")
    count: int = Field(default=0, description="Number of mentions")
    pages: list[str] = Field(
        default_factory=list, description="Pages mentioning this entity"
    )


class InsightsResponse(BaseModel):
    """AI-generated content insights report."""

    topics: list[TopicItem] = Field(
        default_factory=list, description="Topics covered on the website"
    )
    content_distribution: list[DistributionItem] = Field(
        default_factory=list, description="Content distribution by topic"
    )
    frequent_entities: dict[str, list[EntityGroup]] = Field(
        default_factory=dict,
        description="Frequently mentioned entities grouped by type",
    )