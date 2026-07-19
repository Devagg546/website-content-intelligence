"""
Gaps routes — Content gap detection and SEO issue reporting.
"""

from fastapi import APIRouter, Depends

from app.models.gaps import GapsResponse
from app.api.dependencies import get_db
from app.services.gap_service import GapService

router = APIRouter()


@router.get("", response_model=GapsResponse)
async def get_content_gaps(db=Depends(get_db)):
    """
    Detect content gaps and SEO issues.
    """
    service = GapService()
    return service.detect_gaps(db)