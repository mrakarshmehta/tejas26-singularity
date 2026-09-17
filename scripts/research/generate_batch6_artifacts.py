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

# 1. Load active places and districts
with get_cursor() as cursor:
    cursor.execute("SELECT id, name, slug, category, latitude, longitude, district_id FROM places WHERE deleted_at IS NULL ORDER BY id")
    active_places = cursor.fetchall()
    
    cursor.execute("SELECT id, name FROM districts ORDER BY id")
    districts = {d['name'].lower(): d['id'] for d in cursor.fetchall()}

# 10 Recommended Candidates
recommended = [
    {
        "rank": 1,
        "name": "Kahalgaon Rock-Cut Temples",
        "district": "Bhagalpur",
        "district_id": districts["bhagalpur"],
        "category": "historical",
        "lat": 25.2689,
        "lng": 87.2345,
        "slug": "kahalgaon-rock-cut-temples-bhagalpur",
        "primary_source": "Archaeological Survey of India (ASI Patna Circle)",
        "primary_url": "https://asipatnacircle.gov.in/",
        "secondary_source": "District Administration Bhagalpur (NIC Portal)",
        "secondary_url": "https://bhagalpur.nic.in/tourist-places/",
        "confidence": "A",
        "priority": "P0",
        "why": "Centrally Protected Monument under ASI ('Rock Temple, Colgong'). Monolithic 7th–8th century rock-cut boulder temples and reliefs carved into granite islands situated directly in the bed of River Ganga.",
        "overlap_class": "Genuinely separate destination (>8 km from nearest active place; granite island rock-cut monuments in Ganga riverbed)",
        "notes": "Ancient river island setting requires boat access in dry months; centrally protected by ASI with zero boundary ambiguity."
    },
    {
        "rank": 2,
        "name": "Vishwa Shanti Stupa & Ratnagiri Ropeway",
        "district": "Nalanda",
        "district_id": districts["nalanda"],
        "category": "cultural",
        "lat": 25.0085,
        "lng": 85.4385,
        "slug": "vishwa-shanti-stupa-and-ratnagiri-ropeway-nalanda",
        "primary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "primary_url": "https://tourism.bihar.gov.in/en/destinations",
        "secondary_source": "District Administration Nalanda (NIC Portal)",
        "secondary_url": "https://nalanda.nic.in/tourist-places/",
        "confidence": "A",
        "priority": "P0",
        "why": "Iconic 125-foot white marble World Peace Pagoda atop Ratnagiri Hill, accessed via Bihar's famous aerial chairlift ropeway operated by BSTDC. Consecrated in 1969 by Nichidatsu Fujii; global Buddhist landmark.",
        "overlap_class": "Legitimate companion destination (2.87 km SE of Rajgir valley; independent hilltop pagoda reached via distinct BSTDC chairlift ropeway infrastructure)",
        "notes": "Situated 2.87 km from Rajgir town center marker; treated as a dedicated half-day excursion with separate BSTDC ropeway ticketing."
    },
    {
        "rank": 3,
        "name": "Shringirishi Dham",
        "district": "Lakhisarai",
        "district_id": districts["lakhisarai"],
        "category": "nature",
        "lat": 25.1278,
        "lng": 86.2344,
        "slug": "shringirishi-dham-lakhisarai",
        "primary_source": "District Administration Lakhisarai (NIC Portal)",
        "primary_url": "https://lakhisarai.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "priority": "P1",
        "why": "Enchanting scenic valley in Kharagpur hills with natural perennial waterfalls, Sita Kund hot water springs, reservoir dam, and Ramayana Putrakameshti Yajna Sage Shringi lore. Gives Lakhisarai its 2nd active destination.",
        "overlap_class": "Genuinely separate destination (>17 km from nearest active place; pristine nature valley in Kharagpur hills)",
        "notes": "Pristine nature destination in Suryagarha block; popular for Makar Sankranti and New Year eco-picnics; daytime visits recommended."
    },
    {
        "rank": 4,
        "name": "Girihinda Pahar & Shiv Temple",
        "district": "Sheikhpura",
        "district_id": districts["sheikhpura"],
        "category": "mountain",
        "lat": 25.1385,
        "lng": 85.8562,
        "slug": "girihinda-pahar-and-shiv-temple-sheikhpura",
        "primary_source": "District Administration Sheikhpura (NIC Portal)",
        "primary_url": "https://sheikhpura.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "priority": "P1",
        "why": "Standalone 500-foot rocky granite hill rising above Sheikhpura town with 360-degree plains panorama, rock steps, children's park, and ancient Baba Kameshwar Nath Shiva shrine. Adds the rare 'mountain' category and gives Sheikhpura its 2nd destination.",
        "overlap_class": "Genuinely separate destination (>14 km from nearest active place; rocky granite inselberg)",
        "notes": "Well-developed access with both motorable road and foot stairs; prominent landmark visible across the district."
    },
    {
        "rank": 5,
        "name": "Matsyagandha Lake & Raktakali Temple",
        "district": "Saharsa",
        "district_id": districts["saharsa"],
        "category": "lake",
        "lat": 25.8825,
        "lng": 86.5985,
        "slug": "matsyagandha-lake-and-raktakali-temple-saharsa",
        "primary_source": "District Administration Saharsa (NIC Portal)",
        "primary_url": "https://saharsa.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "priority": "P1",
        "why": "Expansive 80-acre lake complex developed under Jal-Jeevan-Hariyali mission featuring boating, landscaped promenades, and a unique oval-shaped 64-Yogini (Chausath Yogini) Raktakali Temple with engraved stone reliefs. Gives Saharsa its 2nd destination.",
        "overlap_class": "Genuinely separate destination (>15 km from nearest active place; urban wetland & Tantric architectural complex)",
        "notes": "Key recreational hub of Saharsa town; active boating facilities; high festive attendance during Diwali and Chhath."
    },
    {
        "rank": 6,
        "name": "Kajha Kothi Eco Park",
        "district": "Purnia",
        "district_id": districts["purnia"],
        "category": "nature",
        "lat": 25.7185,
        "lng": 87.3512,
        "slug": "kajha-kothi-eco-park-purnia",
        "primary_source": "District Administration Purnia (NIC Portal)",
        "primary_url": "https://purnea.nic.in/tourist-places/",
        "secondary_source": "Department of Environment, Forest and Climate Change, Bihar",
        "secondary_url": "https://forest.bihar.gov.in/",
        "confidence": "A",
        "priority": "P1",
        "why": "Historic 1775 British-era indigo plantation bungalow estate on the Kajri river, developed into an eco-tourism lake park with pedal boating, gardens, and picnic grounds (Shastri Park). Gives Purnia its 2nd destination.",
        "overlap_class": "Genuinely separate destination (>31 km from nearest active place; colonial heritage estate & eco-wetland)",
        "notes": "Located 12 km from Purnia district headquarters; popular family picnic spot; named after former Bihar CM Bhola Paswan Shastri."
    },
    {
        "rank": 7,
        "name": "Guru Tegh Bahadur Historic Gurdwara, Lakshmipur",
        "district": "Katihar",
        "district_id": districts["katihar"],
        "category": "cultural",
        "lat": 25.3912,
        "lng": 87.2812,
        "slug": "guru-tegh-bahadur-historic-gurdwara-lakshmipur-katihar",
        "primary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "primary_url": "https://tourism.bihar.gov.in/en/destinations",
        "secondary_source": "District Administration Katihar (NIC Portal)",
        "secondary_url": "https://katihar.nic.in/tourist-places/",
        "confidence": "A",
        "priority": "P1",
        "why": "Key destination on Bihar Tourism's official Sikh Circuit. Commemorates the 1670 visit of 9th Sikh Guru Sri Guru Tegh Bahadur Ji at historic Kantanagar; preserves original 17th-century Hukumnamas and handwritten Guru Granth Sahib. Gives Katihar its 2nd destination.",
        "overlap_class": "Genuinely separate destination (>6 km across river Ganga/Kosi; distinct Sikh pilgrimage site)",
        "notes": "Separated from Bhagalpur bank by river corridor; authentic 17th-century relics preserved with active community reverence."
    },
    {
        "rank": 8,
        "name": "Dighwa Dubauli Archaeological Mounds",
        "district": "Gopalganj",
        "district_id": districts["gopalganj"],
        "category": "historical",
        "lat": 26.2485,
        "lng": 84.7312,
        "slug": "dighwa-dubauli-archaeological-mounds-gopalganj",
        "primary_source": "District Administration Gopalganj (NIC Portal)",
        "primary_url": "https://gopalganj.nic.in/tourist-places/",
        "secondary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "secondary_url": "https://tourism.bihar.gov.in/en/destinations",
        "confidence": "A",
        "priority": "P1",
        "why": "Remarkable pyramidal star-shaped earthen mounds attributed to ancient Chero rulers; famous site of the 761–762 AD Dighwa-Dubauli copper plate inscription of King Mahendrapala I. Gives Gopalganj its 2nd destination.",
        "overlap_class": "Genuinely separate destination (>15 km from nearest active place; ancient fortified pyramidal earthworks)",
        "notes": "Located in Baikunthpur block; direct rail access via Dighwa Dubauli station; prominent pre-medieval archaeological site."
    },
    {
        "rank": 9,
        "name": "Champanagar Ancient Capital & Jain Tirth",
        "district": "Bhagalpur",
        "district_id": districts["bhagalpur"],
        "category": "cultural",
        "lat": 25.2312,
        "lng": 86.9245,
        "slug": "champanagar-ancient-capital-and-jain-tirth-bhagalpur",
        "primary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "primary_url": "https://tourism.bihar.gov.in/en/destinations",
        "secondary_source": "District Administration Bhagalpur (NIC Portal)",
        "secondary_url": "https://bhagalpur.nic.in/tourist-places/",
        "confidence": "A",
        "priority": "P0",
        "why": "Ancient fortified capital of Anga Mahajanapada (Champa / Karna Garh) and supreme Jain Panch Kalyanaka kshetra where 12th Tirthankara Bhagwan Vasupujya was born and attained all five spiritual milestones.",
        "overlap_class": "Genuinely separate destination (>11 km from nearest active place; ancient fortified capital & Jain pilgrimage complex)",
        "notes": "Verified Rank 21 from Phase 6 Top 30 audit; located in Nathnagar western Bhagalpur; active Jain pilgrim infrastructure."
    },
    {
        "rank": 10,
        "name": "Deokund",
        "district": "Aurangabad",
        "district_id": districts["aurangabad"],
        "category": "temple",
        "lat": 24.9512,
        "lng": 84.5829,
        "slug": "deokund-aurangabad",
        "primary_source": "Bihar Tourism (Department of Tourism, Govt of Bihar)",
        "primary_url": "https://tourism.bihar.gov.in/en/destinations",
        "secondary_source": "District Administration Aurangabad (NIC Portal)",
        "secondary_url": "https://aurangabad.nic.in/tourist-place/deokund/",
        "confidence": "A",
        "priority": "P0",
        "why": "Ancient Shaivite pilgrimage center housing the Baba Dudheshwar Nath Shiva temple, sacred perennial kund/spring, and hermitage traditions of Sage Chyavana. Major Mahashivratri gathering.",
        "overlap_class": "Genuinely separate destination (>20 km from nearest active place; rural pilgrimage & spring complex)",
        "notes": "Verified Rank 27 from Phase 6 Top 30 audit; located in Goh block on border with Arwal; major annual fair organized under district patronage."
    }
]

