import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

def main():
    print("=== POST-INSERT DATABASE VERIFICATION ===")
    with get_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        total_active = cursor.fetchone()['cnt']
        print(f"1. Total active places: {total_active} (Expected: 108)")
        assert total_active == 108, f"Expected 108, got {total_active}"

        cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
        districts_covered = cursor.fetchone()['cnt']
        print(f"2. Districts covered: {districts_covered}/38")
        assert districts_covered == 38, f"Expected 38, got {districts_covered}"

        cursor.execute("""
            SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name
            FROM places p
            JOIN districts d ON p.district_id = d.id
            WHERE p.id BETWEEN 149 AND 158
            ORDER BY p.id ASC
        """)
        batch4_rows = cursor.fetchall()
        print(f"\n3. Batch 4 inserted records (Count: {len(batch4_rows)}):")
        expected_places = [
            (149, "Rampurva Ashokan Pillars", 9, "historical", 27.2685, 84.5012, "rampurva-ashokan-pillars-west-champaran"),
            (150, "Phanishwar Nath Renu Smarak & Birthplace", 11, "cultural", 26.2486, 87.2842, "phanishwar-nath-renu-smarak-and-birthplace-araria"),
            (151, "Shergarh Fort", 8, "historical", 24.8415, 83.7812, "shergarh-fort-rohtas"),
            (152, "Daud Khan Fort", 13, "historical", 25.0315, 84.4024, "daud-khan-fort-aurangabad"),
            (153, "Lauriya Nandangarh", 9, "historical", 26.9954, 84.4124, "lauriya-nandangarh-west-champaran"),
            (154, "Rajnagar Palace Complex", 20, "historical", 26.3912, 86.1485, "rajnagar-palace-complex-madhubani"),
            (155, "Kaimur Wildlife Sanctuary & Adhaura Hills", 22, "nature", 24.8125, 83.6125, "kaimur-wildlife-sanctuary-and-adhaura-hills-kaimur"),
            (156, "Simaria Ghat & Dinkar Memorial", 15, "cultural", 25.4382, 85.9921, "simaria-ghat-and-dinkar-memorial-begusarai"),
            (157, "Jal Mandir, Pawapuri", 3, "temple", 25.0925, 85.5385, "jal-mandir-pawapuri-nalanda"),
            (158, "Gupta Dham (Gupteshwar Mahadev Cave)", 8, "nature", 24.7512, 83.7912, "gupta-dham-gupteshwar-mahadev-cave-rohtas"),
        ]

        for row, exp in zip(batch4_rows, expected_places):
            exp_id, exp_name, exp_dist_id, exp_cat, exp_lat, exp_lng, exp_slug = exp
            assert row['id'] == exp_id, f"ID mismatch: {row['id']} vs {exp_id}"
            assert row['name'] == exp_name, f"Name mismatch: {row['name']} vs {exp_name}"
            assert row['district_id'] == exp_dist_id, f"District mismatch: {row['district_id']} vs {exp_dist_id}"
            assert row['category'] == exp_cat, f"Category mismatch: {row['category']} vs {exp_cat}"
            assert abs(float(row['latitude']) - exp_lat) < 0.0001, f"Lat mismatch: {row['latitude']} vs {exp_lat}"
            assert abs(float(row['longitude']) - exp_lng) < 0.0001, f"Lng mismatch: {row['longitude']} vs {exp_lng}"
            assert row['slug'] == exp_slug, f"Slug mismatch: {row['slug']} vs {exp_slug}"
            print(f"  [ID {row['id']:3d}] {row['name']:42} | Dist: {row['district_name']} ({row['district_id']}) | Cat: {row['category']:10} | ({row['latitude']:.4f}, {row['longitude']:.4f}) | Slug: {row['slug']}")

        # 4. Duplicate checks across all 108 active places
        cursor.execute("SELECT slug, COUNT(*) as cnt FROM places WHERE deleted_at IS NULL GROUP BY slug HAVING cnt > 1")
        dup_slugs = cursor.fetchall()
        print(f"\n4. Duplicate slugs count: {len(dup_slugs)}")
        assert len(dup_slugs) == 0, f"Duplicate slugs found: {dup_slugs}"

        cursor.execute("SELECT LOWER(name) as lname, COUNT(*) as cnt FROM places WHERE deleted_at IS NULL GROUP BY lname HAVING cnt > 1")
        dup_names = cursor.fetchall()
        print(f"5. Duplicate names count: {len(dup_names)}")
        assert len(dup_names) == 0, f"Duplicate names found: {dup_names}"

        cursor.execute("SELECT ROUND(latitude, 4) as rlat, ROUND(longitude, 4) as rlng, COUNT(*) as cnt FROM places WHERE deleted_at IS NULL GROUP BY rlat, rlng HAVING cnt > 1")
        dup_coords = cursor.fetchall()
        print(f"6. Duplicate coordinates count: {len(dup_coords)}")
        assert len(dup_coords) == 0, f"Duplicate coordinates found: {dup_coords}"

        # 7. Unintended existing-record changes
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE id < 149 AND deleted_at IS NULL")
        existing_active = cursor.fetchone()['cnt']
        print(f"7. Pre-existing records still active: {existing_active} (Expected: 98)")
        assert existing_active == 98, f"Expected 98 pre-existing active records, got {existing_active}"

        # 8. District counts for requested districts
        target_districts = [
            ("West Champaran", 9),
            ("Araria", 11),
            ("Rohtas", 8),
            ("Aurangabad", 13),
            ("Madhubani", 20),
            ("Kaimur", 22),
            ("Begusarai", 15),
            ("Nalanda", 3)
        ]
        print("\n8. District counts for affected districts:")
        for dname, did in target_districts:
            cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE district_id = %s AND deleted_at IS NULL", (did,))
            dcnt = cursor.fetchone()['cnt']
            print(f"  - {dname:20} (ID: {did:>2}): {dcnt} active places")

    print("\nALL POST-INSERT DATABASE CHECKS PASSED [OK]")

if __name__ == "__main__":
    main()
