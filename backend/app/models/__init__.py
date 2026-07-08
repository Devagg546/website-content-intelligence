"""Pydantic models package — request/response schemas for all API endpoints."""

from app.models.crawl import CrawlRequest, CrawlResponse, CrawlStatusResponse
from app.models.page import PageResponse, PageListResponse
from app.models.ask import AskRequest, AskResponse, Citation
from app.models.search import SearchRequest, SearchResponse, SearchResult
from app.models.inventory import InventoryResponse, KeywordStat, PageStat
from app.models.gaps import GapsResponse, GapItem, DuplicatePair
from app.models.insights import InsightsResponse, TopicItem, DistributionItem

__all__ = [
    "CrawlRequest", "CrawlResponse", "CrawlStatusResponse",
    "PageResponse", "PageListResponse",
    "AskRequest", "AskResponse", "Citation",
    "SearchRequest", "SearchResponse", "SearchResult",
    "InventoryResponse", "KeywordStat", "PageStat",
    "GapsResponse", "GapItem", "DuplicatePair",
    "InsightsResponse", "TopicItem", "DistributionItem",
]