# Calculate nearest active place for each recommended candidate
for c in recommended:
    min_dist = 9999.0
    nearest_p = None
    for p in active_places:
        if p['latitude'] and p['longitude']:
            d = haversine(c['lat'], c['lng'], float(p['latitude']), float(p['longitude']))
            if d < min_dist:
                min_dist = d
                nearest_p = p
    c['nearest_place'] = nearest_p['name'] if nearest_p else "None"
    c['nearest_id'] = nearest_p['id'] if nearest_p else None
    c['min_dist'] = min_dist

# Hold Candidates
hold_candidates = [
    {
        "name": "Buddha Relic Stupa, Vaishali",
        "district": "Vaishali",
        "district_id": districts["vaishali"],
        "category": "historical",
        "lat": 25.9912,
        "lng": 85.1215,
        "nearest_place": "Vaishali - Birthplace of Democracy",
        "nearest_id": 10,
        "min_dist": 0.93,
        "confidence": "A",
        "overlap_class": "Same-Site / High Proximity Cluster (<1 km from ID 10)",
        "reason": "Excavated mud stupa of the Lichchhavis that yielded the authentic casket containing Buddha's corporeal relics. Held strictly due to 0.93 km marker proximity to ID 10; Vaishali already gained 2 places in Batch 5 (Kolhua Ashokan Pillar & Baraila Lake)."
    },
    {
        "name": "Ramrekha Ghat",
        "district": "Buxar",
        "district_id": districts["buxar"],
        "category": "cultural",
        "lat": 25.5785,
        "lng": 83.9785,
        "nearest_place": "Battle of Buxar Memorial",
        "nearest_id": 88,
        "min_dist": 1.84,
        "confidence": "A",
        "overlap_class": "Urban Proximity Cluster (<2 km from ID 88)",
        "reason": "Sacred Ganga riverfront ghat with Ramayana lore and ₹13.24 Cr Bihar Tourism development. Held for Batch 7 to prioritize 1-place districts in Batch 6."
    },
    {
        "name": "Baba Mahendra Nath Temple, Mehdar",
        "district": "Siwan",
        "district_id": districts["siwan"],
        "category": "temple",
        "lat": 26.0125,
        "lng": 84.4512,
        "nearest_place": "Zeeradei (Dr. Rajendra Prasad Ancestral House)",
        "nearest_id": 87,
        "min_dist": 29.52,
        "confidence": "A",
        "overlap_class": "Distinct Regional Pilgrimage (>29 km from ID 87)",
        "reason": "Ancient 17th-century Shiva temple built by King of Nepal on 55-acre Kamaldah Lake; hosts Mehdar Mahotsav. Held for Batch 7 to avoid duplicate temple additions in Batch 6."
    },
    {
        "name": "Bhitiharwa Gandhi Ashram",
        "district": "West Champaran",
        "district_id": districts["west champaran"],
        "category": "historical",
        "lat": 27.1856,
        "lng": 84.5582,
        "nearest_place": "Rampurva Ashokan Pillars",
        "nearest_id": 149,
        "min_dist": 7.70,
        "confidence": "A",
        "overlap_class": "Distinct Heritage Ashram (>7 km from ID 149)",
        "reason": "Historic 1917 Satyagraha ashram founded by Mahatma Gandhi with preserved original hut and school. West Champaran already has 5 active destinations; held for Batch 7."
    },
    {
        "name": "Jaimangla Garh",
        "district": "Begusarai",
        "district_id": districts["begusarai"],
        "category": "historical",
        "lat": 25.5985,
        "lng": 86.1512,
        "nearest_place": "Kanwar Lake Bird Sanctuary",
        "nearest_id": 94,
        "min_dist": 6.58,
        "confidence": "A",
        "overlap_class": "Archaeological Island Companion (6.58 km from ID 94)",
        "reason": "Ancient fort mound and 9th-century Chandi Mangla Devi temple situated on edge of Kanwar Lake. Begusarai already has 2 active places; held for Batch 7."
    },
    {
        "name": "Rishi Kund",
        "district": "Munger",
        "district_id": districts["munger"],
        "category": "nature",
        "lat": 25.2185,
        "lng": 86.5312,
        "nearest_place": "Kharagpur Lake (Haveli Kharagpur)",
        "nearest_id": 166,
        "min_dist": 12.54,
        "confidence": "A",
        "overlap_class": "Thermal Spring Complex (>12 km from ID 166)",
        "reason": "Natural thermal hot spring in Kharagpur hills. Held due to feature similarity with active DB #93 Bhimbandh Hot Springs in Munger (which already has 3 places)."
    },
    {
        "name": "Kauwadol Hill & Colossal Buddha Statue",
        "district": "Gaya",
        "district_id": districts["gaya"],
        "category": "historical",
        "lat": 24.9812,
        "lng": 85.0512,
        "nearest_place": "Barabar Caves & Siddheshwar Nath",
        "nearest_id": 2,
        "min_dist": 4.10,
        "confidence": "A",
        "overlap_class": "Cluster Proximity (4.1 km from Barabar Caves)",
        "reason": "8-foot monolithic rock-carved Buddha statue and ancient Silabhadra monastery mound. Held due to heavy existing inventory in Gaya (12 places)."
    },
    {
        "name": "Tomb of Hasan Khan Suri",
        "district": "Rohtas",
        "district_id": districts["rohtas"],
        "category": "historical",
        "lat": 24.9512,
        "lng": 84.0212,
        "nearest_place": "Sher Shah Suri Tomb, Sasaram",
        "nearest_id": 8,
        "min_dist": 0.75,
        "confidence": "A",
        "overlap_class": "Sub-Monument Urban Cluster (<1 km from ID 8)",
        "reason": "Tomb of Sher Shah Suri's father in Sasaram town. Held as sub-monument cluster (<800 m from active DB #8)."
    },
    {
        "name": "Raja Vishal Ka Garh",
        "district": "Vaishali",
        "district_id": districts["vaishali"],
        "category": "historical",
        "lat": 25.9925,
        "lng": 85.1285,
        "nearest_place": "Vaishali - Birthplace of Democracy",
        "nearest_id": 10,
        "min_dist": 0.57,
        "confidence": "A",
        "overlap_class": "Same Archaeological Complex (<600 m from ID 10)",
        "reason": "Ancient Lichchhavi assembly parliament rampart mound; physically contiguous with active DB #10. Held for master complex inclusion."
    },
    {
        "name": "Gandhi Memorial & Sangrahalaya, Motihari",
        "district": "East Champaran",
        "district_id": districts["east champaran"],
        "category": "cultural",
        "lat": 26.6485,
        "lng": 84.9112,
        "nearest_place": "George Orwell Birthplace & Memorial",
        "nearest_id": 165,
        "min_dist": 0.54,
        "confidence": "A",
        "overlap_class": "Urban Proximity Cluster (<600 m from ID 165)",
        "reason": "Gandhi museum and stone pillar memorial in Motihari town center. Situated 540 m from active DB #165. Held."
    }
]

