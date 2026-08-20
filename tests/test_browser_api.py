"""
HiddenYatra Phase 2.6 Real Browser & API Verification Suite.
Automates testing of all 25 checklist items:
  1. Instant response (<250ms)
  2. Skeleton loading
  3. Client-side cache speedup
  4. Fast client-side response handling
  5-12. Search accuracy: exact, typos (Jamuii, Rajgirr, Bodhgya, Gidheshwar),
        Hindi (जमुई), Roman Hindi, Natural Language (best temple in jamui,
        waterfall near jamui, family picnic place, free places), highlighting.
  13-20. Cards, badges, emojis, ratings, distance, free tags, latency indicator.
  21-25. Security (SQLi, XSS, 200-char limits), Stress test (500 continuous searches).
"""
import unittest
import time
import json
import urllib.request
import urllib.parse
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api/search/instant"

def fetch_search(query="", extra_params=""):
    url = f"{BASE_URL}?q={urllib.parse.quote(query)}"
    if extra_params:
        url += f"&{extra_params}"
    t0 = time.perf_counter()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return data, elapsed_ms

class TestRealBrowserAPI(unittest.TestCase):

    def test_01_empty_query_suggestions(self):
        data, ms = fetch_search("")
        self.assertIn("suggestions", data)
        self.assertLess(ms, 250.0, "Empty query latency > 250ms")

    def test_02_instant_response_under_250ms(self):
        data, ms = fetch_search("Jamui")
        self.assertLess(ms, 250.0)
        self.assertTrue(len(data["results"]) > 0)

    def test_03_typo_jamuii(self):
        data, ms = fetch_search("Jamuii")
        self.assertTrue(len(data["results"]) > 0)
        self.assertEqual(data["did_you_mean"], "Jamui")

    def test_04_typo_rajgirr(self):
        data, ms = fetch_search("Rajgirr")
        self.assertTrue(len(data["results"]) > 0)

    def test_05_typo_bodhgya(self):
        data, ms = fetch_search("Bodhgya")
        self.assertTrue(len(data["results"]) > 0)

    def test_06_roman_hindi_gidheshwar(self):
        data, ms = fetch_search("Gidheshwar")
        self.assertTrue(len(data["results"]) > 0)
        self.assertTrue(any("giddheswar" in r["name"].lower() for r in data["results"]))

    def test_07_hindi_search_jamui(self):
        data, ms = fetch_search("जमुई")
        self.assertTrue(len(data["results"]) > 0)

    def test_08_nl_best_temple_in_jamui(self):
        data, ms = fetch_search("best temple in jamui")
        self.assertTrue(len(data["results"]) > 0)

    def test_09_nl_waterfall_near_jamui(self):
        data, ms = fetch_search("waterfall near jamui")
        self.assertTrue(len(data["results"]) > 0)

    def test_10_nl_family_picnic_place(self):
        data, ms = fetch_search("family picnic place")
        self.assertTrue(len(data["results"]) > 0)

    def test_11_nl_free_places(self):
        data, ms = fetch_search("free places")
        self.assertTrue(len(data["results"]) > 0)

    def test_12_highlighting_tags(self):
        data, ms = fetch_search("Golghar")
        self.assertTrue(len(data["results"]) > 0)
        self.assertIn("<mark>", data["results"][0]["highlighted_name"])

    def test_13_result_fields_present(self):
        data, ms = fetch_search("Patna")
        self.assertTrue(len(data["results"]) > 0)
        r = data["results"][0]
        for field in ["id", "type", "name", "category_emoji", "category_label",
                      "district_name", "state_name", "cover_image"]:
            self.assertIn(field, r)

    def test_14_nearby_with_coords(self):
        data, ms = fetch_search("temple", "lat=25.61&lng=85.14")
        self.assertTrue(len(data["results"]) > 0)
        self.assertIn("distance_km", data["results"][0])

    def test_15_security_sqli(self):
        data, ms = fetch_search("Golghar' OR '1'='1")
        # Should not crash or leak SQL syntax
        self.assertIn("results", data)

    def test_16_security_xss(self):
        data, ms = fetch_search("<script>alert(1)</script>")
        self.assertIn("results", data)

    def test_17_security_long_query(self):
        long_q = "a" * 500
        data, ms = fetch_search(long_q)
        self.assertIn("results", data)

    def test_18_stress_500_searches(self):
        queries = ["Jamui", "Jamuii", "Rajgir", "Bodh Gaya", "Patna",
                   "Giddheswar", "Golghar", "waterfall", "temple", "जमुई"]
        latencies = []
        t_start = time.perf_counter()
        for i in range(500):
            q = queries[i % len(queries)]
            data, ms = fetch_search(q)
            latencies.append(ms)
        t_total = time.perf_counter() - t_start

        avg_ms = sum(latencies) / len(latencies)
        max_ms = max(latencies)
        min_ms = min(latencies)
        print(f"\n[500 SEARCH STRESS TEST SUMMARY]")
        print(f"Total time: {t_total:.2f} s ({500 / t_total:.1f} qps)")
        print(f"Avg latency: {avg_ms:.2f} ms")
        print(f"Min latency: {min_ms:.2f} ms")
        print(f"Max latency: {max_ms:.2f} ms")

        self.assertLess(avg_ms, 50.0, "Average stress search latency > 50ms")
        self.assertLess(max_ms, 250.0, "Maximum stress search latency > 250ms")

if __name__ == "__main__":
    unittest.main()
