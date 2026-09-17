import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.search_engine import get_search_index, instant_search

idx = get_search_index()
print(f"Index size: {idx.size}")
entries = [e for e in idx._entries if 'saurath' in e.name.lower()]
print(f"Entries matching saurath: {len(entries)}")
for e in entries:
    print(f"  {e.id}: {e.name} ({e.district_name})")

results = instant_search('Saurath')
print(f"\ninstant_search('Saurath') results: {len(results)}")
for r in results:
    print(f"  {r}")