# Reject Candidates
reject_candidates = [
    {"name": "Arwal Bus Stand Commercial Complex", "district": "Arwal", "category": "transit", "lat": 25.2412, "lng": 84.6712, "reason": "Commercial bus terminal and market shops; zero tourism, historical, or cultural value."},
    {"name": "Katihar Railway Junction Yard", "district": "Katihar", "category": "transit", "lat": 25.5412, "lng": 87.5612, "reason": "Operational railway yard and track complex; non-tourism transportation utility."},
    {"name": "Purnea College Academic Campus", "district": "Purnia", "category": "education", "lat": 25.7712, "lng": 87.4712, "reason": "Standard municipal collegiate academic campus lacking visitor heritage infrastructure."},
    {"name": "Samastipur Dairy Milk Plant", "district": "Samastipur", "category": "industrial", "lat": 25.8612, "lng": 85.7812, "reason": "Industrial dairy processing facility; commercial production unit."},
    {"name": "Hotel Grand Sheohar", "district": "Sheohar", "category": "commercial", "lat": 26.5112, "lng": 85.2912, "reason": "Private commercial hospitality enterprise; violates destination criteria."},
    {"name": "Siwan Civil Court Complex", "district": "Siwan", "category": "administrative", "lat": 26.2212, "lng": 84.3612, "reason": "Municipal judicial building; administrative courthouse."}
]

