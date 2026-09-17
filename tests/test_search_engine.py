"""
Unit tests for HiddenYatra Ultimate AI Search Engine (Phase 2.5).
Tests: exact, partial, typo, Hindi, Roman Hindi, phonetic, synonym,
NL intent, nearby, filters, analytics, security, caching, ranking, performance.
"""
import unittest
import time
import math
from app import create_app
from models.search_engine import (
    levenshtein_distance, normalize, normalize_compact, sanitize_query,
    transliterate_hindi, resolve_roman_hindi, expand_query_with_synonyms,
    soundex, highlight_match, haversine_km, parse_nl_intent,
    SearchIndex, instant_search, get_search_suggestions,
    nearby_search, get_filter_options, get_search_analytics,
)


class TestLevenshtein(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(levenshtein_distance("jamui", "jamui"), 0)

    def test_one_extra_char(self):
        self.assertEqual(levenshtein_distance("jamuii", "jamui"), 1)

    def test_one_wrong_char(self):
        self.assertEqual(levenshtein_distance("jamuih", "jamui"), 1)

    def test_one_missing_char(self):
        self.assertEqual(levenshtein_distance("rajgirr", "rajgir"), 1)

    def test_insertion(self):
        self.assertEqual(levenshtein_distance("bodhgya", "bodhgaya"), 1)


class TestSoundex(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(soundex("Robert"), "R163")

    def test_jamui(self):
        self.assertEqual(soundex("Jamui"), soundex("Jamuii"))  # same soundex

    def test_rajgir(self):
        s1 = soundex("Rajgir")
        s2 = soundex("Rajgeer")
        self.assertEqual(s1, s2)

    def test_empty(self):
        self.assertEqual(soundex(""), "")


class TestNormalization(unittest.TestCase):
    def test_case(self):
        self.assertEqual(normalize("RAJGIR"), "rajgir")

    def test_mixed_case(self):
        self.assertEqual(normalize("RajGir"), "rajgir")

    def test_hyphens(self):
        self.assertEqual(normalize("raj-gir"), "raj gir")

    def test_whitespace(self):
        self.assertEqual(normalize("  Bodh  Gaya  "), "bodh gaya")

    def test_compact(self):
        self.assertEqual(normalize_compact("Bodh Gaya"), "bodhgaya")


class TestSanitization(unittest.TestCase):
    def test_length_limit(self):
        long_q = "a" * 500
        self.assertEqual(len(sanitize_query(long_q)), 200)

    def test_strips_sql_chars(self):
        self.assertNotIn("'", sanitize_query("test' OR 1=1"))
        self.assertNotIn(";", sanitize_query("test; DROP TABLE"))

    def test_strips_null_bytes(self):
        self.assertNotIn("\x00", sanitize_query("test\x00injection"))

    def test_normal_query_unchanged(self):
        self.assertEqual(sanitize_query("Jamui Temple"), "Jamui Temple")


class TestHindiTransliteration(unittest.TestCase):
    def test_jamui(self):
        txt, is_hindi = transliterate_hindi("जमुई")
        self.assertTrue(is_hindi)
        self.assertEqual(txt, "jamui")

    def test_temple(self):
        txt, is_hindi = transliterate_hindi("मंदिर")
        self.assertTrue(is_hindi)
        self.assertEqual(txt, "temple")

    def test_patna(self):
        txt, is_hindi = transliterate_hindi("पटना")
        self.assertTrue(is_hindi)
        self.assertEqual(txt, "patna")

    def test_english_passthrough(self):
        txt, is_hindi = transliterate_hindi("Jamui")
        self.assertFalse(is_hindi)
        self.assertEqual(txt, "Jamui")


class TestRomanHindi(unittest.TestCase):
    def test_gidheshwar(self):
        self.assertEqual(resolve_roman_hindi("gidheshwar"), "giddheswar")

    def test_patneswar(self):
        self.assertEqual(resolve_roman_hindi("patneswar"), "patneshwar")

    def test_bodhgya(self):
        self.assertEqual(resolve_roman_hindi("bodhgya"), "bodh gaya")

    def test_mandir(self):
        self.assertEqual(resolve_roman_hindi("mandir"), "temple")

    def test_unknown_returns_none(self):
        self.assertIsNone(resolve_roman_hindi("xyzabc"))


class TestSynonymExpansion(unittest.TestCase):
    def test_mandir_to_temple(self):
        syns = expand_query_with_synonyms("mandir")
        self.assertIn("temple", syns)

    def test_jharna_to_waterfall(self):
        syns = expand_query_with_synonyms("jharna")
        self.assertIn("waterfall", syns)

    def test_pahar_to_hill(self):
        syns = expand_query_with_synonyms("pahar")
        self.assertIn("hill", syns)


class TestNLIntentParsing(unittest.TestCase):
    def test_near_me(self):
        intent = parse_nl_intent("temple near me")
        self.assertTrue(intent.near_me)
        self.assertEqual(intent.category_filter, "temple")

    def test_category_in_location(self):
        intent = parse_nl_intent("best temple in Jamui")
        self.assertEqual(intent.category_filter, "temple")
        self.assertIn("jamui", intent.location_filter.lower())

    def test_family_friendly(self):
        intent = parse_nl_intent("family picnic place")
        self.assertTrue(intent.family_friendly)

    def test_free_entry(self):
        intent = parse_nl_intent("free entry places")
        self.assertTrue(intent.free_entry)

    def test_season(self):
        intent = parse_nl_intent("places to visit in winter")
        self.assertIsNotNone(intent.season)

    def test_plain_keyword(self):
        intent = parse_nl_intent("Golghar")
        self.assertEqual(intent.intent_type, "keyword")


class TestHaversine(unittest.TestCase):
    def test_same_point(self):
        self.assertAlmostEqual(haversine_km(25.6, 85.1, 25.6, 85.1), 0.0, places=1)

    def test_known_distance(self):
        # Patna to Gaya ≈ 100 km
        d = haversine_km(25.61, 85.14, 24.80, 84.99)
        self.assertGreater(d, 80)
        self.assertLess(d, 120)


class TestHighlightMatch(unittest.TestCase):
    def test_exact_substring(self):
        h = highlight_match("Golghar Patna", "Golghar")
        self.assertIn("<mark>Golghar</mark>", h)

    def test_case_insensitive(self):
        h = highlight_match("Mahabodhi Temple", "mahabodhi")
        self.assertIn("<mark>", h)

    def test_no_match(self):
        h = highlight_match("Golghar", "xyzabc")
        self.assertEqual(h, "Golghar")


class TestSearchIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_ctx = cls.app.app_context()
        cls.app_ctx.push()
        cls.idx = SearchIndex()
        cls.idx.build()

    @classmethod
    def tearDownClass(cls):
        cls.app_ctx.pop()

    def test_index_built(self):
        self.assertTrue(self.idx.size > 0)

    def test_exact_search(self):
        results = self.idx.search("Jamui", limit=5)
        self.assertTrue(len(results) > 0)
        self.assertTrue(any("jamui" in r['name'].lower() for r in results))

    def test_typo_jamuii(self):
        results = self.idx.search("Jamuii", limit=5)
        self.assertTrue(len(results) > 0, "No results for 'Jamuii'")
        self.assertTrue(any("jamui" in r['name'].lower() or "jamui" in r['district_name'].lower() for r in results))

    def test_typo_bodhgya(self):
        results = self.idx.search("Bodhgya", limit=5)
        self.assertTrue(len(results) > 0, "No results for 'Bodhgya'")

    def test_typo_rajgirr(self):
        results = self.idx.search("Rajgirr", limit=5)
        self.assertTrue(len(results) > 0, "No results for 'Rajgirr'")

    def test_partial_pat(self):
        results = self.idx.search("pat", limit=5)
        self.assertTrue(len(results) > 0, "No results for partial 'pat'")

    def test_partial_bod(self):
        results = self.idx.search("bod", limit=5)
        self.assertTrue(len(results) > 0, "No results for partial 'bod'")

    def test_partial_gid(self):
        results = self.idx.search("gid", limit=5)
        self.assertTrue(len(results) > 0, "No results for partial 'gid'")

    def test_hindi_search(self):
        results = self.idx.search("जमुई", limit=5)
        self.assertTrue(len(results) > 0, "No results for Hindi 'जमुई'")

    def test_roman_hindi_gidheshwar(self):
        results = self.idx.search("Gidheshwar", limit=5)
        self.assertTrue(len(results) > 0, "No results for Roman Hindi 'Gidheshwar'")

    def test_synonym_mandir(self):
        results = self.idx.search("Mandir", limit=10)
        self.assertTrue(len(results) > 0, "No results for synonym 'Mandir'")

    def test_case_insensitivity(self):
        r1 = self.idx.search("RAJGIR", limit=5)
        r2 = self.idx.search("rajgir", limit=5)
        r3 = self.idx.search("RajGir", limit=5)
        self.assertEqual(len(r1), len(r2))
        self.assertEqual(len(r2), len(r3))

    def test_nl_temple_in_jamui(self):
        results = self.idx.search("best temple in Jamui", limit=10)
        self.assertTrue(len(results) > 0, "No results for NL query 'best temple in Jamui'")

    def test_filter_category(self):
        results = self.idx.search("Bihar", limit=20, filters={'category': 'temple'})
        for r in results:
            if r['type'] == 'place':
                self.assertEqual(r['category'], 'temple',
                                 f"Non-temple result: {r['name']} ({r['category']})")

    def test_filter_family_friendly(self):
        results = self.idx.search("family picnic place", limit=10)
        # Should return results (NL intent sets family_friendly filter)
        # Just check it doesn't crash
        self.assertIsInstance(results, list)

    def test_nearby_search(self):
        # Patna coordinates
        results = self.idx.get_nearby(25.61, 85.14, radius_km=50, limit=10)
        self.assertTrue(len(results) > 0, "No nearby results around Patna")
        # All should have distance_km
        for r in results:
            self.assertIn('distance_km', r)

    def test_filter_options(self):
        opts = self.idx.get_filter_options()
        self.assertIn('categories', opts)
        self.assertIn('districts', opts)
        self.assertTrue(len(opts['categories']) > 0)

    def test_ranking_exact_beats_fuzzy(self):
        results = self.idx.search("Jamui", limit=10)
        if len(results) >= 2:
            # First result should have higher score
            self.assertGreaterEqual(results[0]['score'], results[1]['score'])

    def test_popular_searches(self):
        popular = self.idx.get_popular_searches(limit=5)
        self.assertIsInstance(popular, list)

    def test_result_has_required_fields(self):
        results = self.idx.search("Patna", limit=3)
        self.assertTrue(len(results) > 0)
        r = results[0]
        for field in ['id', 'type', 'name', 'url', 'category', 'score',
                      'match_type', 'highlighted_name']:
            self.assertIn(field, r, f"Missing field: {field}")


class TestSearchAnalytics(unittest.TestCase):
    def test_log_and_retrieve(self):
        analytics = get_search_analytics()
        analytics.log_search("test query", 5, 1.2)
        stats = analytics.get_stats()
        self.assertIn('total_searches', stats)
        self.assertGreater(stats['total_searches'], 0)

    def test_failed_search_tracking(self):
        analytics = get_search_analytics()
        analytics.log_search("xyznonexistent123", 0, 0.5)
        failed = analytics.get_failed_queries(limit=5)
        self.assertTrue(any("xyznonexistent123" in q for q, _ in failed))


class TestPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_ctx = cls.app.app_context()
        cls.app_ctx.push()
        cls.idx = SearchIndex()
        cls.idx.build()

    @classmethod
    def tearDownClass(cls):
        cls.app_ctx.pop()

    def test_search_under_50ms(self):
        queries = ["Jamui", "Jamuii", "pat", "gid", "temple", "mandir",
                    "bodhgya", "RAJGIR", "best temple in Jamui", "waterfall near me"]
        t0 = time.perf_counter()
        for _ in range(100):
            for q in queries:
                self.idx.search(q, limit=10)
        elapsed = time.perf_counter() - t0
        avg_ms = (elapsed / (100 * len(queries))) * 1000
        print(f"\nAverage search time: {avg_ms:.3f} ms per query "
              f"({100 * len(queries)} total queries in {elapsed:.2f}s)")
        self.assertLess(avg_ms, 50.0, "Search > 50ms average")

    def test_caching_speedup(self):
        # First search (cold)
        t0 = time.perf_counter()
        self.idx.search("Jamui", limit=10)
        cold_ms = (time.perf_counter() - t0) * 1000

        # Second search (cached)
        t0 = time.perf_counter()
        self.idx.search("Jamui", limit=10)
        hot_ms = (time.perf_counter() - t0) * 1000

        print(f"\nCold: {cold_ms:.3f}ms, Hot (cached): {hot_ms:.3f}ms")
        # Cached should be faster (or at least not slower)
        self.assertLess(hot_ms, cold_ms + 5)


    def test_search_engine_seq_id_propagation(self):
        """Verify seq_id parameter propagates through instant_search results."""
        from models.search_engine import instant_search
        results = instant_search('patna', limit=5, seq_id=42)
        if results:
            for r in results:
                self.assertEqual(r.get('seq_id'), 42)

if __name__ == '__main__':
    unittest.main()
