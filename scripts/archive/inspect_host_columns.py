import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cur:
    for table in ['host_profiles', 'host_listings']:
        cur.execute(f"DESCRIBE {table}")
        print(f"\n=== {table} Columns ===")
        for col in cur.fetchall():
            print(f"  {col['Field']:<24} {col['Type']:<20}")

    cur.execute("SELECT * FROM host_listings")
    listings = cur.fetchall()
    print(f"\n=== Current host_listings ({len(listings)} rows) ===")
    for l in listings:
        print(f"  ID {l['id']}: title='{l['title']}' | status='{l['status']}' | price={l['price_per_night']} | district_id={l['district_id']} | cover='{l['cover_image']}'")

    cur.execute("SELECT * FROM host_profiles")
    hosts = cur.fetchall()
    print(f"\n=== Current host_profiles ({len(hosts)} rows) ===")
    for h in hosts:
        print(f"  Host ID {h['id']}: user_id={h['user_id']} | name='{h['display_name']}' | status='{h['verification_status']}' | district_id={h['district_id']}")
