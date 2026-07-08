"""
Search routes — Keyword and semantic content search.

Endpoints:
    POST /api/search — Search content by keyword or semantic similarity
"""

from fastapi import APIRouter, Depends

from app.models.search import SearchRequest, SearchResponse
from app.api.dependencies import get_db, get_chroma

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search_content(
    request: SearchRequest,
    db=Depends(get_db),
):
    """
    Search crawled content using keyword matching, semantic similarity, or hybrid.

    Supports three search types:
    - keyword: Traditional text matching with highlighting
    - semantic: Vector similarity search via ChromaDB
    - hybrid: Combined keyword + semantic ranking
    """
    # TODO: Implement search service
    return SearchResponse(results=[], total=0)
