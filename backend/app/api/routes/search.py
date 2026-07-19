"""
Search routes — Keyword and semantic content search.
"""

from fastapi import APIRouter, Depends

from app.models.search import SearchRequest, SearchResponse
from app.api.dependencies import get_db
from app.services.search_service import SearchService

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search_content(
    request: SearchRequest,
    db=Depends(get_db),
):
    """
    Search crawled content using keyword matching, semantic similarity, or hybrid.
    """
    service = SearchService(db)
    return service.search(request)