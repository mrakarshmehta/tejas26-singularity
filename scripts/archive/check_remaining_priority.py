import sys
import os
import csv
import re
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()

# 1. Fetch all 148 active places
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
""")
active_places = cur.fetchall()
active_names = {p['name'].lower().strip(): p for p in active_places}
active_slugs = {p['slug'].lower().strip(): p for p in active_places}

def clean_toks(name):
    s = re.sub(r'[^\w\s]', ' ', name.lower())
    return set(w for w in s.split() if len(w) > 2 and w not in ['the', 'and', 'for', 'temple', 'mandir', 'fort', 'sanctuary', 'lake', 'park', 'bihar', 'district'])

print(f"Loaded {len(active_places)} active places from DB.")

# Load candidates from BIHAR_PRIORITY_APPROVAL_QUEUE.csv
candidates = []
with open('BIHAR_PRIORITY_APPROVAL_QUEUE.csv', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pname = row.get('place_name', '').strip()
        dist = row.get('district', '').strip()
        cat = row.get('category', '').strip()
        prio = row.get('priority', '').strip()
        source = row.get('primary_source_name', '').strip()
        source_url = row.get('primary_source_url', '').strip()
        why = row.get('why_it_deserves_priority', '').strip()
        evidence = row.get('evidence_strength', '').strip()
        
        # Check if already active
        is_active = False
        matched_active = None
        if pname.lower() in active_names:
            is_active = True
            matched_active = active_names[pname.lower()]
        else:
            ctoks = clean_toks(pname)
            for aname, ap in active_names.items():
                atoks = clean_toks(aname)
                if ctoks and atoks and (ctoks == atoks or (len(ctoks) >= 2 and ctoks.issubset(atoks)) or (len(atoks) >= 2 and atoks.issubset(ctoks))):
                    if dist.lower() == ap['district_name'].lower():
                        is_active = True
                        matched_active = ap
                        break
        
        candidates.append({
            'name': pname,
            'district': dist,
            'category': cat,
            'priority': prio,
            'source': source,
            'source_url': source_url,
            'why': why,
            'evidence': evidence,
            'is_active': is_active,
            'matched_active': matched_active
        })

print(f"Total candidates in PRIORITY queue: {len(candidates)}")
active_in_queue = sum(1 for c in candidates if c['is_active'])
print(f"Already active in DB: {active_in_queue}")
remaining = [c for c in candidates if not c['is_active']]
print(f"Remaining candidates in PRIORITY queue: {len(remaining)}")

# Print remaining candidates grouped by district
from collections import defaultdict
by_dist = defaultdict(list)
for c in remaining:
    by_dist[c['district']].append(c)

print("\n--- REMAINING CANDIDATES BY DISTRICT ---")
for d, c_list in sorted(by_dist.items()):
    print(f"\nDistrict: {d} ({len(c_list)} candidates):")
    for c in c_list:
        print(f"  - [{c['priority']}] {c['name']} ({c['category']}) | {c['evidence'][:35]} | {c['why'][:60]}...")
