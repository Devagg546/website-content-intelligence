"""
Pages routes — List and retrieve crawled pages.
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
    cursor = db.cursor()

    # Build query with optional search filter
    base_query = "FROM pages"
    params = []

    if search:
        base_query += " WHERE title LIKE ? OR url LIKE ?"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])

    # Get total count
    cursor.execute(f"SELECT COUNT(*) {base_query}", params)
    total = cursor.fetchone()[0]

    # Get paginated results
    offset = (page - 1) * per_page
    query = f"""
        SELECT id, url, title, meta_description, h1, body_text,
               canonical_url, crawl_date, word_count
        {base_query}
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """
    cursor.execute(query, params + [per_page, offset])
    rows = cursor.fetchall()

    pages_list = [
        PageResponse(
            id=row["id"],
            url=row["url"],
            title=row["title"] or "",
            meta_description=row["meta_description"] or "",
            h1=row["h1"] or "",
            body_text=row["body_text"] or "",
            canonical_url=row["canonical_url"],
            crawl_date=row["crawl_date"],
            word_count=row["word_count"] or 0,
        )
        for row in rows
    ]

    return PageListResponse(pages=pages_list, total=total, page=page, per_page=per_page)


@router.get("/{page_id}", response_model=PageResponse)
async def get_page(page_id: int, db=Depends(get_db)):
    """
    Get full details for a single crawled page.
    """
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT id, url, title, meta_description, h1, body_text,
               canonical_url, crawl_date, word_count
        FROM pages WHERE id = ?
        """,
        (page_id,),
    )
    row = cursor.fetchone()

    if not row:
        return PageResponse(id=page_id, url="", title="", word_count=0)

    return PageResponse(
        id=row["id"],
        url=row["url"],
        title=row["title"] or "",
        meta_description=row["meta_description"] or "",
        h1=row["h1"] or "",
        body_text=row["body_text"] or "",
        canonical_url=row["canonical_url"],
        crawl_date=row["crawl_date"],
        word_count=row["word_count"] or 0,
    )