import sys
import os
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor
import csv

with get_cursor() as cursor:
    cursor.execute("""
        SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name 
        FROM places p 
        JOIN districts d ON p.district_id = d.id 
        WHERE p.deleted_at IS NULL 
        ORDER BY p.id
    """)
    active_places = cursor.fetchall()

print(f"Total active places in DB: {len(active_places)}")

# Load PHASE6_TOP30_FACTCHECK.csv
with open('PHASE6_TOP30_FACTCHECK.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    top30 = list(reader)

print("\n=== PHASE6_TOP30_FACTCHECK Status Check ===")
not_inserted_top30 = []

for idx, row in enumerate(top30):
    name = str(row.get('place_name', '')).strip()
    district = str(row.get('district', '')).strip()
    verdict = str(row.get('final_verdict', '')).strip()
    matched = None
    for p in active_places:
        p_name = p['name'].lower()
        c_name = name.lower()
        if (c_name in p_name or p_name in c_name):
            matched = p
            break
        # also match by tokens
        tokens_c = set(c_name.replace('&', '').replace(',', '').split())
        tokens_p = set(p_name.replace('&', '').replace(',', '').split())
        common = tokens_c.intersection(tokens_p)
        if len(common) >= 3 or (len(common) >= 2 and 'temple' not in common and 'fort' not in common and 'sanctuary' not in common):
            matched = p
            break
    if matched:
        print(f"Rank {row.get('rank', idx+1):>2}: {name:<48} ({district:<15}) -> INSERTED (ID {matched['id']}: {matched['name']})")
    else:
        print(f"Rank {row.get('rank', idx+1):>2}: {name:<48} ({district:<15}) -> PENDING / NOT INSERTED [Verdict: {verdict}]")
        not_inserted_top30.append(row)

print(f"\nTotal Pending / Not Inserted in Top 30: {len(not_inserted_top30)}")
print("\n--- Details of Pending Top 30 Candidates ---")
for r in not_inserted_top30:
    print(f"Rank {r.get('rank')}: {r.get('place_name')} | District: {r.get('district')} | Cat: {r.get('category')} | Lat/Lng: {r.get('latitude')},{r.get('longitude')} | Verdict: {r.get('final_verdict')} | Reason: {r.get('reason')}")
