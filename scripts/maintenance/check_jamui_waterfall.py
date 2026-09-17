import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor
from models.search_engine import instant_search, parse_nl_intent, get_search_index

print("=== PLACES IN JAMUI ===")
with get_cursor() as cur:
    cur.execute("""
        SELECT p.id, p.name, p.category, d.name AS district_name, p.deleted_at
        FROM places p
        JOIN districts d ON p.district_id = d.id
        WHERE d.name = 'Jamui'
    """)
    for r in cur.fetchall():
        print(f"  {r['id']}: {r['name']} (cat: {r['category']}) - deleted={r['deleted_at']}")

print("\n=== SEARCH TEST: 'waterfall near jamui' ===")
parsed = parse_natural_language_query("waterfall near jamui")
print("Parsed NL:", parsed)

results = instant_search("waterfall near jamui")
print(f"Results count: {len(results)}")
for res in results:
    print(f"  - {res['name']} ({res.get('district_name')}) [score: {res.get('score')}]")
