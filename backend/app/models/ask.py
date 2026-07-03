"""
Ask AI models — Schemas for RAG question answering.
"""

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A source citation backing an AI-generated answer."""

    page_title: str = Field(..., description="Title of the source page")
    url: str = Field(..., description="URL of the source page")
    snippet: str = Field(..., description="Relevant text snippet from the source")
    relevance_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Relevance score (0.0 to 1.0)",
    )


class AskRequest(BaseModel):
    """Request schema for asking a question."""

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Natural language question about the website content",
        examples=["What pages discuss sustainability?"],
    )


class AskResponse(BaseModel):
    """Response schema for an AI-generated answer with citations."""

    answer: str = Field(..., description="AI-generated answer")
    citations: list[Citation] = Field(
        default_factory=list,
        description="Source citations backing the answer",
    )
    confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Overall confidence score for the answer",
    )
