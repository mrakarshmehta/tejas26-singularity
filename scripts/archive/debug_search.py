import sys
sys.path.insert(0, '.')
from models.search_engine import get_search_index

idx = get_search_index()
idx.build()

res = idx.search("Bhitiharwa")
print(f"Total results: {len(res)}")
for r in res:
    print(f"ID: {r.get('id')} | Name: {r.get('name')} | Match Type: {r.get('match_type')} | Score: {r.get('score')}")
