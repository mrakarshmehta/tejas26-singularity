import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

def main():
    print("=== POST-INSERT DATABASE VERIFICATION FOR BATCH 5 ===")
    with get_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
        total_active = cursor.fetchone()['cnt']
        print(f"1. Total active places: {total_active} (Expected: 118)")
        assert total_active == 118, f"Expected 118, got {total_active}"

        cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
        districts_covered = cursor.fetchone()['cnt']
        print(f"2. Districts covered: {districts_covered}/38")
        assert districts_covered == 38, f"Expected 38, got {districts_covered}"

        cursor.execute("""
            SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude, p.district_id, d.name as district_name
            FROM places p
            JOIN districts d ON p.district_id = d.id
            WHERE p.id BETWEEN 159 AND 168
            ORDER BY p.id ASC
        """)
        batch5_rows = cursor.fetchall()
        print(f"\n3. Batch 5 inserted records (Count: {len(batch5_rows)}):")
        expected_places = [
            (159, "Umga Sun Temple & Rock Complex", 13, "historical", 24.6312, 84.5518, "umga-sun-temple-and-rock-complex-aurangabad"),
            (160, "Ashokan Pillar & Ananda Stupa, Kolhua", 37, "historical", 26.0125, 85.1124, "ashokan-pillar-and-ananda-stupa-kolhua-vaishali"),
            (161, "Punaura Dham", 34, "cultural", 26.6125, 85.4512, "punaura-dham-sitamarhi"),
            (162, "Udaipur Wildlife Sanctuary", 9, "nature", 26.8512, 84.4812, "udaipur-wildlife-sanctuary-west-champaran"),
            (163, "Chandan Dam", 14, "lake", 24.7812, 86.8125, "chandan-dam-banka"),
            (164, "Baraila Lake / Salim Ali Jubba Sahni Bird Sanctuary", 37, "nature", 25.7512, 85.4512, "baraila-lake-salim-ali-bird-sanctuary-vaishali"),
            (165, "George Orwell Birthplace & Memorial", 10, "historical", 26.6452, 84.9085, "george-orwell-birthplace-and-memorial-east-champaran"),
            (166, "Kharagpur Lake (Haveli Kharagpur)", 6, "lake", 25.1215, 86.5124, "kharagpur-lake-haveli-kharagpur-munger"),
            (167, "Sarvodaya Ashram, Shekhodeora", 38, "cultural", 24.8125, 85.8412, "sarvodaya-ashram-shekhodeora-nawada"),
            (168, "Sujani Embroidery Craft Cluster", 7, "cultural", 26.1512, 85.4812, "sujani-embroidery-craft-cluster-muzaffarpur"),
        ]

        for row, exp in zip(batch5_rows, expected_places):
            exp_id, exp_name, exp_dist_id, exp_cat, exp_lat, exp_lng, exp_slug = exp
            assert row['id'] == exp_id, f"ID mismatch: {row['id']} vs {exp_id}"
            assert row['name'] == exp_name, f"Name mismatch: {row['name']} vs {exp_name}"
            assert row['district_id'] == exp_dist_id, f"District mismatch: {row['district_id']} vs {exp_dist_id}"
            assert row['category'] == exp_cat, f"Category mismatch: {row['category']} vs {exp_cat}"
            assert abs(float(row['latitude']) - exp_lat) < 0.0001, f"Lat mismatch: {row['latitude']} vs {exp_lat}"
            assert abs(float(row['longitude']) - exp_lng) < 0.0001, f"Lng mismatch: {row['longitude']} vs {exp_lng}"
            assert row['slug'] == exp_slug, f"Slug mismatch: {row['slug']} vs {exp_slug}"
            print(f"  [ID {row['id']:3d}] {row['name']:48} | Dist: {row['district_name']} ({row['district_id']}) | Cat: {row['category']:10} | ({row['latitude']:.4f}, {row['longitude']:.4f}) | Slug: {row['slug']}")

        # 4. Duplicate checks across all 118 active places
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
        cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE id < 159 AND deleted_at IS NULL")
        existing_active = cursor.fetchone()['cnt']
        print(f"7. Pre-existing records still active: {existing_active} (Expected: 108)")
        assert existing_active == 108, f"Expected 108 pre-existing active records, got {existing_active}"

        # 8. District counts for affected districts
        target_districts = [
            ("Aurangabad", 13),
            ("Vaishali", 37),
            ("Sitamarhi", 34),
            ("West Champaran", 9),
            ("Banka", 14),
            ("East Champaran", 10),
            ("Munger", 6),
            ("Nawada", 38),
            ("Muzaffarpur", 7)
        ]
        print("\n8. District counts for affected districts:")
        for dname, did in target_districts:
            cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE district_id = %s AND deleted_at IS NULL", (did,))
            dcnt = cursor.fetchone()['cnt']
            print(f"  - {dname:20} (ID: {did:>2}): {dcnt} active places")

    print("\nALL POST-INSERT DATABASE CHECKS PASSED [OK]")

if __name__ == "__main__":
    main()
