import sys
import os
import csv
import math
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

sys.stdout.reconfigure(encoding='utf-8')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 1. Load active places and districts from MySQL
with get_cursor() as cursor:
    cursor.execute("SELECT id, name, slug, category, latitude, longitude, district_id FROM places WHERE deleted_at IS NULL")
    active_places = cursor.fetchall()
    
    cursor.execute("SELECT id, name FROM districts")
    districts = {d['name'].lower(): d['id'] for d in cursor.fetchall()}

print(f"Loaded {len(active_places)} active places and {len(districts)} districts.")

# 10 proposed candidates for Batch 6
proposed = [
    {
        "rank": 1,
        "name": "Kahalgaon Rock-Cut Temples",
        "district": "Bhagalpur",
        "category": "historical",
        "lat": 25.2689,
        "lng": 87.2345,
        "slug": "kahalgaon-rock-cut-temples-bhagalpur",
        "primary_source": "Archaeological Survey of India (ASI Patna Circle)",
        "primary_url": "https://asipatnacircle.gov.in/",
        "secondary_source": "District Administration Bhagalpur (NIC Portal)",
        "secondary_url": "https://bhagalpur.nic.in/tourist-places/",
        "confidence": "A",
        "why": "Centrally Protected Monument under ASI. Monolithic 7th–8th century rock-cut boulder temples and reliefs carved into granitic islands in the bed of River Ganga.",
        "overlap_class": "Distinct Heritage Site (>8 km from nearest active place)"
    },
    {
        "rank": 2,
        "name": "Vishwa Shanti Stupa & Ratnagiri Ropeway",
        "district": "Nalanda",
        "category": "cultural",
        "lat": 25.0085,
        "lng": 85.4385,
        "slug": "vishwa-shanti-stupa-and-ratnagiri-ropeway-nalanda",
        "primary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "primary_url": "https://tourism.bihar.gov.in/en/destinations",
        "secondary_source": "District Administration Nalanda (NIC Portal)",
        "secondary_url": "https://nalanda.nic.in/tourist-places/",
        "confidence": "A",
        "why": "Iconic 125-foot white marble World Peace Pagoda atop Ratnagiri Hill, accessed via Bihar's premier aerial chairlift ropeway operated by BSTDC. Consecrated in 1969 by Nichidatsu Fujii.",
        "overlap_class": "Companion Landmark (2.87 km SE of Rajgir valley; independent aerial ropeway infrastructure)"
    },
    {
        "rank": 3,
        "name": "Shringirishi Dham",
        "district": "Lakhisarai",
        "category": "nature",
        "lat": 25.1278,
        "lng": 86.2344,
        "slug": "shringirishi-dham-lakhisarai",
        "primary_source": "District Administration Lakhisarai (NIC Portal)",
        "primary_url": "https://lakhisarai.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Enchanting scenic valley in Kharagpur hills with natural perennial waterfalls, Sita Kund hot water springs, reservoir dam, and Ramayana Putrakameshti Yajna Sage Shringi lore.",
        "overlap_class": "Independent Regional Eco-Nature Destination (>13 km from nearest active place)"
    },
    {
        "rank": 4,
        "name": "Girihinda Pahar & Shiv Temple",
        "district": "Sheikhpura",
        "category": "mountain",
        "lat": 25.1385,
        "lng": 85.8562,
        "slug": "girihinda-pahar-and-shiv-temple-sheikhpura",
        "primary_source": "District Administration Sheikhpura (NIC Portal)",
        "primary_url": "https://sheikhpura.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Standalone 500-foot rocky granite hill rising above Sheikhpura town with 360-degree plains panorama, rock steps, children's park, and ancient Baba Kameshwar Nath Shiva shrine. Adds the rare 'mountain' category.",
        "overlap_class": "Independent Mountain Landmark (>13 km from nearest active place)"
    },
    {
        "rank": 5,
        "name": "Matsyagandha Lake & Raktakali Temple",
        "district": "Saharsa",
        "category": "lake",
        "lat": 25.8825,
        "lng": 86.5985,
        "slug": "matsyagandha-lake-and-raktakali-temple-saharsa",
        "primary_source": "District Administration Saharsa (NIC Portal)",
        "primary_url": "https://saharsa.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Expansive 80-acre lake complex developed under Jal-Jeevan-Hariyali mission featuring boating, landscaped gardens, and a unique oval-shaped 64-Yogini (Chausath Yogini) Raktakali Temple with engraved stone reliefs.",
        "overlap_class": "Independent Lake & Tantric Temple (>15 km from nearest active place)"
    },
    {
        "rank": 6,
        "name": "Kajha Kothi Eco Park",
        "district": "Purnia",
        "category": "nature",
        "lat": 25.7185,
        "lng": 87.3512,
        "slug": "kajha-kothi-eco-park-purnia",
        "primary_source": "District Administration Purnia (NIC Portal)",
        "primary_url": "https://purnea.nic.in/tourist-places/",
        "secondary_source": "Department of Environment, Forest and Climate Change, Bihar",
        "secondary_url": "https://forest.bihar.gov.in/",
        "confidence": "A",
        "why": "Historic 1775 British-era indigo plantation bungalow estate on the Kajri river, developed into an eco-tourism lake park with pedal boating, gardens, and picnic grounds (Shastri Park).",
        "overlap_class": "Independent Eco-Park & Colonial Heritage (>26 km from nearest active place)"
    },
    {
        "rank": 7,
        "name": "Guru Tegh Bahadur Historic Gurdwara, Lakshmipur",
        "district": "Katihar",
        "category": "cultural",
        "lat": 25.3912,
        "lng": 87.2812,
        "slug": "guru-tegh-bahadur-historic-gurdwara-lakshmipur-katihar",
        "primary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "primary_url": "https://tourism.bihar.gov.in/en/destinations",
        "secondary_source": "District Administration Katihar (NIC Portal)",
        "secondary_url": "https://katihar.nic.in/tourist-places/",
        "confidence": "A",
        "why": "Key destination on Bihar Tourism's official Sikh Circuit. Commemorates the 1670 visit of 9th Sikh Guru Sri Guru Tegh Bahadur Ji at historic Kantanagar; preserves original 17th-century Hukumnamas and handwritten Guru Granth Sahib.",
        "overlap_class": "Independent Sikh Pilgrimage Site (>18 km from nearest active place)"
    },
    {
        "rank": 8,
        "name": "Dighwa Dubauli Archaeological Mounds",
        "district": "Gopalganj",
        "category": "historical",
        "lat": 26.2485,
        "lng": 84.7312,
        "slug": "dighwa-dubauli-archaeological-mounds-gopalganj",
        "primary_source": "District Administration Gopalganj (NIC Portal)",
        "primary_url": "https://gopalganj.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Remarkable pyramidal star-shaped earthen mounds attributed to ancient Chero rulers; famous site of the 761–762 AD Dighwa-Dubauli copper plate inscription of King Mahendrapala I.",
        "overlap_class": "Independent Ancient Archaeological Site (>14 km from nearest active place)"
    },
    {
        "rank": 9,
        "name": "Champanagar Ancient Capital & Jain Tirth",
        "district": "Bhagalpur",
        "category": "cultural",
        "lat": 25.2312,
        "lng": 86.9245,
        "slug": "champanagar-ancient-capital-and-jain-tirth-bhagalpur",
        "primary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "primary_url": "https://tourism.bihar.gov.in/en/destinations",
        "secondary_source": "District Administration Bhagalpur (NIC Portal)",
        "secondary_url": "https://bhagalpur.nic.in/tourist-places/",
        "confidence": "A",
        "why": "Ancient fortified capital of Anga Mahajanapada (Champa / Karna Garh) and supreme Jain Panch Kalyanaka kshetra where 12th Tirthankara Bhagwan Vasupujya was born and attained all five spiritual milestones.",
        "overlap_class": "Independent Mahajanapada & Jain Capital (>11 km from nearest active place)"
    },
    {
        "rank": 10,
        "name": "Deokund",
        "district": "Aurangabad",
        "category": "temple",
        "lat": 24.9512,
        "lng": 84.5829,
        "slug": "deokund-aurangabad",
        "primary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "primary_url": "https://tourism.bihar.gov.in/en/destinations",
        "secondary_source": "District Administration Aurangabad (NIC Portal)",
        "secondary_url": "https://aurangabad.bih.nic.in/tourist-places/",
        "confidence": "A",
        "why": "Ancient Shaivite pilgrimage center housing the Baba Dudheshwar Nath Shiva temple, sacred perennial kund/spring, and hermitage traditions of Sage Chyavana. Major Mahashivratri gathering.",
        "overlap_class": "Independent Ancient Pilgrimage & Kund (>20 km from nearest active place)"
    }
]

