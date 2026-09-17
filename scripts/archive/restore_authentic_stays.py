import os
import shutil
import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

DEST_DIR = r'd:\HiddenYatra\static\uploads\hosts\listings'
os.makedirs(DEST_DIR, exist_ok=True)

simultala_src = r'C:\Users\AKARSH RAJ\Downloads\Naldanga_Rajbari_in_Simultala,_Bihar_25.jpg'
bodh_gaya_src = r'C:\Users\AKARSH RAJ\Downloads\wallpapwr\Mahabodhi-Temple-A-Spiritual-Pilgrimage-into-the-Buddhist-Legacy.jpg'

if os.path.exists(simultala_src):
    shutil.copy2(simultala_src, os.path.join(DEST_DIR, 'simultala_stay_cover.jpg'))
    print("Copied Simultala stay image to uploads/hosts/listings/")

if os.path.exists(bodh_gaya_src):
    shutil.copy2(bodh_gaya_src, os.path.join(DEST_DIR, 'bodh_gaya_homestay_cover.jpg'))
    print("Copied Bodh Gaya homestay image to uploads/hosts/listings/")

with get_cursor(commit=True) as cur:
    # 1. Update authentic listings with real cover photos
    cur.execute("UPDATE host_listings SET cover_image = 'bodh_gaya_homestay_cover.jpg', status = 'published' WHERE id = 1")
    cur.execute("UPDATE host_listings SET cover_image = 'simultala_stay_cover.jpg', status = 'published' WHERE id = 2")

    # 2. Set test/dev listings to draft status so public /stays is pristine
    cur.execute("UPDATE host_listings SET status = 'draft' WHERE id IN (9, 17, 18)")

    print("Updated database host_listings records successfully.")

    # Verify
    cur.execute("SELECT id, title, status, cover_image FROM host_listings")
    for r in cur.fetchall():
        print(f"  Listing {r['id']}: {r['title']} -> status={r['status']}, cover={r['cover_image']}")
