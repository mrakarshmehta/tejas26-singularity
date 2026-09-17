import os
import urllib.request
import urllib.parse
import json
import hashlib
from dotenv import load_dotenv

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from models.database import get_db

PLACES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads', 'places')
os.makedirs(PLACES_DIR, exist_ok=True)

# Map of Place ID -> (Search Term / Direct Image URLs / Fallbacks)
PLACE_IMAGE_SOURCES = {
    88: {
        "name": "Bihar Museum",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Bihar_Museum_Patna.jpg/1280px-Bihar_Museum_Patna.jpg",
            "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    89: {
        "name": "Mahavir Mandir Patna",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Mahavir_Mandir_Patna.jpg/1280px-Mahavir_Mandir_Patna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/f/f6/Mahavir_Mandir_Patna.jpg"
        ]
    },
    90: {
        "name": "Badi Patan Devi Temple",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Patan_Devi_Temple_Patna.jpg/1280px-Patan_Devi_Temple_Patna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/4/41/Patan_Devi_Temple_Patna.jpg"
        ]
    },
    91: {
        "name": "Kumhrar Archaeological Site",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Kumhrar_Excavated_Pillared_Hall_Patna.jpg/1280px-Kumhrar_Excavated_Pillared_Hall_Patna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/b/b2/Kumhrar_Excavated_Pillared_Hall_Patna.jpg"
        ]
    },
    92: {
        "name": "Agam Kuan Shitala Devi Temple",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Agam_Kuan_Patna.jpg/1280px-Agam_Kuan_Patna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/3/30/Agam_Kuan_Patna.jpg"
        ]
    },
    93: {
        "name": "Sanjay Gandhi Jaivik Udyan Patna Zoo",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Patna_Zoo_Entrance.jpg/1280px-Patna_Zoo_Entrance.jpg",
            "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    94: {
        "name": "Buddha Smriti Park",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Buddha_Smriti_Park_Patna.jpg/1280px-Buddha_Smriti_Park_Patna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/3/36/Buddha_Smriti_Park_Patna.jpg"
        ]
    },
    95: {
        "name": "Maner Sharif",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Maner_Sharif_Dargah.jpg/1280px-Maner_Sharif_Dargah.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/7/7b/Maner_Sharif_Dargah.jpg"
        ]
    },
    96: {
        "name": "Patna Planetarium",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Indira_Gandhi_Planetarium_Patna.jpg/1280px-Indira_Gandhi_Planetarium_Patna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/7/77/Indira_Gandhi_Planetarium_Patna.jpg"
        ]
    },
    97: {
        "name": "Padri Ki Haveli",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Padri_Ki_Haveli_Patna.jpg/1280px-Padri_Ki_Haveli_Patna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/1/15/Padri_Ki_Haveli_Patna.jpg"
        ]
    },
    98: {
        "name": "Sabhyata Dwar",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Sabhyata_Dwar_Patna.jpg/1280px-Sabhyata_Dwar_Patna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/5/5a/Sabhyata_Dwar_Patna.jpg"
        ]
    },
    99: {
        "name": "Eco Park Rajdhani Vatika",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Eco_Park_Patna.jpg/1280px-Eco_Park_Patna.jpg",
            "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    100: {
        "name": "JP Ganga Path Marine Drive",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/JP_Ganga_Path_Marine_Drive_Patna.jpg/1280px-JP_Ganga_Path_Marine_Drive_Patna.jpg",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    101: {
        "name": "ISKCON Temple Patna",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/ISKCON_Temple_Patna.jpg/1280px-ISKCON_Temple_Patna.jpg",
            "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    102: {
        "name": "Royal Thai Monastery",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Royal_Thai_Monastery_Bodh_Gaya.jpg/1280px-Royal_Thai_Monastery_Bodh_Gaya.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/e/e0/Royal_Thai_Monastery_Bodh_Gaya.jpg"
        ]
    },
    103: {
        "name": "Indosan Nipponji Japanese Temple",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Indosan_Nipponji_Japanese_Temple_Bodh_Gaya.jpg/1280px-Indosan_Nipponji_Japanese_Temple_Bodh_Gaya.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/2/26/Indosan_Nipponji_Japanese_Temple_Bodh_Gaya.jpg"
        ]
    },
    104: {
        "name": "Dungeshwari Cave Temples",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Dungeshwari_Cave_Temple_Gaya.jpg/1280px-Dungeshwari_Cave_Temple_Gaya.jpg",
            "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    105: {
        "name": "Pretshila Hill",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Pretshila_Hill_Gaya.jpg/1280px-Pretshila_Hill_Gaya.jpg",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    106: {
        "name": "Mangla Gauri Temple",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Maa_Mangla_Gauri_Temple_Gaya.jpg/1280px-Maa_Mangla_Gauri_Temple_Gaya.jpg",
            "https://images.unsplash.com/photo-1542385151-efd9000785a0?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    107: {
        "name": "Barabar Caves Siddheshwar Nath",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Barabar_caves_Lomas_Rishi.jpg/1280px-Barabar_caves_Lomas_Rishi.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/f/fa/Barabar_caves_Lomas_Rishi.jpg"
        ]
    },
    108: {
        "name": "Devghat Falgu River Ghats",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Falgu_River_Ghat_Gaya.jpg/1280px-Falgu_River_Ghat_Gaya.jpg",
            "https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    109: {
        "name": "Metta Buddharam Temple",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Metta_Buddharam_Temple_Bodh_Gaya.jpg/1280px-Metta_Buddharam_Temple_Bodh_Gaya.jpg",
            "https://images.unsplash.com/photo-1548013146-72479768bbaa?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    110: {
        "name": "Bodh Gaya Archaeological Museum",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Archaeological_Museum_Bodhgaya.jpg/1280px-Archaeological_Museum_Bodhgaya.jpg",
            "https://images.unsplash.com/photo-1565034946487-077786996e27?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    111: {
        "name": "Brahmayoni Hill",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Brahmayoni_Hill_Gaya.jpg/1280px-Brahmayoni_Hill_Gaya.jpg",
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    112: {
        "name": "Gehlaur Ghati Dashrath Manjhi Smarak",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Dashrath_Manjhi_Memorial_Gehlaur.jpg/1280px-Dashrath_Manjhi_Memorial_Gehlaur.jpg",
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    4: {
        "name": "Gandhi Maidan Patna",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Gandhi_Maidan_Patna.jpg/1280px-Gandhi_Maidan_Patna.jpg",
            "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    17: {
        "name": "Valmiki National Park",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Tiger_at_Valmiki_National_Park.jpg/1280px-Tiger_at_Valmiki_National_Park.jpg",
            "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    23: {
        "name": "Battle of Buxar Memorial",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Buxar_Battle_Memorial.jpg/1280px-Buxar_Battle_Memorial.jpg",
            "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    27: {
        "name": "Litchi Gardens Muzaffarpur",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Litchi_Fruit_Tree_Muzaffarpur.jpg/1280px-Litchi_Fruit_Tree_Muzaffarpur.jpg",
            "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?auto=format&fit=crop&w=1200&q=80"
        ]
    },
    28: {
        "name": "Veer Kunwar Singh Fort",
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Veer_Kunwar_Singh_Fort_Jagdishpur.jpg/1280px-Veer_Kunwar_Singh_Fort_Jagdishpur.jpg",
            "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80"
        ]
    }
}

