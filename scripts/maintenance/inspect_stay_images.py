import sys
import os
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

print("=== HOST LISTINGS ===")
with get_cursor() as cur:
    cur.execute("""
        SELECT hl.id, hl.title, hl.slug, hl.status, hl.cover_image, hl.district_id, d.name AS district_name
        FROM host_listings hl
        LEFT JOIN districts d ON hl.district_id = d.id
        ORDER BY hl.id ASC
    """)
    listings = cur.fetchall()
    for l in listings:
        print(f"ID {l['id']}: '{l['title']}' (slug: {l['slug']}) | status={l['status']} | cover_image={repr(l['cover_image'])} | district={l['district_name']}")

print("\n=== SCHEMA OF host_listings ===")
with get_cursor() as cur:
    cur.execute("DESCRIBE host_listings")
    for col in cur.fetchall():
        print(f"  {col['Field']}: {col['Type']} | Null={col['Null']} | Default={col['Default']}")

print("\n=== SCHEMA OF listing_photos ===")
with get_cursor() as cur:
    cur.execute("DESCRIBE listing_photos")
    for col in cur.fetchall():
        print(f"  {col['Field']}: {col['Type']} | Null={col['Null']} | Default={col['Default']}")

print("\n=== ALL ROWS IN listing_photos ===")
with get_cursor() as cur:
    cur.execute("SELECT * FROM listing_photos")
    photos = cur.fetchall()
    print(f"Total rows in listing_photos: {len(photos)}")
    for p in photos:
        print(f"  {p}")

print("\n=== FILES ON DISK ===")
listings_dir = r"d:\HiddenYatra\static\uploads\hosts\listings"
if os.path.exists(listings_dir):
    files = os.listdir(listings_dir)
    print(f"Directory {listings_dir} has {len(files)} files:")
    for f in files:
        fpath = os.path.join(listings_dir, f)
        print(f"  - {f} ({os.path.getsize(fpath)} bytes)")
else:
    print(f"Directory {listings_dir} does NOT exist!")

profiles_dir = r"d:\HiddenYatra\static\uploads\hosts\profiles"
if os.path.exists(profiles_dir):
    files = os.listdir(profiles_dir)
    print(f"\nDirectory {profiles_dir} has {len(files)} files:")
    for f in files:
        fpath = os.path.join(profiles_dir, f)
        print(f"  - {f} ({os.path.getsize(fpath)} bytes)")
