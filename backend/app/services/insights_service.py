"""
Insights Service — AI-powered content intelligence.

Generates insights such as:
- Topics covered across the website
- Content distribution by topic
- Frequently mentioned entities (brands, locations, services, products)
"""

import re
from collections import Counter, defaultdict

from app.models.insights import InsightsResponse, TopicItem, DistributionItem, EntityGroup

TOPIC_KEYWORDS = {
    "Dining": ["restaurant", "dining", "cuisine", "chef", "menu", "bar", "breakfast", "culinary"],
    "Wellness & Spa": ["spa", "wellness", "yoga", "massage", "therapy", "fitness", "meditation"],
    "Rooms & Suites": ["room", "suite", "villa", "accommodation", "bedroom", "view"],
    "Weddings & Events": ["wedding", "event", "banquet", "conference", "celebration", "venue"],
    "Sustainability": ["sustainability", "sustainable", "eco", "environment", "green", "conservation"],
    "Awards & Recognition": ["award", "recognition", "honoured", "honored", "accolade", "achievement"],
    "News & Press": ["news", "press", "release", "announcement", "media"],
    "Offers & Packages": ["offer", "discount", "deal", "package", "promotion"],
    "Locations & Destinations": ["destination", "location", "travel", "explore", "discover"],
}

KNOWN_LOCATIONS = [
    "India", "Delhi", "Mumbai", "Jaipur", "Udaipur", "Agra", "Shimla", "Gurgaon",
    "Chandigarh", "Bangalore", "Kolkata", "Egypt", "Bali", "Mauritius", "Dubai",
    "London", "Ranthambhore", "Sahl Hasheesh", "Khajuraho",
]

SERVICE_KEYWORDS = [
    "Spa", "Dining", "Wedding", "Conference", "Wellness", "Yoga", "Concierge",
    "Butler Service", "Airport Transfer", "Room Service",
]

PRODUCT_KEYWORDS = [
    "Suite", "Villa", "Membership", "Package", "Gift Card", "Voucher",
]


class InsightsService:
    """Generates AI-powered content insights from crawled data."""

    def generate_insights(self, db_conn) -> InsightsResponse:
        cursor = db_conn.cursor()
        cursor.execute("SELECT url, title, h1, body_text FROM pages")
        pages = cursor.fetchall()

        topics = self._identify_topics(pages)
        distribution = self._calculate_distribution(pages, topics)
        entities = self._extract_entities(pages)

        return InsightsResponse(
            topics=topics,
            content_distribution=distribution,
            frequent_entities=entities,
        )

    def _identify_topics(self, pages) -> list[TopicItem]:
        topic_pages = defaultdict(list)

        for page in pages:
            text = f"{page['title'] or ''} {page['h1'] or ''} {page['body_text'] or ''}".lower()

            for topic_name, keywords in TOPIC_KEYWORDS.items():
                match_count = sum(1 for kw in keywords if kw in text)
                if match_count >= 2:
                    topic_pages[topic_name].append(page["url"])

        topics = []
        for topic_name, urls in topic_pages.items():
            topics.append(TopicItem(
                name=topic_name,
                page_count=len(urls),
                sample_urls=urls[:5],
            ))

        topics.sort(key=lambda t: t.page_count, reverse=True)
        return topics

    def _calculate_distribution(self, pages, topics: list[TopicItem]) -> list[DistributionItem]:
        total_pages = len(pages)
        if total_pages == 0:
            return []

        distribution = []
        for topic in topics:
            percentage = round((topic.page_count / total_pages) * 100, 1)
            distribution.append(DistributionItem(
                topic=topic.name,
                percentage=percentage,
                page_count=topic.page_count,
            ))

        return distribution

    def _extract_entities(self, pages) -> dict[str, list[EntityGroup]]:
        location_counter = Counter()
        location_pages = defaultdict(set)
        service_counter = Counter()
        service_pages = defaultdict(set)
        product_counter = Counter()
        product_pages = defaultdict(set)
        brand_counter = Counter()
        brand_pages = defaultdict(set)

        for page in pages:
            text = page["body_text"] or ""
            url = page["url"]

            for loc in KNOWN_LOCATIONS:
                count = text.count(loc)
                if count > 0:
                    location_counter[loc] += count
                    location_pages[loc].add(url)

            for svc in SERVICE_KEYWORDS:
                count = text.lower().count(svc.lower())
                if count > 0:
                    service_counter[svc] += count
                    service_pages[svc].add(url)

            for prod in PRODUCT_KEYWORDS:
                count = text.lower().count(prod.lower())
                if count > 0:
                    product_counter[prod] += count
                    product_pages[prod].add(url)

            brand_matches = re.findall(r"\bOberoi\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?", text)
            for match in brand_matches:
                brand_counter[match] += 1
                brand_pages[match].add(url)

        def top_n(counter, pages_map, n=10):
            return [
                EntityGroup(name=name, count=count, pages=list(pages_map[name])[:5])
                for name, count in counter.most_common(n)
            ]

        return {
            "brands": top_n(brand_counter, brand_pages),
            "locations": top_n(location_counter, location_pages),
            "services": top_n(service_counter, service_pages),
            "products": top_n(product_counter, product_pages),
        }