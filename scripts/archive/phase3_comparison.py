"""
Phase 3: District by District Comparison Table.
Compares DB state vs expected state for all 38 districts.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("""
    SELECT d.id, d.name, d.slug, d.cover_image,
           COUNT(DISTINCT p.id) AS place_count,
           COUNT(DISTINCT b.id) AS block_count,
           GROUP_CONCAT(DISTINCT p.name SEPARATOR '; ') AS place_names,
           GROUP_CONCAT(DISTINCT b.name SEPARATOR '; ') AS block_names
    FROM districts d
    LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
    LEFT JOIN blocks b ON b.district_id = d.id
    GROUP BY d.id
    ORDER BY d.id
""")
rows = cur.fetchall()

def exp_slug(name):
    import re
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

print("ID | District Name | Current Slug | Expected Slug | Slug Match | Place Count | Current Places Attached | Block Count | Current Blocks Attached")
print("-" * 140)
for r in rows:
    es = exp_slug(r['name'])
    match = "MATCH" if r['slug'] == es else "MISMATCH"
    pnames = (r['place_names'] or 'None')[:40]
    bnames = (r['block_names'] or 'None')[:40]
    print(f"{r['id']:2d} | {r['name']:22s} | {r['slug']:20s} | {es:20s} | {match:8s} | Places: {r['place_count']:2d} ({pnames}...) | Blocks: {r['block_count']:2d} ({bnames}...)")

cur.close()
conn.close()
