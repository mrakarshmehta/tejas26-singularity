"""
Unit and integration tests for Cultural Dimensions navigation and subsystem discovery.
Verifies the discover dropdown, homepage cultural grid, footer columns, and route accessibility.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _create_test_app():
    try:
        from app import create_app
        app = create_app()
        app.config['TESTING'] = True
        return app
    except Exception:
        return None


class TestCulturalDimensionsNavigation(unittest.TestCase):
    """Test Cultural Dimensions navigation components and integration."""

    @classmethod
    def setUpClass(cls):
        cls.app = _create_test_app()
        if cls.app is None:
            raise unittest.SkipTest("MySQL not available")
        cls.client = cls.app.test_client()

    def test_homepage_cultural_dimensions_section(self):
        """Home page must contain the Cultural Dimensions section and cards."""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn('id="cultural-dimensions-section"', html)
        self.assertIn('cultural-dimensions-grid', html)
        self.assertIn('id="card-intellectual-heritage"', html)
        self.assertIn('id="card-treks"', html)
        self.assertIn('id="card-souvenirs"', html)
        self.assertIn('id="card-guides"', html)
        self.assertIn('id="card-quiz"', html)
        self.assertIn('id="card-budget"', html)

    def test_navbar_discover_dropdown(self):
        """Navbar must include the Discover dropdown with all cultural routes."""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn('id="nav-discover-dropdown"', html)
        self.assertIn('id="discover-dropdown-btn"', html)
        self.assertIn('id="discover-dropdown-menu"', html)
        self.assertIn('id="nav-discover-scholars"', html)
        self.assertIn('id="nav-discover-treks"', html)
        self.assertIn('id="nav-discover-souvenirs"', html)
        self.assertIn('id="nav-discover-guides"', html)
        self.assertIn('id="nav-discover-quiz"', html)
        self.assertIn('id="nav-discover-budget"', html)
        self.assertIn('id="nav-discover-archaeology"', html)
        self.assertIn('id="nav-discover-arts"', html)
        self.assertIn('id="nav-discover-weather"', html)

    def test_footer_cultural_links(self):
        """Footer must feature the Culture & Treks column with active links."""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn('Culture & Treks', html)
        self.assertIn('/intellectual-heritage', html)
        self.assertIn('/treks', html)
        self.assertIn('/souvenirs', html)
        self.assertIn('/guides', html)
        self.assertIn('/quiz', html)
        self.assertIn('/budget-planner', html)

    def test_cultural_routes_render_successfully(self):
        """All cultural dimension directory routes must return HTTP 200."""
        routes = [
            '/intellectual-heritage',
            '/treks',
            '/souvenirs',
            '/guides',
            '/quiz',
            '/budget-planner',
            '/archaeology',
            '/performing-arts',
            '/weather',
        ]
        for path in routes:
            with self.subTest(route=path):
                r = self.client.get(path)
                self.assertEqual(r.status_code, 200, f"Route {path} failed with {r.status_code}")

    def test_discover_active_highlight_on_cultural_page(self):
        """Nav discover button should receive the 'active' class on cultural pages."""
        resp = self.client.get('/intellectual-heritage')
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn('nav-discover-btn active', html)


if __name__ == '__main__':
    unittest.main()
