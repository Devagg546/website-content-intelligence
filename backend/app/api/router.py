"""
Central API router that aggregates all route modules.
"""

from fastapi import APIRouter

from app.api.routes import crawl, pages, ask, search, inventory, gaps, insights

api_router = APIRouter()

# ── Register all route modules ───────────────────────────────────────────
api_router.include_router(crawl.router, prefix="/crawl", tags=["Crawl"])
api_router.include_router(pages.router, prefix="/pages", tags=["Pages"])
api_router.include_router(ask.router, prefix="/ask", tags=["Ask AI"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(gaps.router, prefix="/gaps", tags=["Gaps"])
api_router.include_router(insights.router, prefix="/insights", tags=["Insights"])
