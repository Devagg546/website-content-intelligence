# API Reference

Base URL: `http://localhost:8000/api`

---

## Crawl

### `POST /api/crawl`
Start a new website crawl job.

**Request Body:**
```json
{
  "url": "https://www.example.com",
  "max_pages": 500
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "started",
  "message": "Crawl job started"
}
```

### `GET /api/crawl/status/{job_id}`
Check crawl job progress.

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "in_progress",
  "pages_crawled": 42,
  "pages_total": 150,
  "started_at": "2024-01-01T00:00:00Z"
}
```

---

## Pages

### `GET /api/pages`
List all crawled pages with pagination.

**Query Parameters:**
- `page` (int, default: 1)
- `per_page` (int, default: 20)
- `search` (string, optional)

**Response:**
```json
{
  "pages": [...],
  "total": 150,
  "page": 1,
  "per_page": 20
}
```

---

## Ask AI

### `POST /api/ask`
Ask a natural language question about crawled content.

**Request Body:**
```json
{
  "question": "What pages discuss sustainability?"
}
```

**Response:**
```json
{
  "answer": "The website discusses sustainability in 8 locations...",
  "citations": [
    {
      "page_title": "Sustainability Initiatives",
      "url": "https://example.com/sustainability",
      "snippet": "...our commitment to sustainability...",
      "relevance_score": 0.92
    }
  ]
}
```

---

## Search

### `POST /api/search`
Search content by keyword or semantic similarity.

**Request Body:**
```json
{
  "query": "spa wellness",
  "search_type": "hybrid"
}
```

**Response:**
```json
{
  "results": [
    {
      "page_title": "Wellness Spa",
      "url": "https://example.com/spa",
      "snippet": "...luxury spa treatments...",
      "score": 0.89
    }
  ],
  "total": 5
}
```

---

## Inventory

### `GET /api/inventory`
Get content inventory statistics.

**Response:**
```json
{
  "total_pages": 150,
  "total_words": 245000,
  "avg_content_length": 1633,
  "top_keywords": [...],
  "largest_pages": [...],
  "smallest_pages": [...]
}
```

---

## Gaps

### `GET /api/gaps`
Detect content gaps and SEO issues.

**Response:**
```json
{
  "missing_title": [...],
  "missing_meta_description": [...],
  "missing_h1": [...],
  "thin_content": [...],
  "duplicate_content": [...],
  "orphan_pages": [...]
}
```

---

## Insights

### `GET /api/insights`
Get AI-generated content insights.

**Response:**
```json
{
  "topics": [...],
  "content_distribution": [...],
  "frequent_entities": {
    "brands": [...],
    "locations": [...],
    "services": [...]
  }
}
```
