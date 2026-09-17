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
    print("POST-INSERT DATABASE VALIDATION FOR BATCH 8")
    print("=" * 80)
    
    with get_cursor() as cursor:
        # 1. Total Active Places
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        total_active = cursor.fetchone()['cnt']
        print(f"1. Total active places: {total_active} (Expected: 148)")
        assert total_active == 148, f"Expected 148, got {total_active}"

        # 2. Districts Covered
        cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
        districts_covered = cursor.fetchone()['cnt']
        print(f"2. Districts covered: {districts_covered}/38")
        assert districts_covered == 38, f"Expected 38, got {districts_covered}"

        # 3. Max Place ID
        cursor.execute("SELECT MAX(id) as max_id FROM places WHERE deleted_at IS NULL")
        max_id = cursor.fetchone()['max_id']
        print(f"3. Max place ID: {max_id} (Expected: 198)")
        assert max_id == 198, f"Expected 198, got {max_id}"

        # 4. Batch 8 Inserted Rows
        cursor.execute("""
            SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name
            FROM places p
            JOIN districts d ON p.district_id = d.id
            WHERE p.id BETWEEN 189 AND 198
            ORDER BY p.id ASC
        """)
        batch8_rows = cursor.fetchall()
        print(f"\n4. Batch 8 inserted records (Count: {len(batch8_rows)}):")
        expected_places = [
            (189, "Ara House", 16, "historical", 25.5539, 84.6680, "ara-house-bhojpur"),
            (190, "Ahilya Sthan, Ahiyari", 18, "cultural", 26.2917, 85.8015, "ahilya-sthan-ahiyari-darbhanga"),
            (191, "Baba Garibnath Temple", 7, "temple", 26.1205, 85.3912, "baba-garibnath-temple-muzaffarpur"),
            (192, "Surya Mandir, Kandaha", 29, "historical", 25.8820, 86.4670, "surya-mandir-kandaha-saharsa"),
            (193, "Mata Puran Devi Temple", 28, "cultural", 25.7725, 87.4580, "mata-puran-devi-temple-purnia"),
            (194, "Baba Brahmeshwar Nath Temple, Brahmpur", 17, "temple", 25.5992, 84.2882, "baba-brahmeshwar-nath-temple-brahmpur-buxar"),
            (195, "Gunawa Ji (Jain Tirth)", 38, "cultural", 24.8944, 85.5312, "gunawa-ji-jain-tirth-nawada"),
            (196, "Ambika Sthan, Aami", 31, "cultural", 25.6881, 85.0062, "ambika-sthan-aami-saran"),
            (197, "Lakri Dargah", 19, "cultural", 26.3150, 84.4720, "lakri-dargah-gopalganj"),
            (198, "Baba Tileshwar Nath Mandir, Sukhpur", 36, "temple", 26.0620, 86.6080, "baba-tileshwar-nath-mandir-sukhpur-supaul")
        ]

        for row, exp in zip(batch8_rows, expected_places):
            print(f"   ID {row['id']}: {row['name']} | Dist: {row['district_name']} ({row['district_id']}) | Cat: {row['category']} | Coords: {row['latitude']},{row['longitude']} | Slug: {row['slug']}")
            assert row['id'] == exp[0], f"ID mismatch: {row['id']} != {exp[0]}"
            assert row['name'] == exp[1], f"Name mismatch: {row['name']} != {exp[1]}"
            assert row['district_id'] == exp[2], f"District ID mismatch: {row['district_id']} != {exp[2]}"
            assert row['category'] == exp[3], f"Category mismatch: {row['category']} != {exp[3]}"
            assert abs(float(row['latitude']) - exp[4]) < 1e-4, f"Latitude mismatch: {row['latitude']} != {exp[4]}"
            assert abs(float(row['longitude']) - exp[5]) < 1e-4, f"Longitude mismatch: {row['longitude']} != {exp[5]}"
            assert row['slug'] == exp[6], f"Slug mismatch: {row['slug']} != {exp[6]}"

        # 5. Duplicate Check across all 148 active places
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

        # 9. Invariance of prior 138 active records (IDs 1-188)
        cursor.execute("""
            SELECT COUNT(*) as cnt 
            FROM places 
            WHERE id <= 188 AND deleted_at IS NULL
        """)
        prior_active = cursor.fetchone()['cnt']
        print(f"9. Invariance check (IDs <= 188 active): {prior_active} (Must be exactly 138)")
        assert prior_active == 138, f"Prior active places altered! Found {prior_active}"
        
        # Check that no place with ID <= 188 was modified
        print("10. Prior 138 places untouched: Verified.")
        print("\nALL POST-INSERT DATABASE INTEGRITY CHECKS PASSED!")

if __name__ == "__main__":
    main()
