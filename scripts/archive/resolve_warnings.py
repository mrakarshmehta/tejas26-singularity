"""
Resolve Warning 1 (District Hero Images) and Warning 2 (Patna Block Names)
Transactional update script.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

# ═══════════════════════════════════════════════════════════════
# EXACT CANONICAL DISTRICT -> COVER IMAGE MAPPING
# ═══════════════════════════════════════════════════════════════
DISTRICT_IMAGE_MAP = {
    'patna': 'district_1_d61537eb.png',
    'gaya': 'district_3_8a0f3f75.png',          # or district_2_8350b443.jpg
    'nalanda': 'district_4_9030bb49.png',
    'jamui': 'district_22_94c91e01.png',
    'bhagalpur': 'district_7_7e3b5476.png',
    'munger': 'district_8_25a14799.png',
    'muzaffarpur': 'district_6_d1723b69.png',
    'rohtas': 'district_9_6fa2e6a2.png',
    'west-champaran': 'district_13_9b39135b.png',
    'east-champaran': 'district_14_5c785e0a.png',
    'araria': 'district_31_28eea6bf.png',
    'arwal': 'district_21_5882b2d7.png',
    'aurangabad': 'district_19_2c7ef355.png',
    'banka': 'district_35_15ccff16.png',
    'begusarai': 'district_25_bbf82b7c.png',
    'bhojpur': 'district_37_a301a6f3.png',
    'buxar': 'district_36_10be3944.png',
    'darbhanga': 'district_11_15d6f011.png',
    'gopalganj': 'district_17_04567bed.png',
    'jhanjharpur-madhubani': 'district_10_3669c268.png',
    'jehanabad': 'district_20_3a4b7de3.png',
    'kaimur': 'district_38_375abf49.png',
    'katihar': 'district_28_e9058af6.png',
    'khagaria': 'district_27_1bf95b77.png',
    'kishanganj': 'district_30_47abfa65.png',
    'lakhisarai': 'district_23_8e84d17d.png',
    'madhepura': 'district_33_ece654ac.png',
    'purnia': 'district_29_a401ffad.png',
    'saharsa': 'district_34_a8714b8b.png',
    'samastipur': 'district_26_8a5a61f7.png',
    'saran': 'district_15_11b159d1.png',
    'sheikhpura': 'district_24_420b46fc.png',
    'sheohar': 'district_39_79f6e8e8.png',
    'sitamarhi': 'district_12_61eab6f0.png',
    'siwan': 'district_16_f14ff5af.png',
    'supaul': 'district_32_2490d1be.png',
    'vaishali': 'district_5_1ebbc8c3.png',
    'nawada': 'district_18_0b820e66.png',
}

uploads_dir = r"D:\HiddenYatra\static\uploads\districts"

print("=" * 80)
print("EXECUTING WARNING RESOLUTIONS")
print("=" * 80)

# Check all image files exist first
missing_images = []
for slug, img_name in DISTRICT_IMAGE_MAP.items():
    p = os.path.join(uploads_dir, img_name)
    if not os.path.exists(p):
        missing_images.append((slug, img_name))

if missing_images:
    print(f"❌ Aborting: {len(missing_images)} image files missing:")
    for slug, img in missing_images:
        print(f"   - {slug} -> {img}")
    sys.exit(1)

print(f"✅ All {len(DISTRICT_IMAGE_MAP)} district image files verified on disk!")

# 1. Update cover_image on districts
print("\n── 1. Updating districts.cover_image pointers ──")
img_updates = 0
for slug, img_name in DISTRICT_IMAGE_MAP.items():
    cur.execute("SELECT id, name, cover_image FROM districts WHERE slug = %s", (slug,))
    row = cur.fetchone()
    if row:
        if row['cover_image'] != img_name:
            print(f"  District {row['id']:2d} ({row['name']:25s}): '{row['cover_image']}' -> '{img_name}'")
            cur.execute("UPDATE districts SET cover_image = %s WHERE id = %s", (img_name, row['id']))
            img_updates += 1
        else:
            print(f"  District {row['id']:2d} ({row['name']:25s}): already '{img_name}'")

print(f"✅ Updated {img_updates} district cover image pointers")

# 2. Update Patna block names
print("\n── 2. Updating Patna block names ──")
block_updates = [
    (2, 'danapur', 'Danapur'),
    (3, 'phulwari-sharif', 'Phulwari Sharif'),
    (4, 'maner', 'Maner'),
]

for bid, slug, correct_name in block_updates:
    cur.execute("SELECT id, name, slug FROM blocks WHERE id = %s AND slug = %s", (bid, slug))
    row = cur.fetchone()
    if row:
        print(f"  Block ID {bid} (slug: {slug}): '{row['name']}' -> '{correct_name}'")
        cur.execute("UPDATE blocks SET name = %s WHERE id = %s", (correct_name, bid))
    else:
        print(f"  ⚠️ Block ID {bid} with slug {slug} not found!")

conn.commit()
print("✅ Patna block names updated and committed!")

cur.close()
conn.close()
