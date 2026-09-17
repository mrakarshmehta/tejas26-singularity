"""
Audit District and Place Cover Images
Check image files and paths in static directory.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("SELECT id, name, slug, cover_image, image_url FROM districts ORDER BY id")
districts = cur.fetchall()

uploads_districts = r"D:\HiddenYatra\static\uploads\districts"
img_districts = r"D:\HiddenYatra\static\images\districts"

print("Uploads dir exists:", os.path.exists(uploads_districts))
print("Images dir exists:", os.path.exists(img_districts))

for d in districts:
    cov = d.get('cover_image') or ''
    exists_uploads = os.path.exists(os.path.join(uploads_districts, cov)) if cov else False
    print(f"District {d['id']:2d} | {d['name']:25s} | slug: {d['slug']:20s} | cover_img: {cov:30s} | exists: {exists_uploads}")

cur.close()
conn.close()
