import sys
import os
import csv
import math
import pymysql
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

conn = pymysql.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    port=int(os.getenv('DB_PORT', 3307)),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'hiddenyatra'),
    cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()

# 1. Load active places and districts
cur.execute("SELECT id, name, slug, category, latitude, longitude, district_id FROM places WHERE deleted_at IS NULL")
active_places = cur.fetchall()

cur.execute("SELECT id, name FROM districts")
districts = {d['name'].lower(): d['id'] for d in cur.fetchall()}

print(f"Loaded {len(active_places)} active places and {len(districts)} districts.")

# 10 proposed candidates for Batch 7
candidates = [
    {
        "rank": 1,
        "name": "Bhitiharwa Gandhi Ashram",
        "district": "West Champaran",
        "category": "historical",
        "lat": 27.2437,
        "lng": 84.4838,
        "slug": "bhitiharwa-gandhi-ashram-west-champaran",
        "primary_source": "District Administration West Champaran (NIC Portal)",
        "primary_url": "https://westchamparan.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Historic ashram and basic school founded on 20 November 1917 by Mahatma Gandhi during the historic Champaran Satyagraha. Preserves the original Kasturba Gandhi Vidyalaya hut, the historical school bell rung by Bapu, prayer grounds, and an extensive museum of freedom movement artifacts.",
        "overlap_class": "Genuinely separate destination (3.24 km SW of Rampurva Ashokan Pillars; modern national freedom struggle heritage vs ancient Mauryan pillar site)"
    },
    {
        "rank": 2,
        "name": "Baba Mahendra Nath Temple, Mehdar",
        "district": "Siwan",
        "category": "temple",
        "lat": 25.9870,
        "lng": 84.4380,
        "slug": "baba-mahendra-nath-temple-mehdar-siwan",
        "primary_source": "District Administration Siwan (NIC Portal)",
        "primary_url": "https://siwan.nic.in/tourist-place/mahendranath-temple/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Monumental 17th-century Shaivite pilgrimage complex constructed by King Mahendra Bir Bikram Shah of Nepal on the banks of the expansive 55-acre Kamaldah Lake (Sarovar) famed for water lilies. Official venue of the annual state-sponsored Mehdar Mahotsav; gives Siwan its 2nd active destination.",
        "overlap_class": "Genuinely separate destination (28.46 km SE of Zeeradei; major rural pilgrimage & lake complex)"
    },
    {
        "rank": 3,
        "name": "Jaimangla Garh",
        "district": "Begusarai",
        "category": "historical",
        "lat": 25.5921,
        "lng": 86.1613,
        "slug": "jaimangla-garh-begusarai",
        "primary_source": "District Administration Begusarai (NIC Portal)",
        "primary_url": "https://begusarai.nic.in/tourist-place/jaimangla-garh/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Ancient fortified island promontory on the southern fringe of Kabartal / Kanwar Lake, excavated by State Archaeology and ASI yielding black stone Pala-era sculptures and antiquities. Houses the sacred 9th–10th century Chandi Mangla Devi Shaktipeeth temple; gives Begusarai its 3rd active destination.",
        "overlap_class": "Genuinely separate destination (6.52 km SE of Kanwar Lake Bird Sanctuary; distinct archaeological fort mound & temple complex)"
    },
    {
        "rank": 4,
        "name": "Ramrekha Ghat",
        "district": "Buxar",
        "category": "cultural",
        "lat": 25.5761,
        "lng": 83.9711,
        "slug": "ramrekha-ghat-buxar",
        "primary_source": "District Administration Buxar (NIC Portal)",
        "primary_url": "https://buxar.nic.in/tourist-place/ramrekha-ghat/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Prime sacred Ganga riverfront ghat of Buxar where Lord Rama crossed the Ganga with Sage Vishwamitra. Enhanced with a major ₹13.24 Cr Bihar Tourism riverfront development, Ganga Aarti pavilion, steps, and promenade; host of the annual Panchkosi Parikrama mela and daily evening Maha Aarti. Gives Buxar cultural diversity beyond battlefields.",
        "overlap_class": "Legitimate companion riverfront destination (1.74 km N of Battle of Buxar Memorial; vibrant riverfront pilgrim ghat vs inland colonial battle monument park)"
    },
    {
        "rank": 5,
        "name": "Aganoor Mini Hydroelectric Project",
        "district": "Arwal",
        "category": "tourist_spot",
        "lat": 25.1328,
        "lng": 84.5385,
        "slug": "aganoor-mini-hydroelectric-project-arwal",
        "primary_source": "District Administration Arwal (NIC Portal)",
        "primary_url": "https://arwal.nic.in/tourist-place/aganoor-mini-hydroelectric-project/",
        "secondary_source": "Department of Energy, Govt of Bihar / BSEB",
        "secondary_url": "https://energy.bihar.gov.in/",
        "confidence": "A",
        "why": "Scenic barrage, mini hydel power station, and canal waterfalls on the Sone River canal network at Aganoor in Kaler block. Highly popular regional picnic spot, eco-leisure destination, and engineering marvel; gives Arwal its 2nd active destination.",
        "overlap_class": "Genuinely separate destination (18.37 km SW of Makhdum Shah Baba Dargah; scenic river barrage in southern Arwal)"
    },
    {
        "rank": 6,
        "name": "Raja Bali Ka Garh",
        "district": "Madhubani",
        "category": "historical",
        "lat": 26.4595,
        "lng": 86.3230,
        "slug": "raja-bali-ka-garh-madhubani",
        "primary_source": "Archaeological Survey of India (ASI Patna Circle)",
        "primary_url": "https://asipatnacircle.gov.in/",
        "secondary_source": "District Administration Madhubani (NIC Portal)",
        "secondary_url": "https://madhubani.nic.in/tourist-place/baligarh/",
        "confidence": "A",
        "why": "Centrally Protected Monument of National Importance under ASI (declared 1938). Sprawling 176-acre fortified ancient city at Balirajgarh (Babubarhi block) with massive brick ramparts up to 40 ft high, representing ancient Videha Kingdom urban settlement spanning NBPW, Sunga, Kushan, Gupta, and Pala eras. Gives Madhubani an archaeological marvel.",
        "overlap_class": "Genuinely separate destination (18.66 km NE of Rajnagar Palace Complex; ancient mega-fortification in eastern Madhubani)"
    },
    {
        "rank": 7,
        "name": "Dr. Rajendra Prasad Central Agricultural University",
        "district": "Samastipur",
        "category": "historical",
        "lat": 25.9860,
        "lng": 85.6754,
        "slug": "dr-rajendra-prasad-central-agricultural-university-samastipur",
        "primary_source": "District Administration Samastipur (NIC Portal)",
        "primary_url": "https://samastipur.nic.in/tourist-place/dr-rajendra-prasad-central-agricultural-university-pusa/",
        "secondary_source": "Ministry of Agriculture & Farmers Welfare, Govt of India",
        "secondary_url": "https://www.pusavarsity.org.in/",
        "confidence": "A",
        "why": "Birthplace of modern agricultural science in India, founded in 1905 by Lord Curzon with grant from Henry Phipps as the Imperial Agricultural Research Institute. Sprawling heritage campus featuring grand colonial architecture, historic Curzon Ground, botanical gardens, and agricultural museum. Gives Samastipur its 2nd active destination.",
        "overlap_class": "Genuinely separate destination (26.79 km E of Sujani Craft Cluster; 40.52 km NW of Vidyapati Dham; independent university campus)"
    },
    {
        "rank": 8,
        "name": "Baba Vishu Raut Temple, Pachrasi Dham",
        "district": "Madhepura",
        "category": "cultural",
        "lat": 25.4450,
        "lng": 87.0250,
        "slug": "baba-vishu-raut-temple-pachrasi-dham-madhepura",
        "primary_source": "District Administration Madhepura (NIC Portal)",
        "primary_url": "https://madhepura.nic.in/tourist-place/baba-vishu-raut/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Revered 300-year-old pastoral folk hero memorial and temple in Chausa block, honoring Baba Vishu Raut who defended cattle herds from wild predators. Site of an official government-recognized Rajkiya Mela every April where thousands of herders offer flowing milk in a unique ritual; gives Madhepura its 2nd active destination.",
        "overlap_class": "Genuinely separate destination (66.72 km S of Singheshwar Sthan; distinct pastoral heritage shrine in southern Madhepura)"
    },
    {
        "rank": 9,
        "name": "Kanhaiya Ji Mandir, Bandarjhula",
        "district": "Kishanganj",
        "category": "historical",
        "lat": 26.3683,
        "lng": 87.9636,
        "slug": "kanhaiya-ji-mandir-bandarjhula-kishanganj",
        "primary_source": "Archaeological Survey of India (Centrally Protected Monument List)",
        "primary_url": "https://asi.nic.in/",
        "secondary_source": "District Administration Kishanganj (NIC Portal)",
        "secondary_url": "https://kishanganj.nic.in/",
        "confidence": "A",
        "why": "Centrally Protected Monument of National Importance under ASI ('Kanhaiya ji ka mandir'). Archaeological mound near the Indo-Nepal border in Thakurganj block, housing an exquisite 8th–9th century full-size black basalt statue of Lord Vishnu/Krishna and ancient structural ruins. Gives Kishanganj its 2nd active destination.",
        "overlap_class": "Genuinely separate destination (18.28 km NW of Kishanganj Tea Gardens; standalone border archaeological monument)"
    },
    {
        "rank": 10,
        "name": "Gautam Asthan, Revelganj",
        "district": "Saran",
        "category": "cultural",
        "lat": 25.7812,
        "lng": 84.6712,
        "slug": "gautam-asthan-revelganj-saran",
        "primary_source": "District Administration Saran (NIC Portal)",
        "primary_url": "https://saran.nic.in/tourist-place/gautam-asthan/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "why": "Sacred hermitage on the holy Saryu (Ghaghara) riverbank 8 km west of Chhapra, officially recognized on Bihar Tourism's Ramayana Circuit. Commemorates Sage Maharshi Gautama and the sacred Ahilya Uddhar sthal described in Valmiki Ramayana, featuring ancient temple, river ghat, and annual Kartik Purnima fair. Gives Saran its 3rd active destination.",
        "overlap_class": "Genuinely separate destination (16.14 km NW of Chirand Archaeological Site; independent Saryu riverfront ashram)"
    }
]

