import sys
sys.path.insert(0, 'scratch')
from inspect_p0_p1_remaining import uninserted_p0_p1
p0s = [r for r in uninserted_p0_p1 if r.get('recommended_priority') == 'P0']
print(f"Uninserted P0 count: {len(p0s)}")
for r in p0s:
    print(f"[{r.get('district')}] {r.get('place_name')} | Cat: {r.get('category')} | Coords: {r.get('coordinates')}")
    print(f"   Primary: {r.get('primary_source')}")
    print(f"   Reason: {r.get('reason')}")
    print()
