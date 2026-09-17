import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

print("=== DISTRICT TABLE SCHEMA ===")
with get_cursor() as cur:
    cur.execute('DESCRIBE districts')
    for r in cur.fetchall():
        print(f"  {r['Field']:25s} {r['Type']:30s} {r['Null']:5s} {r['Key']:5s}")

print("\n=== PLACE TABLE SCHEMA ===")
with get_cursor() as cur:
    cur.execute('DESCRIBE places')
    for r in cur.fetchall():
        print(f"  {r['Field']:25s} {r['Type']:30s} {r['Null']:5s} {r['Key']:5s}")

print("\n=== COUNTS ===")
with get_cursor() as cur:
    cur.execute('SELECT COUNT(*) as c FROM places WHERE latitude IS NOT NULL AND longitude IS NOT NULL AND deleted_at IS NULL')
    print(f"  Places with coordinates: {cur.fetchone()['c']}")

with get_cursor() as cur:
    cur.execute('SELECT COUNT(*) as c FROM districts')
    print(f"  Districts: {cur.fetchone()['c']}")

with get_cursor() as cur:
    cur.execute('SELECT COUNT(*) as c FROM states')
    print(f"  States: {cur.fetchone()['c']}")

with get_cursor() as cur:
    cur.execute("SHOW TABLES LIKE 'nearby_services'")
    if cur.fetchone():
        cur.execute('SELECT COUNT(*) as c FROM nearby_services WHERE latitude IS NOT NULL')
        print(f"  Nearby services with coords: {cur.fetchone()['c']}")
    else:
        print("  nearby_services table: NOT FOUND")

with get_cursor() as cur:
    cur.execute("SHOW TABLES LIKE 'blocks'")
    if cur.fetchone():
        cur.execute('SELECT COUNT(*) as c FROM blocks')
        print(f"  Blocks: {cur.fetchone()['c']}")
    else:
        print("  blocks table: NOT FOUND")

with get_cursor() as cur:
    cur.execute("SHOW TABLES LIKE 'host_listings'")
    if cur.fetchone():
        cur.execute('SELECT COUNT(*) as c FROM host_listings WHERE latitude IS NOT NULL AND status = %s', ('published',))
        print(f"  Host listings with coords: {cur.fetchone()['c']}")

print("\n=== CATEGORY DISTRIBUTION ===")
with get_cursor() as cur:
    cur.execute('SELECT category, COUNT(*) as c FROM places WHERE latitude IS NOT NULL AND longitude IS NOT NULL AND deleted_at IS NULL GROUP BY category ORDER BY c DESC')
    for r in cur.fetchall():
        print(f"  {r['category'] or 'NULL':25s} {r['c']}")

print("\n=== DISTRICT SAMPLE (first 5) ===")
with get_cursor() as cur:
    cur.execute('SELECT id, name, state_id FROM districts LIMIT 5')
    for r in cur.fetchall():
        print(f"  ID {r['id']:3d}: {r['name']} (state_id={r['state_id']})")
