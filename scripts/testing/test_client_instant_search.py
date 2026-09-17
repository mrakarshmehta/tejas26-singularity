import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from app import create_app

app = create_app()
client = app.test_client()

resp = client.get('/api/search/instant?q=Saurath')
print(f"Status: {resp.status_code}")
data = resp.get_json()
print(f"Results count: {len(data.get('results', []))}")
for r in data.get('results', []):
    print("  Match:", r.get('name'), "| District:", r.get('district_name'))
