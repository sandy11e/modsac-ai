from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import trafilatura
from pathlib import Path

START_URL = "https://www.mosdac.gov.in"
MAX_PAGES = 30
RAW_DIR = Path("data/raw"); RAW_DIR.mkdir(parents=True, exist_ok=True)

visited = set()
to_visit = [START_URL]
page_count = 0

while to_visit and page_count < MAX_PAGES:
    url = to_visit.pop(0)
    if url in visited or not url.startswith(START_URL):
        continue
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        main_text = trafilatura.extract(res.text)
        if not main_text: continue
        domain = urlparse(url).netloc.replace(".", "_")
        slug = urlparse(url).path.strip("/").replace("/", "_") or "index"
        filename = f"{domain}__{slug}.txt"
        (RAW_DIR / filename).write_text(main_text)
        page_count += 1
        print(f"[{page_count}] Saved: {url}")
        # Find more links
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if link not in visited and link.startswith(START_URL):
                to_visit.append(link)
        visited.add(url)
    except Exception as e:
        print(f"Failed: {url} ({e})")

print("✅ Done crawling.")
