"""
FastAPI application entry point.

Sets up the application with:
- CORS middleware
- Lifespan events (DB init, ChromaDB init)
- Router inclusion
- Swagger docs configuration
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.router import api_router
from app.db.sqlite_db import init_database
from app.db.vector_store import init_vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Runs initialization on startup and cleanup on shutdown.
    """
    # ── Startup ──────────────────────────────────────────────────────
    print(f"🚀 Starting {settings.app_name}...")

    # Initialize SQLite database and tables
    init_database()
    print("✅ SQLite database initialized")

    # Initialize ChromaDB vector store
    init_vector_store()
    print("✅ ChromaDB vector store initialized")

    print(f"✅ {settings.app_name} is ready!")

    yield

    # ── Shutdown ─────────────────────────────────────────────────────
    print(f"👋 Shutting down {settings.app_name}...")


def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        description=(
            "AI-powered RAG platform that crawls websites, indexes content, "
            "and enables natural language Q&A with source citations."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── CORS Middleware ──────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Include API Router ───────────────────────────────────────────
    app.include_router(api_router, prefix="/api")

    # ── Health Check ─────────────────────────────────────────────────
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Basic health check endpoint."""
        return {
            "status": "healthy",
            "app": settings.app_name,
            "version": "1.0.0",
        }

    return app


# Create the application instance
app = create_app()
