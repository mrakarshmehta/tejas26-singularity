import sys, os
sys.path.insert(0, os.path.abspath('.'))
from dotenv import load_dotenv
load_dotenv()

from models.connection import get_cursor

def audit():
    with get_cursor() as cur:
        # 1. District count and list with all details
        cur.execute("SELECT id, name, slug, image_url, cover_image, is_visible FROM districts ORDER BY id")
        districts = cur.fetchall()
        print(f"=== ALL DISTRICTS IN DB ({len(districts)} Total) ===")
        for d in districts:
            print(f"  ID: {d['id']:2d} | Name: {d['name']:22s} | Slug: {d['slug']:20s} | Visible: {d['is_visible']}")

        # 2. Places count per district ID
        cur.execute("""
            SELECT d.id, d.name as district_name, d.slug as district_slug, COUNT(p.id) as place_count 
            FROM districts d 
            LEFT JOIN places p ON d.id = p.district_id AND p.deleted_at IS NULL
            GROUP BY d.id, d.name, d.slug
            ORDER BY d.id
        """)
        counts = cur.fetchall()
        print("\n=== PLACES COUNT PER DISTRICT ===")
        for c in counts:
            print(f"  ID: {c['id']:2d} | Name: {c['district_name']:22s} | Slug: {c['district_slug']:20s} | Places: {c['place_count']}")

        # 3. Jamui details
        print("\n=== JAMUI SEARCH IN DISTRICTS ===")
        cur.execute("SELECT * FROM districts WHERE name LIKE '%Jamui%' OR slug LIKE '%jamui%'")
        for d in cur.fetchall():
            print(f"  ID: {d['id']} | Name: {d['name']} | Slug: {d['slug']} | Image: {d['image_url']} | Cover: {d['cover_image']}")

        # 4. Check places assigned to district ID 4 (Name: Jamui, Slug: nalanda) vs District ID 22 (Name: Kaimur, Slug: jamui) vs places with Jamui in text
        print("\n=== PLACES WITH district_id = 4 (District Name: Jamui) ===")
        cur.execute("SELECT id, name, slug, category, description, cover_image FROM places WHERE district_id = 4 AND deleted_at IS NULL")
        for p in cur.fetchall():
            print(f"  ID: {p['id']} | Name: {p['name']} | Slug: {p['slug']} | Cat: {p['category']} | Desc: {(p['description'] or '')[:60]}")

        print("\n=== PLACES WITH district_id = 22 (District Slug: jamui, Name: Kaimur) ===")
        cur.execute("SELECT id, name, slug, category, description, cover_image FROM places WHERE district_id = 22 AND deleted_at IS NULL")
        for p in cur.fetchall():
            print(f"  ID: {p['id']} | Name: {p['name']} | Slug: {p['slug']} | Cat: {p['category']} | Desc: {(p['description'] or '')[:60]}")

        print("\n=== PLACES WITH 'Jamui' IN NAME OR DESCRIPTION ===")
        cur.execute("SELECT id, name, slug, district_id, category, description FROM places WHERE (name LIKE '%Jamui%' OR description LIKE '%Jamui%') AND deleted_at IS NULL")
        for p in cur.fetchall():
            print(f"  ID: {p['id']} | Name: {p['name']} | DistID: {p['district_id']} | Desc: {(p['description'] or '')[:60]}")

        # 5. Search for placeholder / empty / suspicious entries across ALL places
        print("\n=== ALL PLACES WITH PLACEHOLDER / 'Please add' / EMPTY DESCRIPTIONS ===")
        cur.execute("""
            SELECT p.id, p.name, p.slug, p.district_id, d.name as district_name, p.description, p.cover_image 
            FROM places p
            LEFT JOIN districts d ON p.district_id = d.id
            WHERE p.deleted_at IS NULL AND (
               p.name LIKE '%Please add%' 
               OR p.description LIKE '%Please add%'
               OR p.name LIKE '%placeholder%'
               OR p.description LIKE '%placeholder%'
               OR p.name LIKE '%TBD%'
               OR p.description LIKE '%TBD%'
               OR p.description IS NULL
               OR TRIM(p.description) = ''
            )
        """)
        suspicious = cur.fetchall()
        print(f"Found {len(suspicious)} suspicious entries:")
        for s in suspicious:
            print(f"  ID: {s['id']:3d} | Name: {s['name']:35s} | DistID: {s['district_id']} ({s['district_name']}) | Desc: {(s['description'] or 'NULL')[:60]}")

        # 6. Check for ALL places in the DB
        cur.execute("SELECT COUNT(*) as total FROM places WHERE deleted_at IS NULL")
        total_p = cur.fetchone()['total']
        print(f"\n=== TOTAL ACTIVE PLACES IN DB: {total_p} ===")

if __name__ == '__main__':
    audit()
