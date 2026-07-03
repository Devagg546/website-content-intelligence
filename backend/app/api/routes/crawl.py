"""
Crawl routes — Start and monitor website crawl jobs.

Endpoints:
    POST /api/crawl          — Start a new crawl job
    GET  /api/crawl/status/{job_id} — Get crawl job status
    GET  /api/crawl/history  — List past crawl jobs
"""

from fastapi import APIRouter, BackgroundTasks, Depends

from app.models.crawl import CrawlRequest, CrawlResponse, CrawlStatusResponse
from app.api.dependencies import get_db

router = APIRouter()


@router.post("", response_model=CrawlResponse)
async def start_crawl(
    request: CrawlRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
):
    """
    Start a new website crawl job.

    Accepts a URL and optional max_pages parameter.
    The crawl runs in the background using FastAPI's BackgroundTasks.
    Returns a job ID immediately so the frontend doesn't hang.
    """
    # TODO: Implement crawl job creation and background task
    # 1. Create crawl job record in DB
    # 2. Add crawler.run() to background tasks
    # 3. Return job ID
    return CrawlResponse(
        job_id="placeholder-uuid",
        status="started",
        message="Crawl job started",
    )


@router.get("/status/{job_id}", response_model=CrawlStatusResponse)
async def get_crawl_status(job_id: str, db=Depends(get_db)):
    """
    Check the status of a crawl job.

    Returns current progress including pages crawled, total discovered,
    and job status (queued, in_progress, completed, failed).
    """
    # TODO: Query crawl job status from DB
    return CrawlStatusResponse(
        job_id=job_id,
        status="in_progress",
        pages_crawled=0,
        pages_total=0,
        started_at=None,
        completed_at=None,
    )


@router.get("/history")
async def get_crawl_history(db=Depends(get_db)):
    """
    List all past crawl jobs with their status and summary.
    """
    # TODO: Query crawl history from DB
    return {"jobs": []}
