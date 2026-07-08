import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def extract_page_data(url, soup):
    
    # Extract title
    title = soup.find("title")
    title = title.get_text(strip=True) if title else "No title found"

    # Extract meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc["content"] if meta_desc else "No meta description found"

    # Extract H1
    h1 = soup.find("h1")
    h1 = h1.get_text(strip=True) if h1 else "No H1 found"

    # Extract canonical URL
    canonical = soup.find("link", attrs={"rel": "canonical"})
    canonical = canonical["href"] if canonical else url

    # Extract body content
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    body = soup.get_text(separator=" ", strip=True)

    return {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "h1": h1,
        "canonical_url": canonical,
        "content_body": body,
        "crawl_date": str(__import__("datetime").date.today())
    }

def get_internal_links(url, soup, base_domain):
    links = set()
    
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)
        
        # Remove fragments like #section
        clean_url = parsed._replace(fragment="").geturl()
        
        # Only keep internal links, ignore everything else
        if parsed.netloc == base_domain and parsed.scheme in ["http", "https"]:
            links.add(clean_url)
    
    return links


def crawl_website(start_url, max_pages=500):
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc
    
    visited = set()
    queue = [start_url]
    all_pages = []

    print(f"Starting crawl on: {start_url}")
    print(f"Base domain: {base_domain}")
    print("-" * 50)

    while queue and len(visited) < max_pages:
        url = queue.pop(0)

        if url in visited:
            continue

        print(f"Crawling ({len(visited) + 1}/{max_pages}): {url}")

        soup = fetch_page(url)
        if soup is None:
            visited.add(url)
            continue

        page_data = extract_page_data(url, soup)
        all_pages.append(page_data)

        new_links = get_internal_links(url, soup, base_domain)
        for link in new_links:
            if link not in visited:
                queue.append(link)

        visited.add(url)

    print("-" * 50)
    print(f"Crawl complete. Total pages crawled: {len(all_pages)}")
    return all_pages

import json

def save_to_json(pages, filename="crawl_output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(pages)} pages to {filename}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
    else:
        start_url = input("Enter website URL to crawl: ")
    
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    
    pages = crawl_website(start_url, max_pages=max_pages)
    save_to_json(pages)