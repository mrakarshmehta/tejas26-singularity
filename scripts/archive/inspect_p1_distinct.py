import sys
import os
import csv
sys.path.insert(0, '.')
from scratch.inspect_p0_p1 import uninserted_p0_p1

sys.stdout.reconfigure(encoding='utf-8')

print("\n=== TOP UNINSERTED P1 CANDIDATES (SORTED BY MIN DISTANCE DESCENDING) ===")
p1_list = [c for c in uninserted_p0_p1 if c['rec_priority'] == 'P1']
# filter for candidates with min_dist >= 5 km to avoid immediate cluster overlap
p1_distinct = [c for c in p1_list if c['min_dist'] >= 3.0]

for idx, c in enumerate(p1_distinct):
    print(f"{idx+1:2d}. {c['name']:<42} | {c['district']:<15} | {c['category']:<12} | {c['min_dist']:>6.2f} km | {c['nearest_p']}")