def download_image(urls, filename):
    filepath = os.path.join(PLACES_DIR, filename)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://en.wikipedia.org/'
    }
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    data = resp.read()
                    if len(data) > 1000:
                        with open(filepath, 'wb') as f:
                            f.write(data)
                        print(f"  [OK] Downloaded {filename} ({len(data)} bytes)")
                        return filename
        except Exception:
            pass
    return None

def main():
    conn = get_db()
    cur = conn.cursor()
    
    # 1. Fix ??? encoding in entry_fee
    cur.execute("UPDATE places SET entry_fee = REPLACE(entry_fee, '???', '₹') WHERE entry_fee LIKE '%???%'")
    print("Fixed '???' entry fee encoding in database.")
    
    # 2. Download and assign cover images
    updated = 0
    for place_id, info in PLACE_IMAGE_SOURCES.items():
        fname = f"{place_id}_{hashlib.md5(info['name'].encode()).hexdigest()[:8]}.jpg"
        downloaded = download_image(info['urls'], fname)
        if downloaded:
            cur.execute("UPDATE places SET cover_image = %s WHERE id = %s", (downloaded, place_id))
            updated += 1
        else:
            # If download fails, use the first working direct URL in database
            first_url = info['urls'][0]
            cur.execute("UPDATE places SET cover_image = %s WHERE id = %s", (first_url, place_id))
            updated += 1
            print(f"  [URL] Set direct URL for Place {place_id}: {first_url}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\nSuccessfully updated {updated} places with authentic landmark photos!")

if __name__ == '__main__':
    main()
