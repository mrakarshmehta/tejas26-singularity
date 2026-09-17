import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from config import GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_MAP_ID, MAP_ENGINE, DB_HOST, DB_NAME
from models.database import get_cursor
import requests

print("=" * 70)
print("DEMO ENVIRONMENT & STARTUP VERIFICATION")
print("=" * 70)

# 1. Credentials Check
print("\n1. GOOGLE MAPS CONFIGURATION:")
has_key = bool(GOOGLE_MAPS_API_KEY and len(GOOGLE_MAPS_API_KEY) > 10)
has_map_id = bool(GOOGLE_MAPS_MAP_ID and len(GOOGLE_MAPS_MAP_ID) > 5)
print(f"  API Key Present: {'✓ YES' if has_key else '✗ NO'} (length={len(GOOGLE_MAPS_API_KEY) if GOOGLE_MAPS_API_KEY else 0})")
print(f"  Map ID Present:  {'✓ YES' if has_map_id else '✗ NO'} ({GOOGLE_MAPS_MAP_ID})")
print(f"  Engine Mode:     {MAP_ENGINE}")

# 2. Database Connection Check
print("\n2. DATABASE CONNECTIVITY:")
try:
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total_places FROM places WHERE deleted_at IS NULL")
        places_count = cur.fetchone()['total_places']
        cur.execute("SELECT COUNT(*) AS total_districts FROM districts WHERE state_id = 1")
        districts_count = cur.fetchone()['total_districts']
        cur.execute("SELECT COUNT(*) AS total_stays FROM host_listings WHERE status = 'approved'")
        stays_count = cur.fetchone()['total_stays']
    print(f"  Database Host: {DB_HOST}, Name: {DB_NAME}")
    print(f"  Connection:    ✓ PASS")
    print(f"  Places:        {places_count}")
    print(f"  Districts:     {districts_count}")
    print(f"  Active Stays:  {stays_count}")
except Exception as e:
    print(f"  Connection:    ✗ FAIL ({e})")

# 3. Server Health
print("\n3. SERVER HEALTH:")
try:
    r = requests.get("http://127.0.0.1:5000/", timeout=5)
    print(f"  GET / -> HTTP {r.status_code} ({len(r.content)} bytes)")
    print(f"  Server Status: ✓ PASS")
except Exception as e:
    print(f"  Server Status: ✗ FAIL ({e})")

print("\n" + "=" * 70)
print("ENVIRONMENT CHECK COMPLETE")
print("=" * 70)
