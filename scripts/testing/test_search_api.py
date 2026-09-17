"""
Test Global Search API for key queries
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from app import create_app

app = create_app()
client = app.test_client()

terms = ["Jamui", "Nalanda", "Rajgir", "Bhagalpur", "Kaimur", "Gaya", "Patna"]

print("=" * 80)
print("GLOBAL SEARCH API VERIFICATION")
print("=" * 80)

for term in terms:
    resp = client.get(f"/api/search/instant?q={term}")
    print(f"\n🔍 Query: '{term}' (Status: {resp.status_code})")
    try:
        data = resp.get_json()
        results = data.get('results', [])
        print(f"   Found {len(results)} results:")
        for r in results[:5]:
            t = str(r.get('type') or '')
            title = str(r.get('title') or '')
            url = str(r.get('url') or '')
            print(f"     - Type: {t:10s} | Title: {title:35s} | URL: {url}")
    except Exception as e:
        print(f"   Error parsing response: {e}")
