import os
import json
from crawler.crawler import crawl_faq

os.makedirs("data/processed", exist_ok=True)

faqs = crawl_faq()

with open("data/processed/faqs.json", "w", encoding="utf-8") as f:
    json.dump(faqs, f, indent=2, ensure_ascii=False)

print(f"✅ {len(faqs)} FAQs saved to data/processed/faqs.json")
