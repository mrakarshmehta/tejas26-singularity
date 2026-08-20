"""Test search engine with recovered data."""
import os
os.chdir('d:/HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.search_engine import instant_search, rebuild_search_index

n = rebuild_search_index()
print(f"Index size: {n}")

r = instant_search('Jamui', limit=5)
print(f"Results for 'Jamui': {len(r)}")
for x in r:
    print(f"  - {x['name']} ({x.get('category','?')}) [{x.get('district_name','?')}]")

r2 = instant_search('temple', limit=5)
print(f"\nResults for 'temple': {len(r2)}")
for x in r2:
    print(f"  - {x['name']}")

r3 = instant_search('waterfall', limit=5)
print(f"\nResults for 'waterfall': {len(r3)}")
for x in r3:
    print(f"  - {x['name']}")
