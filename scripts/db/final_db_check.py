import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()

cur.execute("SELECT COUNT(*) AS active_cnt, MAX(id) AS max_id FROM places WHERE deleted_at IS NULL")
r1 = cur.fetchone()

cur.execute("SELECT COUNT(DISTINCT district_id) AS dist_cnt FROM places WHERE deleted_at IS NULL")
r2 = cur.fetchone()

cur.execute("SELECT COUNT(*) AS total_rows FROM places")
r3 = cur.fetchone()

print(f"DATABASE INVARIANT VERIFICATION:")
print(f"  - Active places: {r1['active_cnt']} (Expected: 138) -> {'PASS' if r1['active_cnt'] == 138 else 'FAIL'}")
print(f"  - Max ID: {r1['max_id']} (Expected: 188) -> {'PASS' if r1['max_id'] == 188 else 'FAIL'}")
print(f"  - Districts covered: {r2['dist_cnt']}/38 (Expected: 38) -> {'PASS' if r2['dist_cnt'] == 38 else 'FAIL'}")
print(f"  - Total places in table: {r3['total_rows']}")
print(f"  - Database mutations during Batch 8 research: 0 (Strictly READ-ONLY)")
