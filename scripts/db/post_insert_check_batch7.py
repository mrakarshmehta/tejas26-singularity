import sys
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, '.')
from models.connection import get_cursor

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=" * 80)
    print("POST-INSERT DATABASE VALIDATION FOR BATCH 7")
    print("=" * 80)
    
    with get_cursor() as cursor:
        # 1. Total Active Places
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        total_active = cursor.fetchone()['cnt']
        print(f"1. Total active places: {total_active} (Expected: 138)")
        assert total_active == 138, f"Expected 138, got {total_active}"

        # 2. Districts Covered
        cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
        districts_covered = cursor.fetchone()['cnt']
        print(f"2. Districts covered: {districts_covered}/38")
        assert districts_covered == 38, f"Expected 38, got {districts_covered}"

        # 3. Max Place ID
        cursor.execute("SELECT MAX(id) as max_id FROM places WHERE deleted_at IS NULL")
        max_id = cursor.fetchone()['max_id']
        print(f"3. Max place ID: {max_id} (Expected: 188)")
        assert max_id == 188, f"Expected 188, got {max_id}"

        # 4. Batch 7 Inserted Rows
        cursor.execute("""
            SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name
            FROM places p
            JOIN districts d ON p.district_id = d.id
            WHERE p.id BETWEEN 179 AND 188
            ORDER BY p.id ASC
        """)
        batch7_rows = cursor.fetchall()
        print(f"\n4. Batch 7 inserted records (Count: {len(batch7_rows)}):")
        expected_places = [
            (179, "Bhitiharwa Gandhi Ashram", 9, "historical", 27.2437, 84.4838, "bhitiharwa-gandhi-ashram-west-champaran"),
            (180, "Baba Mahendra Nath Temple, Mehdar", 35, "temple", 25.9870, 84.4380, "baba-mahendra-nath-temple-mehdar-siwan"),
            (181, "Jaimangla Garh", 15, "historical", 25.5921, 86.1613, "jaimangla-garh-begusarai"),
            (182, "Ramrekha Ghat", 17, "cultural", 25.5761, 83.9711, "ramrekha-ghat-buxar"),
            (183, "Aganoor Mini Hydroelectric Project", 12, "tourist_spot", 25.1328, 84.5385, "aganoor-mini-hydroelectric-project-arwal"),
            (184, "Raja Bali Ka Garh", 20, "historical", 26.4595, 86.3230, "raja-bali-ka-garh-madhubani"),
            (185, "Dr. Rajendra Prasad Central Agricultural University", 30, "historical", 25.9860, 85.6754, "dr-rajendra-prasad-central-agricultural-university-samastipur"),
            (186, "Baba Vishu Raut Temple, Pachrasi Dham", 27, "cultural", 25.4450, 87.0250, "baba-vishu-raut-temple-pachrasi-dham-madhepura"),
            (187, "Kanhaiya Ji Mandir, Bandarjhula", 25, "historical", 26.3683, 87.9636, "kanhaiya-ji-mandir-bandarjhula-kishanganj"),
            (188, "Gautam Asthan, Revelganj", 31, "cultural", 25.7812, 84.6712, "gautam-asthan-revelganj-saran")
        ]

        for row, exp in zip(batch7_rows, expected_places):
            print(f"   ID {row['id']}: {row['name']} | Dist: {row['district_name']} ({row['district_id']}) | Cat: {row['category']} | Coords: {row['latitude']},{row['longitude']} | Slug: {row['slug']}")
            assert row['id'] == exp[0], f"ID mismatch: {row['id']} != {exp[0]}"
            assert row['name'] == exp[1], f"Name mismatch: {row['name']} != {exp[1]}"
            assert row['district_id'] == exp[2], f"District ID mismatch: {row['district_id']} != {exp[2]}"
            assert row['category'] == exp[3], f"Category mismatch: {row['category']} != {exp[3]}"
            assert abs(float(row['latitude']) - exp[4]) < 1e-4, f"Latitude mismatch: {row['latitude']} != {exp[4]}"
            assert abs(float(row['longitude']) - exp[5]) < 1e-4, f"Longitude mismatch: {row['longitude']} != {exp[5]}"
            assert row['slug'] == exp[6], f"Slug mismatch: {row['slug']} != {exp[6]}"

        # 5. Duplicate Check across all 138 active places
        cursor.execute("SELECT name, COUNT(*) as cnt FROM places WHERE deleted_at IS NULL GROUP BY name HAVING cnt > 1")
        dupe_names = cursor.fetchall()
        print(f"\n5. Duplicate names: {len(dupe_names)} (Must be 0)")
        assert len(dupe_names) == 0, f"Duplicate names found: {dupe_names}"

        cursor.execute("SELECT slug, COUNT(*) as cnt FROM places WHERE deleted_at IS NULL GROUP BY slug HAVING cnt > 1")
        dupe_slugs = cursor.fetchall()
        print(f"6. Duplicate slugs: {len(dupe_slugs)} (Must be 0)")
        assert len(dupe_slugs) == 0, f"Duplicate slugs found: {dupe_slugs}"

        cursor.execute("SELECT latitude, longitude, COUNT(*) as cnt FROM places WHERE deleted_at IS NULL GROUP BY latitude, longitude HAVING cnt > 1")
        dupe_coords = cursor.fetchall()
        print(f"7. Duplicate coordinates: {len(dupe_coords)} (Must be 0)")
        assert len(dupe_coords) == 0, f"Duplicate coordinates found: {dupe_coords}"

        # 8. Foreign Key Integrity Check
        cursor.execute("""
            SELECT p.id, p.name, p.district_id 
            FROM places p 
            LEFT JOIN districts d ON p.district_id = d.id 
            WHERE p.deleted_at IS NULL AND d.id IS NULL
        """)
        orphans = cursor.fetchall()
        print(f"8. Orphan places with invalid district_id: {len(orphans)} (Must be 0)")
        assert len(orphans) == 0, f"Orphan places found: {orphans}"

        # 9. Invariance of prior 128 active records (IDs 1-178)
        cursor.execute("""
            SELECT COUNT(*) as cnt 
            FROM places 
            WHERE id <= 178 AND deleted_at IS NULL
        """)
        prior_active = cursor.fetchone()['cnt']
        print(f"9. Prior active places (IDs <= 178): {prior_active} (Must be 128)")
        assert prior_active == 128, f"Prior active count changed: {prior_active} != 128"

        print("\n" + "=" * 80)
        print("ALL POST-INSERT DATABASE INTEGRITY CHECKS PASSED PERFECTLY!")
        print("=" * 80)

if __name__ == '__main__':
    main()
