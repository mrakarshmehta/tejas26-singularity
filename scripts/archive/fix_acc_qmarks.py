import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from models.database import get_cursor

with get_cursor(commit=True) as cur:
    cur.execute("SELECT id, name, price_range, description FROM accommodations WHERE price_range LIKE '%?%' OR description LIKE '%?%'")
    accs = cur.fetchall()
    for a in accs:
        new_price = a['price_range'].replace('???', '₹').replace('?', '₹') if a['price_range'] else a['price_range']
        new_desc = a['description'].replace(' ??? ', ' — ').replace('???', '—') if a['description'] else a['description']
        cur.execute("UPDATE accommodations SET price_range = %s, description = %s WHERE id = %s", (new_price, new_desc, a['id']))
        print(f"Fixed Accommodation #{a['id']} {a['name']} -> price={new_price}")

print("Accommodations updated successfully.")
