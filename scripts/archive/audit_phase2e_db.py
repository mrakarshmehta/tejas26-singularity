"""
Read-only audit script for Phase 2E: Hotels and Homestays in HiddenYatra.
"""

import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))
from models.connection import get_db

def audit_database():
    print("=" * 60)
    print("  PHASE 2E DATABASE AUDIT: HOTELS & HOMESTAYS")
    print("=" * 60)

    with get_db() as db:
        cursor = db.cursor()

        # 1. Check all tables in DB
        cursor.execute("SHOW TABLES")
        tables = [list(r.values())[0] for r in cursor.fetchall()]
        print(f"\n[1] All Database Tables ({len(tables)}):")
        print(f"    {tables}")

        # 2. Check places table for hotel-like places
        print("\n[2] Inspecting `places` table categories and records...")
        cursor.execute("DESCRIBE places")
        places_cols = [r['Field'] for r in cursor.fetchall()]
        print(f"    Columns in places: {places_cols}")

        cursor.execute("""
            SELECT category, COUNT(*) as cnt
            FROM places
            GROUP BY category
            ORDER BY cnt DESC
        """)
        cats = cursor.fetchall()
        print("    Categories in places:")
        for c in cats:
            print(f"      - {c['category']}: {c['cnt']}")

        # 3. Check for specific hotel/stay tables
        stay_tables = [t for t in tables if any(k in t.lower() for k in ['stay', 'hotel', 'listing', 'host', 'room', 'accommodat'])]
        print(f"\n[3] Stay/Accommodation/Host Tables Found: {stay_tables}")

        for st in stay_tables:
            print(f"\n--- Table: {st} ---")
            cursor.execute(f"DESCRIBE `{st}`")
            cols = cursor.fetchall()
            for c in cols:
                print(f"    {c['Field']} ({c['Type']}) Nullable={c['Null']} Key={c['Key']}")
            
            cursor.execute(f"SELECT COUNT(*) as total FROM `{st}`")
            total = cursor.fetchone()['total']
            print(f"    Total rows: {total}")

            # Sample records
            cursor.execute(f"SELECT * FROM `{st}` LIMIT 3")
            samples = cursor.fetchall()
            for s in samples:
                # Sanitize password / tokens if any
                clean_sample = {k: v for k, v in s.items() if 'password' not in k.lower() and 'token' not in k.lower()}
                print(f"    Sample: {clean_sample}")

if __name__ == "__main__":
    audit_database()
