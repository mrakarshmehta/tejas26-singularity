"""
Phase 2 Comprehensive Data Extractor - 100% Read-Only.
Generates structured JSON data for all tables and relationships.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

# 1. Districts
cur.execute("""
    SELECT d.id, d.state_id, d.name, d.slug, d.description, d.famous_for,
           d.cover_image, d.image_url, d.sort_order, d.is_featured, d.is_visible,
           COUNT(DISTINCT p.id) AS place_count,
           COUNT(DISTINCT b.id) AS block_count
    FROM districts d
    LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
    LEFT JOIN blocks b ON b.district_id = d.id
    GROUP BY d.id
    ORDER BY d.id
""")
districts = cur.fetchall()

# 2. Places
cur.execute("""
    SELECT p.id, p.state_id, p.district_id, p.block_id, p.name, p.slug,
           p.category, p.cover_image, p.latitude, p.longitude,
           p.is_featured, p.deleted_at,
           d.name AS dist_name, d.slug AS dist_slug,
           b.name AS block_name
    FROM places p
    LEFT JOIN districts d ON p.district_id = d.id
    LEFT JOIN blocks b ON p.block_id = b.id
    ORDER BY p.id
""")
places = cur.fetchall()

# 3. Blocks
cur.execute("""
    SELECT b.id, b.district_id, b.name, b.slug,
           d.name AS dist_name, d.slug AS dist_slug,
           COUNT(p.id) AS place_count
    FROM blocks b
    LEFT JOIN districts d ON b.district_id = d.id
    LEFT JOIN places p ON p.block_id = b.id AND p.deleted_at IS NULL
    GROUP BY b.id
    ORDER BY b.district_id, b.id
""")
blocks = cur.fetchall()

# 4. District Foods
cur.execute("""
    SELECT df.id, df.district_id, df.name, df.description, df.image_url,
           d.name AS dist_name, d.slug AS dist_slug
    FROM district_foods df
    LEFT JOIN districts d ON df.district_id = d.id
    ORDER BY df.district_id, df.id
""")
foods = cur.fetchall()

# 5. Nearby Services
cur.execute("""
    SELECT s.*,
           d.name AS dist_name, d.slug AS dist_slug
    FROM nearby_services s
    LEFT JOIN districts d ON s.district_id = d.id
    ORDER BY s.district_id, s.id
""")
services = cur.fetchall()

cur.close()
conn.close()

# Save complete JSON audit
audit_data = {
    "districts": districts,
    "places": places,
    "blocks": blocks,
    "foods": foods,
    "services": services
}

with open(r"D:\HiddenYatra\scratch\audit_dump.json", "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2, default=str)

print("✅ Saved complete audit dump to scratch/audit_dump.json")
print(f"Districts: {len(districts)}")
print(f"Places: {len(places)}")
print(f"Blocks: {len(blocks)}")
print(f"Foods: {len(foods)}")
print(f"Services: {len(services)}")
