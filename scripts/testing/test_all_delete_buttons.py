import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from app import create_app
from models.connection import get_cursor

app = create_app()
client = app.test_client()

print("=== TESTING ALL DELETE ENDPOINTS ===")

with client.session_transaction() as sess:
    sess['admin_logged_in'] = True
    sess['user_id'] = 1
    sess['user_name'] = 'Admin'

# 1. Test Place Soft Delete
with get_cursor() as cur:
    cur.execute("SELECT id, name, deleted_at FROM places WHERE deleted_at IS NULL LIMIT 1")
    p = cur.fetchone()

if p:
    pid = p['id']
    pname = p['name']
    print(f"\n1. Testing Soft Delete on place ID {pid} ('{pname}')...")
    res = client.post(f'/admin/delete/{pid}', follow_redirects=False)
    print(f"   Status code: {res.status_code}, Location: {res.headers.get('Location')}")
    
    with get_cursor() as cur:
        cur.execute("SELECT id, name, deleted_at FROM places WHERE id = %s", (pid,))
        check_p = cur.fetchone()
        print(f"   DB deleted_at: {check_p['deleted_at']}")

    # Restore it back so we don't alter state
    print(f"   Restoring place ID {pid} back to active...")
    res_rest = client.post(f'/admin/restore/{pid}', follow_redirects=False)
    print(f"   Restore status: {res_rest.status_code}")

# 2. Test Recycle Bin Permanent Delete modal form action
print("\n2. Checking Recycle Bin Permanent Delete URL & Route...")
res_bin = client.get('/admin/recycle-bin')
print(f"   Recycle bin GET status: {res_bin.status_code}")
html = res_bin.data.decode('utf-8')
if '/admin/permanent-delete/' in html:
    print("   Found '/admin/permanent-delete/' action in recycle_bin.html")
else:
    print("   MISSING '/admin/permanent-delete/' action in recycle_bin.html")

# 3. Test Hero Media Delete
with get_cursor() as cur:
    cur.execute("SELECT id, title, filename FROM hero_media LIMIT 1")
    hm = cur.fetchone()

if hm:
    print(f"\n3. Hero media ID {hm['id']} found: {hm['filename']}")
else:
    print("\n3. Hero media table is empty.")

# 4. Check Photo Delete on place edit
with get_cursor() as cur:
    cur.execute("SELECT id, place_id, filename FROM photos LIMIT 1")
    ph = cur.fetchone()

if ph:
    print(f"\n4. Photo ID {ph['id']} (Place {ph['place_id']}): filename={ph['filename']}")
else:
    print("\n4. Photos table is empty.")
