"""
Crawl routes — Start and monitor website crawl jobs.
"""

import sqlite3
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends

from app.models.crawl import CrawlRequest, CrawlResponse, CrawlStatusResponse
from app.api.dependencies import get_db
from app.services.crawler.crawler import WebCrawler, CrawlJob
from app.services.processing.cleaner import ContentCleaner
from app.services.processing.chunker import TextChunker
from app.services.processing.embedder import get_embedder
from app.db.vector_store import add_documents

router = APIRouter()

# In-memory job store for tracking active jobs
_active_jobs: dict[str, CrawlJob] = {}


def run_crawl_pipeline(job: CrawlJob, db_path: str):
    """
    Full crawl pipeline — runs in background:
    1. Crawl website pages
    2. Clean and chunk content
    3. Generate embeddings
    4. Store in ChromaDB and SQLite
    """
    import sqlite3
    from pathlib import Path

    try:
        crawler = WebCrawler()
        cleaner = ContentCleaner()
        chunker = TextChunker()
        embedder = get_embedder()

        # Step 1 — Crawl
        pages = crawler.crawl(job)

        # Connect to SQLite
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Save crawl job to DB
        cursor.execute("""
            INSERT OR REPLACE INTO crawl_jobs
            (job_id, root_url, status, max_pages, pages_crawled, started_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (job.job_id, job.root_url, job.status, job.max_pages,
              len(pages), job.started_at))
        conn.commit()

        all_ids = []
        all_documents = []
        all_embeddings = []
        all_metadatas = []

        for page in pages:
            # Step 2 — Save page to SQLite
            word_count = len(page.get("body_text", "").split())
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO pages
                    (url, title, meta_description, h1, body_text,
                     canonical_url, word_count, crawl_job_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    page.get("url", ""),
                    page.get("title", ""),
                    page.get("meta_description", ""),
                    page.get("h1", ""),
                    page.get("body_text", ""),
                    page.get("canonical_url", ""),
                    word_count,
                    job.job_id,
                ))
            except Exception as e:
                print(f"DB insert error for {page.get('url')}: {e}")
                continue

            # Step 3 — Clean and chunk
            body_text = page.get("body_text", "")
            if not body_text or len(body_text.strip()) < 50:
                continue

            metadata = {
                "url": page.get("url", ""),
                "title": page.get("title", ""),
                "meta_description": page.get("meta_description", ""),
                "h1": page.get("h1", ""),
                "crawl_date": page.get("crawl_date", ""),
            }

            chunks = chunker.chunk_text(body_text, metadata)

            for chunk in chunks:
                chunk_id = f"{page.get('url', '')}#chunk{chunk['chunk_index']}"
                text = chunk["content"]

                all_ids.append(chunk_id)
                all_documents.append(text)
                all_metadatas.append(chunk["metadata"])

        conn.commit()
        conn.close()

        # Step 4 — Generate embeddings in batch and store in ChromaDB
        if all_documents:
            print(f"Generating embeddings for {len(all_documents)} chunks...")
            all_embeddings = embedder.embed_texts(all_documents)

            add_documents(
                ids=all_ids,
                documents=all_documents,
                embeddings=all_embeddings,
                metadatas=all_metadatas,
            )
            print(f"Stored {len(all_documents)} chunks in ChromaDB")

        job.status = "completed"
        job.completed_at = datetime.now()
        print(f"Pipeline complete for job {job.job_id}")

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        print(f"Crawl pipeline failed: {e}")


@router.post("", response_model=CrawlResponse)
async def start_crawl(
    request: CrawlRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
):
    """Start a new website crawl job."""
    from app.config import settings
    from pathlib import Path

    job = CrawlJob(url=request.url, max_pages=request.max_pages)
    _active_jobs[job.job_id] = job

    db_path = str(Path(settings.sqlite_db_path).absolute())
    background_tasks.add_task(run_crawl_pipeline, job, db_path)

    return CrawlResponse(
        job_id=job.job_id,
        status="started",
        message=f"Crawl started for {request.url}",
    )


@router.get("/status/{job_id}", response_model=CrawlStatusResponse)
async def get_crawl_status(job_id: str, db=Depends(get_db)):
    """Check the status of a crawl job."""
    job = _active_jobs.get(job_id)

    if not job:
        return CrawlStatusResponse(
            job_id=job_id,
            status="not_found",
            pages_crawled=0,
            pages_total=0,
        )

    return CrawlStatusResponse(
        job_id=job.job_id,
        status=job.status,
        pages_crawled=job.pages_crawled,
        pages_total=job.max_pages,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error_message=job.error_message,
    )


@router.get("/history")
async def get_crawl_history(db=Depends(get_db)):
    """List all past crawl jobs."""
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT job_id, root_url, status, pages_crawled,
                   started_at, completed_at
            FROM crawl_jobs
            ORDER BY started_at DESC
            LIMIT 20
        """)
        jobs = [dict(row) for row in cursor.fetchall()]
        return {"jobs": jobs}
    except Exception as e:
        return {"jobs": [], "error": str(e)}