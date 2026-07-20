"""
Application configuration using Pydantic BaseSettings.
All settings are loaded from environment variables or .env file.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Application ──────────────────────────────────────────────────────
    app_name: str = "Content Intelligence Assistant"
    app_env: str = "development"
    debug: bool = True

    # ── Server ───────────────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # ── Database ─────────────────────────────────────────────────────────
    sqlite_db_path: str = "data/content_intelligence.db"

    # ── ChromaDB ─────────────────────────────────────────────────────────
    chroma_persist_dir: str = "data/chromadb"
    chroma_collection_name: str = "website_content"

    # ── Embeddings ───────────────────────────────────────────────────────
    embedding_model: str = "all-MiniLM-L6-v2"

    # ── Crawler ──────────────────────────────────────────────────────────
    max_crawl_pages: int = 500
    crawl_delay_ms: int = 1000
    browser_headless: bool = True

    # ── LLM ──────────────────────────────────────────────────────────────
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    anthropic_api_key: str = ""
    google_api_key: str = ""
    gemini_model: str = "gemini-flash-latest"

    # ── RAG ──────────────────────────────────────────────────────────────
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def db_path(self) -> Path:
        """Get the absolute path to the SQLite database."""
        return Path(self.sqlite_db_path)

    @property
    def chroma_path(self) -> Path:
        """Get the absolute path to the ChromaDB persistence directory."""
        return Path(self.chroma_persist_dir)


# Singleton settings instance
settings = Settings()