print("\n=== COLLISION & PROXIMITY AUDIT FOR BATCH 6 CANDIDATES ===")
allowed_categories = {'tourist_spot', 'temple', 'food_place', 'hidden_gem', 'nature', 'historical', 'beach', 'mountain', 'market', 'adventure', 'cultural', 'waterfall', 'lake', 'other'}

for c in proposed:
    # 1. District ID
    d_name = c['district'].lower()
    if d_name in districts:
        c['district_id'] = districts[d_name]
    else:
        print(f"ERROR: District {c['district']} not found in DB!")
    
    # 2. Category
    if c['category'] not in allowed_categories:
        print(f"ERROR: Category {c['category']} not in allowed list!")
    
    # 3. Collision check
    min_dist = 9999.0
    nearest_p = None
    for p in active_places:
        # name collision
        if c['name'].lower() == p['name'].lower():
            print(f"COLLISION: Name match with ID {p['id']} ({p['name']})")
        # slug collision
        if c['slug'] == p['slug']:
            print(f"COLLISION: Slug match with ID {p['id']} ({p['slug']})")
        # coordinate distance
        if p['latitude'] and p['longitude']:
            d = haversine(c['lat'], c['lng'], float(p['latitude']), float(p['longitude']))
            if d < min_dist:
                min_dist = d
                nearest_p = p
    
    c['min_dist'] = min_dist
    c['nearest_place'] = nearest_p['name'] if nearest_p else "None"
    c['nearest_id'] = nearest_p['id'] if nearest_p else None

    print(f"Rank {c['rank']:2d}: {c['name']:<48} | Dist: {c['district']:<14} (ID {c['district_id']:2d}) | Cat: {c['category']:<10} | Nearest: {c['nearest_place']} (ID {c['nearest_id']}) -> {c['min_dist']:.2f} km")

print("\nAll 10 candidates audited successfully.")