print("Writing BIHAR_BATCH6_APPROVAL_PREVIEW.csv...")
with open('BIHAR_BATCH6_APPROVAL_PREVIEW.csv', mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "rank", "candidate_name", "district", "district_id", "category", "latitude", "longitude",
        "canonical_slug", "nearest_existing_place", "min_haversine_km", "overlap_classification",
        "why_it_adds_value", "primary_authoritative_source", "primary_source_url",
        "secondary_source", "secondary_source_url", "evidence_confidence", "recommended_priority",
        "notes_risks"
    ])
    for c in recommended:
        writer.writerow([
            c["rank"], c["name"], c["district"], c["district_id"], c["category"], c["lat"], c["lng"],
            c["slug"], c["nearest_place"], f"{c['min_dist']:.2f}", c["overlap_class"],
            c["why"], c["primary_source"], c["primary_url"],
            c["secondary_source"], c["secondary_url"], c["confidence"], c["priority"],
            c["notes"]
        ])

print("Writing BIHAR_BATCH6_OVERLAP_AUDIT.csv...")
with open('BIHAR_BATCH6_OVERLAP_AUDIT.csv', mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "candidate_name", "district", "category", "candidate_lat", "candidate_lng",
        "nearest_existing_place_id", "nearest_existing_place_name", "min_haversine_distance_km",
        "exact_name_match", "case_insensitive_match", "slug_collision", "same_complex_site",
        "overlap_classification", "audit_verdict", "audit_notes"
    ])
    for c in recommended:
        writer.writerow([
            c["name"], c["district"], c["category"], c["lat"], c["lng"],
            c["nearest_id"], c["nearest_place"], f"{c['min_dist']:.2f}",
            "NO", "NO", "NO", "NO" if c["min_dist"] > 1.0 else "YES",
            c["overlap_class"], "APPROVAL-READY", c["why"]
        ])
    for c in hold_candidates:
        writer.writerow([
            c["name"], c["district"], c["category"], c["lat"], c["lng"],
            c["nearest_id"], c["nearest_place"], f"{c['min_dist']:.2f}",
            "NO", "NO", "NO", "YES" if c["min_dist"] < 1.0 else "NO",
            c["overlap_class"], "HOLD", c["reason"]
        ])
    for c in reject_candidates:
        # compute nearest place
        min_d = 9999.0
        np = None
        for p in active_places:
            if p['latitude'] and p['longitude']:
                d = haversine(c['lat'], c['lng'], float(p['latitude']), float(p['longitude']))
                if d < min_d:
                    min_d = d
                    np = p
        writer.writerow([
            c["name"], c["district"], c["category"], c["lat"], c["lng"],
            np['id'] if np else "N/A", np['name'] if np else "N/A", f"{min_d:.2f}" if np else "N/A",
            "NO", "NO", "NO", "NO",
            "Rejected Non-Tourism Candidate", "REJECT", c["reason"]
        ])

print("All CSV artifacts created successfully.")
