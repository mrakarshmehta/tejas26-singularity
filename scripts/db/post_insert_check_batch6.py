import sys
import os
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("================================================================================")
    print("POST-INSERT DATABASE VERIFICATION FOR BATCH 6")
    print("================================================================================")
    
    with get_cursor() as cursor:
        # 1. Total Active Places
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        total_active = cursor.fetchone()['cnt']
        print(f"1. Total active places: {total_active} (Expected: 128)")
        assert total_active == 128, f"Expected 128, got {total_active}"

        # 2. Districts Covered
        cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
        districts_covered = cursor.fetchone()['cnt']
        print(f"2. Districts covered: {districts_covered}/38")
        assert districts_covered == 38, f"Expected 38, got {districts_covered}"

        # 3. Max Place ID
        cursor.execute("SELECT MAX(id) as max_id FROM places WHERE deleted_at IS NULL")
        max_id = cursor.fetchone()['max_id']
        print(f"3. Max place ID: {max_id} (Expected: 178)")
        assert max_id == 178, f"Expected 178, got {max_id}"

        # 4. Batch 6 Inserted Rows
        cursor.execute("""
            SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name
            FROM places p
            JOIN districts d ON p.district_id = d.id
            WHERE p.id BETWEEN 169 AND 178
            ORDER BY p.id ASC
        """)
        batch6_rows = cursor.fetchall()
        print(f"\n4. Batch 6 inserted records (Count: {len(batch6_rows)}):")
        expected_places = [
            (169, "Kahalgaon Rock-Cut Temples", 5, "historical", 25.2689, 87.2345, "kahalgaon-rock-cut-temples-bhagalpur"),
            (170, "Vishwa Shanti Stupa & Ratnagiri Ropeway", 3, "cultural", 25.0085, 85.4385, "vishwa-shanti-stupa-and-ratnagiri-ropeway-nalanda"),
            (171, "Shringirishi Dham", 26, "nature", 25.1278, 86.2344, "shringirishi-dham-lakhisarai"),
            (172, "Girihinda Pahar & Shiv Temple", 32, "mountain", 25.1385, 85.8562, "girihinda-pahar-and-shiv-temple-sheikhpura"),
            (173, "Matsyagandha Lake & Raktakali Temple", 29, "lake", 25.8825, 86.5985, "matsyagandha-lake-and-raktakali-temple-saharsa"),
            (174, "Kajha Kothi Eco Park", 28, "nature", 25.7185, 87.3512, "kajha-kothi-eco-park-purnia"),
            (175, "Guru Tegh Bahadur Historic Gurdwara, Lakshmipur", 23, "cultural", 25.3912, 87.2812, "guru-tegh-bahadur-historic-gurdwara-lakshmipur-katihar"),
            (176, "Dighwa Dubauli Archaeological Mounds", 19, "historical", 26.2485, 84.7312, "dighwa-dubauli-archaeological-mounds-gopalganj"),
            (177, "Champanagar Ancient Capital & Jain Tirth", 5, "cultural", 25.2312, 86.9245, "champanagar-ancient-capital-and-jain-tirth-bhagalpur"),
            (178, "Deokund", 13, "temple", 24.9512, 84.5829, "deokund-aurangabad")
        ]

        for row, exp in zip(batch6_rows, expected_places):
            print(f"   ID {row['id']}: {row['name']} | Dist: {row['district_name']} ({row['district_id']}) | Cat: {row['category']} | Coords: {row['latitude']},{row['longitude']} | Slug: {row['slug']}")
            assert row['id'] == exp[0], f"ID mismatch: {row['id']} != {exp[0]}"
            assert row['name'] == exp[1], f"Name mismatch: {row['name']} != {exp[1]}"
            assert row['district_id'] == exp[2], f"District ID mismatch: {row['district_id']} != {exp[2]}"
            assert row['category'] == exp[3], f"Category mismatch: {row['category']} != {exp[3]}"
            assert round(float(row['latitude']), 4) == round(exp[4], 4), f"Latitude mismatch: {row['latitude']} != {exp[4]}"
            assert round(float(row['longitude']), 4) == round(exp[5], 4), f"Longitude mismatch: {row['longitude']} != {exp[5]}"
            assert row['slug'] == exp[6], f"Slug mismatch: {row['slug']} != {exp[6]}"

        # 5. Duplicate Checks Across All 128 Places
        print("\n5. Checking Duplicates Across Entire 128-Place Active Inventory:")
        cursor.execute("""
            SELECT slug, COUNT(*) as cnt 
            FROM places 
            WHERE deleted_at IS NULL 
            GROUP BY slug 
            HAVING cnt > 1
        """)
        dup_slugs = cursor.fetchall()
        print(f"   - Duplicate slugs: {len(dup_slugs)}")
        assert len(dup_slugs) == 0, f"Duplicate slugs found: {dup_slugs}"

        cursor.execute("""
            SELECT LOWER(name) as lname, COUNT(*) as cnt 
            FROM places 
            WHERE deleted_at IS NULL 
            GROUP BY LOWER(name) 
            HAVING cnt > 1
        """)
        dup_names = cursor.fetchall()
        print(f"   - Duplicate names (case-insensitive): {len(dup_names)}")
        assert len(dup_names) == 0, f"Duplicate names found: {dup_names}"

        cursor.execute("""
            SELECT ROUND(latitude, 4) as rlat, ROUND(longitude, 4) as rlng, COUNT(*) as cnt 
            FROM places 
            WHERE deleted_at IS NULL 
            GROUP BY ROUND(latitude, 4), ROUND(longitude, 4) 
            HAVING cnt > 1
        """)
        dup_coords = cursor.fetchall()
        print(f"   - Duplicate coordinates: {len(dup_coords)}")
        assert len(dup_coords) == 0, f"Duplicate coordinates found: {dup_coords}"

        # 6. Verify pre-existing 118 records are 100% untouched
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE id <= 168 AND deleted_at IS NULL")
        old_count = cursor.fetchone()['cnt']
        print(f"\n6. Invariance of previous records (id <= 168): {old_count} (Expected: 118)")
        assert old_count == 118, f"Expected 118 untouched previous records, found {old_count}"

        # 7. Check district counts
        print("\n7. District Counts for Batch 6 Affected Districts:")
        affected_dists = [5, 3, 26, 32, 29, 28, 23, 19, 13]
        cursor.execute(f"""
            SELECT d.id, d.name, COUNT(p.id) as cnt
            FROM districts d
            LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
            WHERE d.id IN ({','.join(map(str, affected_dists))})
            GROUP BY d.id, d.name
            ORDER BY d.name ASC
        """)
        for r in cursor.fetchall():
            print(f"   - District {r['id']:2d} ({r['name']:<15}): {r['cnt']} active places")

    print("\n================================================================================")
    print("ALL POST-INSERT DATABASE VERIFICATIONS PASSED SUCCESSFULLY!")
    print("================================================================================")

if __name__ == "__main__":
    main()
