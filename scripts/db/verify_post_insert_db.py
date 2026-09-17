import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor() as cursor:
    cursor.execute("SELECT COUNT(*) as cnt FROM places WHERE deleted_at IS NULL")
    active_cnt = cursor.fetchone()['cnt']
    print(f"Total active places: {active_cnt} (Expected: 98)")
    assert active_cnt == 98, f"Active count mismatch: {active_cnt}"

    cursor.execute("SELECT COUNT(DISTINCT district_id) as cnt FROM places WHERE deleted_at IS NULL")
    district_cnt = cursor.fetchone()['cnt']
    print(f"Districts covered: {district_cnt} (Expected: 38)")
    assert district_cnt == 38, f"Districts covered mismatch: {district_cnt}"

    cursor.execute("SELECT * FROM places WHERE id >= 139 AND id <= 148 ORDER BY id")
    batch3 = cursor.fetchall()
    print(f"\nInserted records count: {len(batch3)} (Expected: 10)")
    assert len(batch3) == 10, f"Inserted count mismatch: {len(batch3)}"

    expected = [
        (139, "Saurath Sabha Gachhi", 20, "cultural", 26.4125, 86.0954, "saurath-sabha-gachhi-madhubani"),
        (140, "Tutla Bhawani Waterfall & Hanging Bridge", 8, "waterfall", 24.7815, 84.0125, "tutla-bhawani-waterfall-and-hanging-bridge-rohtas"),
        (141, "Bateshwar Sthan & Patharghata Caves", 5, "historical", 25.3341, 87.2712, "bateshwar-sthan-and-patharghata-caves-bhagalpur"),
        (142, "Bio-Diversity Park, Kusiargaon", 11, "nature", 26.1158, 87.4589, "bio-diversity-park-kusiargaon-araria"),
        (143, "Dhuan Kund & Manjhar Kund Waterfalls", 8, "waterfall", 24.8912, 84.0124, "dhuan-kund-and-manjhar-kund-waterfalls-rohtas"),
        (144, "Someshwar Fort & Hills", 9, "mountain", 27.4685, 84.3125, "someshwar-fort-and-hills-west-champaran"),
        (145, "Ghora Katora Lake Eco-Reserve", 3, "nature", 24.9921, 85.4812, "ghora-katora-lake-eco-reserve-nalanda"),
        (146, "Kusheshwar Asthan Bird Sanctuary & Temple", 18, "nature", 25.8125, 86.1158, "kusheshwar-asthan-bird-sanctuary-and-temple-darbhanga"),
        (147, "Areraj Someshwar Nath Temple & Ashokan Pillar", 10, "historical", 26.5412, 84.7485, "areraj-someshwar-nath-temple-and-ashokan-pillar-east-champaran"),
        (148, "Chirand Archaeological Site", 31, "historical", 25.7125, 84.8125, "chirand-archaeological-site-saran"),
    ]

    for p, exp in zip(batch3, expected):
        exp_id, exp_name, exp_dist, exp_cat, exp_lat, exp_lng, exp_slug = exp
        assert p['id'] == exp_id, f"ID mismatch: {p['id']} vs {exp_id}"
        assert p['name'] == exp_name, f"Name mismatch: {p['name']} vs {exp_name}"
        assert p['district_id'] == exp_dist, f"District mismatch: {p['district_id']} vs {exp_dist}"
        assert p['category'] == exp_cat, f"Category mismatch: {p['category']} vs {exp_cat}"
        assert abs(float(p['latitude']) - exp_lat) < 0.0001, f"Lat mismatch: {p['latitude']} vs {exp_lat}"
        assert abs(float(p['longitude']) - exp_lng) < 0.0001, f"Lng mismatch: {p['longitude']} vs {exp_lng}"
        assert p['slug'] == exp_slug, f"Slug mismatch: {p['slug']} vs {exp_slug}"
        print(f"ID {p['id']}: {p['name']} | dist={p['district_id']} | cat={p['category']} | ({p['latitude']}, {p['longitude']}) | slug={p['slug']} -> PASS")

    # Duplicate checks across all 98 active places
    cursor.execute("SELECT name, slug, latitude, longitude FROM places WHERE deleted_at IS NULL")
    all_active = cursor.fetchall()
    names = [r['name'].lower() for r in all_active]
    slugs = [r['slug'] for r in all_active]
    coords = [(float(r['latitude']), float(r['longitude'])) for r in all_active]

    assert len(names) == len(set(names)), f"Duplicate name detected! Count: {len(names)} vs {len(set(names))}"
    assert len(slugs) == len(set(slugs)), f"Duplicate slug detected! Count: {len(slugs)} vs {len(set(slugs))}"
    assert len(coords) == len(set(coords)), f"Duplicate coordinate detected! Count: {len(coords)} vs {len(set(coords))}"
    print("\nZero duplicate names, zero duplicate slugs, zero duplicate coordinates across all 98 places: PASS")

    # Affected districts count report
    affected_district_ids = [20, 8, 5, 11, 9, 3, 18, 10, 31]
    cursor.execute(f"""
        SELECT d.id, d.name, COUNT(p.id) as place_count 
        FROM districts d 
        LEFT JOIN places p ON d.id = p.district_id AND p.deleted_at IS NULL 
        WHERE d.id IN ({','.join(map(str, affected_district_ids))})
        GROUP BY d.id, d.name
        ORDER BY d.id
    """)
    print("\nAffected Districts New Counts:")
    for d in cursor.fetchall():
        print(f"  District ID {d['id']:2} ({d['name']:25}): {d['place_count']} active places")