print("\n--- Collision and Haversine Distance Check ---")
for c in candidates:
    clat, clng = c['lat'], c['lng']
    # check district id
    dist_name_l = c['district'].lower()
    if dist_name_l in districts:
        c['district_id'] = districts[dist_name_l]
    elif dist_name_l == 'madhubani' and 'jhanjharpur (madhubani)' in districts:
        c['district_id'] = districts['jhanjharpur (madhubani)']
    else:
        c['district_id'] = None
        
    min_dist = float('inf')
    nearest = None
    for p in active_places:
        plat, plon = float(p['latitude']), float(p['longitude'])
        d = haversine(clat, clng, plat, plon)
        if d < min_dist:
            min_dist = d
            nearest = p
            
    c['nearest_id'] = nearest['id']
    c['nearest_name'] = nearest['name']
    c['nearest_dist'] = round(min_dist, 2)
    
    # Check exact/slug matches
    exact_match = any(p['name'].lower() == c['name'].lower() for p in active_places)
    slug_match = any(p['slug'].lower() == c['slug'].lower() for p in active_places)
    
    print(f"[{c['rank']:2d}] {c['name']:<48} | Dist: {c['district']:<15} (ID:{c['district_id']}) | Cat: {c['category']:<12} | Nearest: {nearest['name'][:30]:<30} (ID:{nearest['id']:3d}) -> {c['nearest_dist']:5.2f} km | Collision: exact={exact_match}, slug={slug_match}")

print("\n--- Category Distribution ---")
cats = {}
for c in candidates:
    cats[c['category']] = cats.get(c['category'], 0) + 1
for k, v in cats.items():
    print(f"  {k}: {v}")

print("\n--- District Distribution ---")
dists = {}
for c in candidates:
    dists[c['district']] = dists.get(c['district'], 0) + 1
for k, v in dists.items():
    print(f"  {k}: {v}")
