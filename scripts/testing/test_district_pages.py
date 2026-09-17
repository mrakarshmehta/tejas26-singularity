import urllib.request
import html as html_lib

base_url = "http://127.0.0.1:5000"

district_routes = [
    ("jhanjharpur-madhubani", "Saurath Sabha Gachhi"),
    ("rohtas", "Tutla Bhawani Waterfall & Hanging Bridge"),
    ("bhagalpur", "Bateshwar Sthan & Patharghata Caves"),
    ("araria", "Bio-Diversity Park, Kusiargaon"),
    ("rohtas", "Dhuan Kund & Manjhar Kund Waterfalls"),
    ("west-champaran", "Someshwar Fort & Hills"),
    ("nalanda", "Ghora Katora Lake Eco-Reserve"),
    ("darbhanga", "Kusheshwar Asthan Bird Sanctuary & Temple"),
    ("east-champaran", "Areraj Someshwar Nath Temple & Ashokan Pillar"),
    ("saran", "Chirand Archaeological Site"),
]

print("=== DISTRICT PAGES VERIFICATION ===")
for dist_slug, expected_place in district_routes:
    url = f"{base_url}/state/bihar/{dist_slug}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Test'})
    with urllib.request.urlopen(req) as resp:
        status = resp.status
        raw_html = resp.read().decode('utf-8')
        clean_html = html_lib.unescape(raw_html)
        assert status == 200, f"Status {status} for {dist_slug}"
        assert expected_place in clean_html, f"Place '{expected_place}' not found in /state/bihar/{dist_slug}"
        print(f"PASS: /state/bihar/{dist_slug} -> 200 OK | Verified place: {expected_place}")

print("\nALL AFFECTED DISTRICT PAGES VERIFIED SUCCESSFULLY!")
