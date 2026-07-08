"""
Pages routes — List and retrieve crawled pages.

Endpoints:
    GET /api/pages           — List all crawled pages (paginated)
    GET /api/pages/{page_id} — Get a single page's details
"""

from fastapi import APIRouter, Depends, Query

from app.models.page import PageResponse, PageListResponse
from app.api.dependencies import get_db

router = APIRouter()


@router.get("", response_model=PageListResponse)
async def list_pages(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str = Query(None, description="Filter by keyword in title/URL"),
    db=Depends(get_db),
):
    """
    List all crawled pages with pagination and optional keyword filter.
    """
    # TODO: Query pages from SQLite with pagination
    return PageListResponse(pages=[], total=0, page=page, per_page=per_page)


@router.get("/{page_id}", response_model=PageResponse)
async def get_page(page_id: int, db=Depends(get_db)):
    """
    Get full details for a single crawled page.
    """
    # TODO: Query single page by ID
    return PageResponse(
        id=page_id,
        url="",
        title="",
        meta_description="",
        h1="",
        body_text="",
        canonical_url="",
        crawl_date=None,
        word_count=0,
    )
