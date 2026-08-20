"""Debug search issue inside Flask context."""
import os, sys
os.chdir('d:/HiddenYatra')
sys.path.insert(0, 'd:/HiddenYatra')
from dotenv import load_dotenv
load_dotenv()

from models.search_engine import get_search_index, sanitize_query, normalize, parse_nl_intent

idx = get_search_index()
idx.build()
print(f"Index size: {idx.size}")
print(f"Built: {idx._built}")
print(f"Entries sample: {[e.name for e in list(idx._entries.values())[:5]]}")

# Simulate search step by step
query = "Jamui"
print(f"\n--- Searching '{query}' ---")
sanitized = sanitize_query(query)
print(f"Sanitized: '{sanitized}'")
normalized = normalize(query)
print(f"Normalized: '{normalized}'")
intent = parse_nl_intent(query)
print(f"Intent: {intent}")

# Try the actual search
results = idx.search(query, limit=5)
print(f"Search results: {len(results)}")
for r in results:
    print(f"  - {r['name']} ({r.get('entry_type','?')})")
