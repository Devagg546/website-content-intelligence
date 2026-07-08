"""
Insights routes — AI-generated content intelligence.

Endpoints:
    GET /api/insights — Get AI-generated content insights
"""

from fastapi import APIRouter, Depends

from app.models.insights import InsightsResponse
from app.api.dependencies import get_db

router = APIRouter()


@router.get("", response_model=InsightsResponse)
async def get_content_insights(db=Depends(get_db)):
    """
    Generate AI-powered content insights:
    - Topics covered across the website
    - Content distribution by topic
    - Frequently mentioned entities (brands, locations, services, products)
    """
    # TODO: Implement insights service
    return InsightsResponse(
        topics=[],
        content_distribution=[],
        frequent_entities={
            "brands": [],
            "locations": [],
            "services": [],
            "products": [],
        },
    )
