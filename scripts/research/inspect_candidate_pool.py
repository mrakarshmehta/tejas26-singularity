import csv
import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

# 1. Fetch current 138 active places
conn = get_db()
cur = conn.cursor()
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
    ORDER BY p.id
""")
active_places = cur.fetchall()
print(f"Total active places in MySQL: {len(active_places)}")

# 2. Inspect BIHAR_BATCH7_CANDIDATE_STATUS.csv
b7_rows = list(csv.DictReader(open('BIHAR_BATCH7_CANDIDATE_STATUS.csv', encoding='utf-8')))
print(f"\nBIHAR_BATCH7_CANDIDATE_STATUS.csv has {len(b7_rows)} candidates.")
print("\n--- HELD CANDIDATES IN BATCH 7 ---")
for r in b7_rows:
    if r['current_status'] == 'HOLD':
        print(f"• {r['candidate']} | Reason: {r['reason']}")

print("\n--- REJECTED CANDIDATES IN BATCH 7 ---")
for r in b7_rows:
    if r['current_status'] == 'REJECTED':
        print(f"• {r['candidate']} | Reason: {r['reason']}")

print("\n--- DUPLICATE / ALIAS IN BATCH 7 ---")
for r in b7_rows:
    if r['current_status'] == 'DUPLICATE / ALIAS':
        print(f"• {r['candidate']} | Reason: {r['reason']}")

# 3. Check PHASE5_MASTER_CANDIDATE_QUEUE.csv
p5_rows = list(csv.DictReader(open('PHASE5_MASTER_CANDIDATE_QUEUE.csv', encoding='utf-8')))
print(f"\nPHASE5_MASTER_CANDIDATE_QUEUE.csv has {len(p5_rows)} candidates.")

# 4. Check BIHAR_PRIORITY_APPROVAL_QUEUE.csv
prio_rows = list(csv.DictReader(open('BIHAR_PRIORITY_APPROVAL_QUEUE.csv', encoding='utf-8')))
print(f"BIHAR_PRIORITY_APPROVAL_QUEUE.csv has {len(prio_rows)} candidates.")

# 5. Check PHASE6_TOP30_FACTCHECK.csv
p6_rows = list(csv.DictReader(open('PHASE6_TOP30_FACTCHECK.csv', encoding='utf-8')))
print(f"PHASE6_TOP30_FACTCHECK.csv has {len(p6_rows)} candidates.")
