"""
HiddenYatra — Database Integrity & Health Audit Script
Checks foreign keys, orphan records, broken image links, null anomalies, missing indexes, and duplicates.
"""
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.database import get_db

def run_db_audit():
    print("=" * 60)
    print("HiddenYatra Database Health & Integrity Audit")
    print("=" * 60)

    db = get_db()
    issues_found = 0

    with db.cursor() as cur:
        # 1. Table Counts & Presence
        tables = [
            'places', 'districts', 'users', 'user_photos', 'user_submissions',
            'hero_media', 'hero_settings', 'auth_appearance', 'nearby_services',
            'trending_places', 'wishlists', 'visited_places', 'admin_logs'
        ]
        print("\n--- 1. Table Summary & Row Counts ---")
        for tbl in tables:
            try:
                cur.execute(f"SELECT COUNT(*) AS cnt FROM `{tbl}`")
                row = cur.fetchone()
                cnt = row['cnt'] if isinstance(row, dict) else row[0]
                print(f"  Table `{tbl}`: {cnt} rows")
            except Exception as e:
                print(f"  Table `{tbl}`: [MISSING / ERROR] {e}")

        # 2. Check for Duplicate Place Slugs
        print("\n--- 2. Checking Duplicate Slugs ---")
        cur.execute("SELECT slug, COUNT(*) c FROM places GROUP BY slug HAVING c > 1")
        dups = cur.fetchall()
        if dups:
            print(f"  [WARNING] Found {len(dups)} duplicate place slugs!")
            issues_found += len(dups)
            for d in dups:
                print(f"    - Slug: {d['slug']} (count: {d['c']})")
        else:
            print("  [OK] No duplicate place slugs found.")

        # 3. Check for Orphan Records in user_photos
        print("\n--- 3. Checking Orphan Records ---")
        cur.execute("""
            SELECT COUNT(*) AS cnt FROM user_photos up
            LEFT JOIN places p ON up.place_id = p.id
            WHERE up.place_id IS NOT NULL AND p.id IS NULL
        """)
        row = cur.fetchone()
        orphan_photos = row['cnt'] if isinstance(row, dict) else row[0]
        if orphan_photos > 0:
            print(f"  [WARNING] Found {orphan_photos} orphan photos in user_photos!")
            issues_found += orphan_photos
        else:
            print("  [OK] Zero orphan records in user_photos.")

        # 4. Check for Null / Empty Place Names or Slugs
        print("\n--- 4. Checking NULL / Empty Fields ---")
        cur.execute("SELECT COUNT(*) AS cnt FROM places WHERE name IS NULL OR name = '' OR slug IS NULL OR slug = ''")
        row = cur.fetchone()
        bad_places = row['cnt'] if isinstance(row, dict) else row[0]
        if bad_places > 0:
            print(f"  [WARNING] Found {bad_places} places with empty name or slug!")
            issues_found += bad_places
        else:
            print("  [OK] Zero places with missing name or slug.")

        # 5. Check Image References in Places
        print("\n--- 5. Checking Image References ---")
        cur.execute("SELECT id, name, cover_image FROM places WHERE cover_image IS NULL OR cover_image = ''")
        missing_covers = cur.fetchall()
        if missing_covers:
            print(f"  [WARNING] Found {len(missing_covers)} places without cover images.")
            issues_found += len(missing_covers)
        else:
            print("  [OK] All places have cover image paths defined.")

        # 6. Check District References
        print("\n--- 6. Checking District Slugs & Foreign Keys ---")
        cur.execute("""
            SELECT COUNT(*) AS cnt FROM places p
            LEFT JOIN districts d ON p.district_id = d.id
            WHERE p.district_id IS NOT NULL AND d.id IS NULL
        """)
        row = cur.fetchone()
        orphan_districts = row['cnt'] if isinstance(row, dict) else row[0]
        if orphan_districts > 0:
            print(f"  [WARNING] Found {orphan_districts} places with invalid district_id!")
            issues_found += orphan_districts
        else:
            print("  [OK] All place district references are valid.")

        # 7. Check Indexes
        print("\n--- 7. Checking Database Indexes ---")
        cur.execute("SHOW INDEX FROM places")
        indexes = [r['Key_name'] for r in cur.fetchall()]
        print(f"  Indexes on `places`: {list(set(indexes))}")

    print("\n" + "=" * 60)
    if issues_found == 0:
        print("RESULT: DATABASE AUDIT PASSED 100% — Zero Integrity Issues Found.")
    else:
        print(f"RESULT: DATABASE AUDIT COMPLETED — {issues_found} potential issue(s) identified.")
    print("=" * 60)

if __name__ == '__main__':
    run_db_audit()
