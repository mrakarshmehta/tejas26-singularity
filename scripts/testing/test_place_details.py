import urllib.request
import re

base_url = "http://127.0.0.1:5000"

slugs = [
    ("saurath-sabha-gachhi-madhubani", "Saurath Sabha Gachhi", "cultural"),
    ("tutla-bhawani-waterfall-and-hanging-bridge-rohtas", "Tutla Bhawani Waterfall & Hanging Bridge", "waterfall"),
    ("bateshwar-sthan-and-patharghata-caves-bhagalpur", "Bateshwar Sthan & Patharghata Caves", "historical"),
    ("bio-diversity-park-kusiargaon-araria", "Bio-Diversity Park, Kusiargaon", "nature"),
    ("dhuan-kund-and-manjhar-kund-waterfalls-rohtas", "Dhuan Kund & Manjhar Kund Waterfalls", "waterfall"),
    ("someshwar-fort-and-hills-west-champaran", "Someshwar Fort & Hills", "mountain"),
    ("ghora-katora-lake-eco-reserve-nalanda", "Ghora Katora Lake Eco-Reserve", "nature"),
    ("kusheshwar-asthan-bird-sanctuary-and-temple-darbhanga", "Kusheshwar Asthan Bird Sanctuary & Temple", "nature"),
    ("areraj-someshwar-nath-temple-and-ashokan-pillar-east-champaran", "Areraj Someshwar Nath Temple & Ashokan Pillar", "historical"),
    ("chirand-archaeological-site-saran", "Chirand Archaeological Site", "historical"),
]

print("=== PLACE DETAIL PAGES VERIFICATION ===")
for slug, expected_name, cat in slugs:
    url = f"{base_url}/place/{slug}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Test'})
    with urllib.request.urlopen(req) as resp:
        status = resp.status
        html = resp.read().decode('utf-8')
        assert status == 200, f"Status {status} for {slug}"
        assert expected_name in html or slug in html, f"Name not in HTML for {slug}"
        assert "404" not in html[:500], f"404 detected for {slug}"
        print(f"PASS: /place/{slug} -> Status: {status}, Page Size: {len(html)} bytes")

print("\nALL 10 PLACE DETAIL PAGES RENDERED PERFECTLY WITH 200 OK!")
