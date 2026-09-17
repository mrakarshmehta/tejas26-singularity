"""
Read-only audit of Bihar Blocks in MySQL database for Phase 2D.
"""

import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))
from models.connection import get_db

def run_audit():
    print("=" * 60)
    print("  PHASE 2D BLOCKS AUDIT (READ-ONLY)")
    print("=" * 60)

    with get_db() as db:
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM blocks")
        total_blocks = cursor.fetchone()['cnt']
        print(f"\n1. Total blocks in DB: {total_blocks}")

        cursor.execute("SELECT COUNT(*) as cnt FROM districts WHERE state_id = 1")
        total_districts = cursor.fetchone()['cnt']
        print(f"2. Total districts in Bihar (state_id=1): {total_districts}")

        # Block count per district
        cursor.execute("""
            SELECT d.id as district_id, d.name as district_name, d.slug as district_slug, COUNT(b.id) as block_count
            FROM districts d
            LEFT JOIN blocks b ON d.id = b.district_id
            WHERE d.state_id = 1
            GROUP BY d.id, d.name, d.slug
            ORDER BY d.id
        """)
        districts = cursor.fetchall()
        print(f"\n3. District-wise Block Distribution ({len(districts)} districts):")
        total_counted = 0
        for d in districts:
            print(f"   [{d['district_id']:2d}] {d['district_name']:<20} ({d['district_slug']:<20}): {d['block_count']:2d} blocks")
            total_counted += d['block_count']
        print(f"   Total Counted: {total_counted}")

        # Duplicate block names across different districts
        cursor.execute("""
            SELECT b.name, COUNT(*) as cnt, GROUP_CONCAT(d.name ORDER BY d.name SEPARATOR ', ') as district_names
            FROM blocks b
            JOIN districts d ON b.district_id = d.id
            GROUP BY b.name
            HAVING cnt > 1
            ORDER BY cnt DESC, b.name
        """)
        shared_names = cursor.fetchall()
        print(f"\n4. Duplicate Block Names Across Different Districts: {len(shared_names)}")
        for s in shared_names[:15]:
            print(f"   '{s['name']}': in {s['cnt']} districts -> ({s['district_names']})")

        # Duplicate slugs
        cursor.execute("""
            SELECT b.slug, COUNT(*) as cnt, GROUP_CONCAT(d.name ORDER BY d.name SEPARATOR ', ') as district_names
            FROM blocks b
            JOIN districts d ON b.district_id = d.id
            GROUP BY b.slug
            HAVING cnt > 1
            ORDER BY cnt DESC
        """)
        dup_slugs = cursor.fetchall()
        print(f"\n5. Duplicate Slugs in blocks table: {len(dup_slugs)}")
        for ds in dup_slugs[:10]:
            print(f"   Slug '{ds['slug']}': {ds['cnt']} blocks -> ({ds['district_names']})")

        # Columns in blocks table
        cursor.execute("DESCRIBE blocks")
        columns = cursor.fetchall()
        print("\n6. Blocks Table Schema:")
        for col in columns:
            print(f"   - {col['Field']:<15} {col['Type']:<15} Null={col['Null']} Key={col['Key']} Default={col['Default']}")

        # Sample records
        cursor.execute("""
            SELECT b.id, b.name, b.slug, b.district_id, d.name as district_name
            FROM blocks b
            JOIN districts d ON b.district_id = d.id
            LIMIT 5
        """)
        samples = cursor.fetchall()
        print("\n7. Sample Block Records:")
        for s in samples:
            print(f"   ID {s['id']}: {s['name']} (slug: {s['slug']}) in {s['district_name']} (district_id: {s['district_id']})")

        # Places linked to blocks
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE block_id IS NOT NULL")
        places_with_block = cursor.fetchone()['cnt']
        cursor.execute("SELECT COUNT(*) as cnt FROM places")
        total_places = cursor.fetchone()['cnt']
        print(f"\n8. Places with block_id assigned: {places_with_block} / {total_places}")

if __name__ == "__main__":
    run_audit()
