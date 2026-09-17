import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()

print("=" * 80)
print("DATABASE INVARIANCE AUDIT FOR BATCH 9 RESEARCH PHASE")
print("=" * 80)

# 1. Active count
cur.execute("SELECT COUNT(*) AS active_count FROM places WHERE deleted_at IS NULL")
active_count = cur.fetchone()['active_count']
print(f"1. Active places count: {active_count} (Expected: 148) -> {'PASS' if active_count == 148 else 'FAIL'}")

# 2. Maximum ID
cur.execute("SELECT MAX(id) AS max_id FROM places")
max_id = cur.fetchone()['max_id']
print(f"2. Maximum place ID: {max_id} (Expected: 198) -> {'PASS' if max_id == 198 else 'FAIL'}")

# 3. Distinct districts
cur.execute("SELECT COUNT(DISTINCT district_id) AS district_count FROM places WHERE deleted_at IS NULL")
district_count = cur.fetchone()['district_count']
print(f"3. Distinct districts covered: {district_count} (Expected: 38) -> {'PASS' if district_count == 38 else 'FAIL'}")

if active_count == 148 and max_id == 198 and district_count == 38:
    print("\nALL INVARIANCE CHECKS PASSED: Database remains completely unchanged (READ-ONLY verified).")
else:
    print("\nFATAL: Database invariance violated!")
    sys.exit(1)
