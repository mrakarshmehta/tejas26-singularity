import os
import sys
import json
import urllib.request
import urllib.parse
import hashlib
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from models.database import get_db

PLACES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads', 'places')
os.makedirs(PLACES_DIR, exist_ok=True)

# Place ID to Wikipedia Title Mapping
WIKI_PAGES = {
    7: "Great_Buddha_Statue",
    11: "Vikramashila",
    12: "Mandar_Hill",
    14: "Tomb_of_Sher_Shah_Suri",
    15: "Rohtas_Fort",
    18: "Kesaria_stupa",
    19: "Munger_Fort",
    24: "Mundeshwari_Temple",
    25: "Janaki_Mandir",
    26: "Darbhanga_Fort",
    88: "Bihar_Museum",
    89: "Mahavir_Mandir",
    90: "Patan_Devi",
    91: "Kumhrar",
    92: "Agam_Kuan",
    93: "Sanjay_Gandhi_Jaivik_Udyan",
    94: "Buddha_Smriti_Park",
    95: "Maner_Sharif",
    96: "Indira_Gandhi_Planetarium",
    97: "Padri_Ki_Haveli",
    98: "Sabhyata_Dwar",
    99: "Eco_Park,_Patna",
    100: "Loknayak_Ganga_Path",
    101: "ISKCON_Temple_Patna",
    102: "Wat_Thai_Bodhgaya",
    103: "Bodh_Gaya",
    104: "Dungeshwari_Cave_Temples",
    105: "Pretshila_Hill",
    106: "Mangla_Gauri_Temple",
    107: "Barabar_Caves",
    108: "Falgu_River",
    109: "Bodh_Gaya",
    110: "Archaeological_Museum,_Bodh_Gaya",
    111: "Gaya,_India",
    112: "Dashrath_Manjhi",
    4: "Gandhi_Maidan",
    17: "Valmiki_National_Park",
    23: "Battle_of_Buxar",
    27: "Muzaffarpur",
    28: "Kunwar_Singh"
}

HEADERS = {
    'User-Agent': 'HiddenYatra/1.0 (https://hiddenyatra.onrender.com; contact@hiddenyatra.in) python-requests/2.31'
}

def get_wiki_image_url(title):
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=1000"
    try:
        req = urllib.request.Request(api_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for page in pages.values():
                thumb = page.get('thumbnail', {})
                if 'source' in thumb:
                    return thumb['source']
    except Exception as e:
        print(f"  Wiki API error for {title}: {e}")
    return None

def download_file(url, out_path):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            if len(content) > 1000:
                with open(out_path, 'wb') as f:
                    f.write(content)
                return True
    except Exception as e:
        print(f"  Download error: {e}")
    return False

def main():
    conn = get_db()
    cur = conn.cursor()

    # Fix entry_fee encoding
    cur.execute("UPDATE places SET entry_fee = REPLACE(entry_fee, '???', '₹') WHERE entry_fee LIKE '%???%'")
    print("Fixed currency symbol encoding in places table.")

    success_count = 0
    for place_id, wiki_title in WIKI_PAGES.items():
        cur.execute("SELECT id, name, cover_image FROM places WHERE id = %s", (place_id,))
        row = cur.fetchone()
        if not row:
            continue

        place_name = row['name']
        current_cover = row.get('cover_image', '')

        # Check if we already have a valid local image file
        if current_cover and not current_cover.startswith('http'):
            local_existing = os.path.join(PLACES_DIR, current_cover)
            if os.path.exists(local_existing) and os.path.getsize(local_existing) > 5000:
                print(f"[EXISTS] Place {place_id} ({place_name}) already has {current_cover}")
                continue

        print(f"[FETCHING] Place {place_id} ({place_name}) via Wikipedia: {wiki_title}...")
        img_url = get_wiki_image_url(wiki_title)
        if not img_url:
            print(f"  No thumbnail found for {wiki_title}")
            continue

        ext = '.png' if '.png' in img_url.lower() else '.jpg'
        out_filename = f"{place_id}_{hashlib.md5(place_name.encode()).hexdigest()[:8]}{ext}"
        out_filepath = os.path.join(PLACES_DIR, out_filename)

        if download_file(img_url, out_filepath):
            cur.execute("UPDATE places SET cover_image = %s WHERE id = %s", (out_filename, place_id))
            conn.commit()
            success_count += 1
            print(f"  [SAVED] {place_name} -> {out_filename} ({os.path.getsize(out_filepath)} bytes)")
        else:
            # Fallback to direct URL if download failed
            cur.execute("UPDATE places SET cover_image = %s WHERE id = %s", (img_url, place_id))
            conn.commit()
            print(f"  [SET URL] {place_name} -> {img_url[:60]}...")

        time.sleep(0.3)

    cur.close()
    conn.close()
    print(f"\nAll complete! Downloaded and linked {success_count} authentic landmark photos.")

if __name__ == '__main__':
    main()
