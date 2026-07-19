"""
Insights routes — AI-generated content intelligence.
"""

from fastapi import APIRouter, Depends

from app.models.insights import InsightsResponse
from app.api.dependencies import get_db
from app.services.insights_service import InsightsService

router = APIRouter()


@router.get("", response_model=InsightsResponse)
async def get_content_insights(db=Depends(get_db)):
    """
    Generate AI-powered content insights.
    """
    service = InsightsService()
    return service.generate_insights(db)