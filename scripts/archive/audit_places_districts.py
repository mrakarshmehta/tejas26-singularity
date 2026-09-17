import sys, os
sys.path.insert(0, os.path.abspath('.'))
from dotenv import load_dotenv
load_dotenv()

from models.connection import get_cursor

def audit_places():
    with get_cursor() as cur:
        cur.execute("""
            SELECT p.id, p.name, p.district_id, d.name as current_dist_name, d.slug as current_dist_slug
            FROM places p
            LEFT JOIN districts d ON p.district_id = d.id
            WHERE p.deleted_at IS NULL
            ORDER BY p.id
        """)
        places = cur.fetchall()
        print(f"=== ALL PLACES ({len(places)} total) WITH CURRENT DISTRICT ASSIGNMENT ===")
        for p in places:
            print(f"Place ID: {p['id']:3d} | Name: {p['name']:40s} | DistID: {p['district_id']} | Dist Name: {str(p['current_dist_name']):22s} | Dist Slug: {str(p['current_dist_slug'])}")

audit_places()
