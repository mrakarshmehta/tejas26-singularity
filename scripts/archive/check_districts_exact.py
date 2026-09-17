import sys
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

conn = get_db()
cur = conn.cursor()

cands = [
    ('Ara House', 'Bhojpur'),
    ('Ahilya Sthan, Ahiyari', 'Darbhanga'),
    ('Baba Garibnath Temple', 'Muzaffarpur'),
    ('Surya Mandir, Kandaha', 'Saharsa'),
    ('Mata Puran Devi Temple', 'Purnia'),
    ('Baba Brahmeshwar Nath Temple, Brahmpur', 'Buxar'),
    ('Gunawa Ji (Jain Tirth)', 'Nawada'),
    ('Ambika Sthan, Aami', 'Saran'),
    ('Lakri Dargah', 'Gopalganj'),
    ('Baba Tileshwar Nath Mandir, Sukhpur', 'Supaul')
]

print("QUERYING ACTUAL DISTRICTS TABLE BY NAME:")
print("-" * 60)
for place_name, dname in cands:
    cur.execute("SELECT id, name, slug FROM districts WHERE name = %s", (dname,))
    row = cur.fetchone()
    if row:
        print(f"{place_name:<38} | District: {row['name']:<12} | ID: {row['id']:<2} | Slug: {row['slug']}")
    else:
        print(f"{place_name:<38} | District: {dname:<12} | NOT FOUND!")

print("\nSPECIFIC CHECK ON BUXAR AND SARAN:")
print("-" * 60)
cur.execute("SELECT id, name, slug FROM districts WHERE id IN (2, 17, 18, 31) ORDER BY id")
for r in cur.fetchall():
    print(f"District ID {r['id']:<2} -> {r['name']:<12} ({r['slug']})")
