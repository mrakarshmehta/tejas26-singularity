import sys, csv, os, math
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

with get_cursor() as cur:
    cur.execute("SELECT id, name, slug, category, latitude, longitude, district_id FROM places WHERE deleted_at IS NULL")
    active_places = cur.fetchall()

    cur.execute("SELECT id, name FROM districts")
    dist_map = {d['id']: d['name'] for d in cur.fetchall()}

dist_place_counts = {}
for p in active_places:
    dname = dist_map.get(p['district_id'], 'Unknown')
    dist_place_counts[dname] = dist_place_counts.get(dname, 0) + 1

# List of top shortlisted candidate options for Batch 5
shortlisted_candidates = [
    {
        "name": "Umga Sun Temple & Rock Complex",
        "district": "Aurangabad",
        "category": "historical",
        "latitude": 24.6312,
        "longitude": 84.5518,
        "type": "ancient stone temple & rock-cut architecture",
        "primary_source": "District Administration Aurangabad (aurangabad.nic.in)",
        "secondary_source": "Archaeological Survey of India & Bihar Tourism",
        "claim": "15th-century granite temple atop Umga hill built without mortar by King Bhairavendra with 52 rock shrines",
        "significance": "Megalithic hill temple architecture, ancient inscriptions"
    },
    {
        "name": "Bhitiharwa Gandhi Ashram",
        "district": "West Champaran",
        "category": "historical",
        "latitude": 27.2154,
        "longitude": 84.4512,
        "type": "freedom heritage & Gandhian memorial",
        "primary_source": "District Administration West Champaran (westchamparan.nic.in)",
        "secondary_source": "Gandhi Heritage Portal & Bihar Tourism",
        "claim": "Historic ashram established by Mahatma Gandhi on 20 Nov 1917 during Champaran Satyagraha",
        "significance": "Pivotal freedom struggle site, museum, Kasturba school"
    },
    {
        "name": "Ashokan Pillar & Ananda Stupa, Kolhua",
        "district": "Vaishali",
        "category": "historical",
        "latitude": 26.0125,
        "longitude": 85.1124,
        "type": "Mauryan archaeology & Buddhist stupa",
        "primary_source": "Archaeological Survey of India (ASI Patna Circle)",
        "secondary_source": "UNESCO Tentative List Dossier (Silk Road Sites)",
        "claim": "Centrally Protected ASI monument featuring complete polished Ashokan pillar with lion capital and Ananda Stupa",
        "significance": "Supreme archaeological monument, Second Buddhist Council landscape"
    },
    {
        "name": "Udaipur Wildlife Sanctuary",
        "district": "West Champaran",
        "category": "nature",
        "latitude": 26.8512,
        "longitude": 84.4812,
        "type": "wetland & oxbow lake wildlife sanctuary",
        "primary_source": "Dept of Environment, Forest & Climate Change (Govt of Bihar)",
        "secondary_source": "ENVIS Centre Bihar & District Administration West Champaran",
        "claim": "Statutory Wildlife Sanctuary established 1978 spanning 8.74 sq km around Sarayaman oxbow lake",
        "significance": "Migratory waterfowl, wetland conservation, boating eco-tourism"
    },
    {
        "name": "Chandan Dam",
        "district": "Banka",
        "category": "lake",
        "latitude": 24.7812,
        "longitude": 86.8125,
        "type": "reservoir & hill eco-tourism",
        "primary_source": "District Administration Banka (banka.nic.in)",
        "secondary_source": "Water Resources Dept & Bihar Tourism",
        "claim": "One of eastern Bihar's largest multi-embankment reservoirs across Chandan river with hill boating",
        "significance": "Expands Banka beyond Mandar Hill, major scenic lake"
    },
    {
        "name": "Punaura Dham",
        "district": "Sitamarhi",
        "category": "cultural",
        "latitude": 26.6125,
        "longitude": 85.4512,
        "type": "major pilgrimage & sacred site",
        "primary_source": "Ministry of Tourism (Govt of India - PRASHAD Scheme)",
        "secondary_source": "District Administration Sitamarhi (sitamarhi.nic.in)",
        "claim": "Officially designated birthplace of Mata Sita under PRASHAD Scheme and Ramayana Circuit",
        "significance": "High-priority national pilgrimage, sacred pond, major shrine"
    },
    {
        "name": "Champanagar Ancient Capital & Jain Tirth",
        "district": "Bhagalpur",
        "category": "cultural",
        "latitude": 25.2312,
        "longitude": 86.9245,
        "type": "epic ancient capital & Jain supreme pilgrimage",
        "primary_source": "Archaeological Survey of India & Bihar Tourism",
        "secondary_source": "District Administration Bhagalpur (bhagalpur.nic.in)",
        "claim": "Ancient capital of Anga Kingdom (Mahabharata King Karna) and Panch Kalyanak Bhoomi of 12th Tirthankara Vasupujya",
        "significance": "Karanagarh ramparts, Jain tirth, Manasa Devi folklore"
    },
    {
        "name": "Baraila Lake / Salim Ali Jubba Sahni Sanctuary",
        "district": "Vaishali",
        "category": "nature",
        "latitude": 25.7512,
        "longitude": 85.4512,
        "type": "statutory bird sanctuary & wetland",
        "primary_source": "Dept of Environment, Forest & Climate Change (Govt of Bihar)",
        "secondary_source": "Wildlife Protection Act 1972 notification (1997)",
        "claim": "Statutory Wildlife Sanctuary established 1997 spanning 196 hectares perennial wetland",
        "significance": "Important bird area, massive migratory avian biodiversity"
    },
    {
        "name": "George Orwell Birthplace & Memorial",
        "district": "East Champaran",
        "category": "historical",
        "latitude": 26.6452,
        "longitude": 84.9085,
        "type": "global literary heritage",
        "primary_source": "Department of Art, Culture & Youth (Govt of Bihar)",
        "secondary_source": "District Administration East Champaran (eastchamparan.nic.in)",
        "claim": "Authentic 1903 colonial bungalow birthplace of author George Orwell (Eric Arthur Blair), protected state monument",
        "significance": "International literary tourist attraction, Orwell museum"
    },
    {
        "name": "Kharagpur Lake (Haveli Kharagpur)",
        "district": "Munger",
        "category": "lake",
        "latitude": 25.1215,
        "longitude": 86.5124,
        "type": "historic lake & hill gorge eco-tourism",
        "primary_source": "District Administration Munger (munger.nic.in)",
        "secondary_source": "Forest Department Bihar & Bihar Tourism",
        "claim": "Historic scenic lake built in 1876 by Darbhanga Raj across Man river gorge amidst Kharagpur hills",
        "significance": "Forest hills, waterfall gorge, boating reservoir"
    },
    {
        "name": "Sarvodaya Ashram, Shekhodeora",
        "district": "Nawada",
        "category": "cultural",
        "latitude": 24.8125,
        "longitude": 85.8412,
        "type": "national freedom heritage & rural ashram",
        "primary_source": "District Administration Nawada (nawada.nic.in)",
        "secondary_source": "Sarvodaya Trust Archives & Bihar Tourism",
        "claim": "Established in 1952 by Loknayak Jayaprakash Narayan (JP) as freedom struggle & rural reconstruction hub",
        "significance": "Nawada currently has only 1 place (Kakolat); historic JP heritage"
    },
    {
        "name": "Sujani Embroidery Craft Cluster",
        "district": "Muzaffarpur",
        "category": "cultural",
        "latitude": 26.1512,
        "longitude": 85.4812,
        "type": "GI-tagged traditional artisan craft cluster",
        "primary_source": "Geographical Indications Registry (Govt of India)",
        "secondary_source": "UNESCO / Development Commissioner (Handicrafts)",
        "claim": "UNESCO Seal of Excellence & GI-tagged heritage needlework craft cluster preserved in Bhusura village",
        "significance": "Adds underrepresented artisan craft village destination; Muzaffarpur currently has only 1 place"
    }
]

print("=== CANDIDATE SPATIAL & DIVERSITY ANALYSIS ===")
for c in shortlisted_candidates:
    lat, lng = c['latitude'], c['longitude']
    min_dist = 9999.0
    nearest_p = None
    for ap in active_places:
        alat = float(ap['latitude'] or 0)
        alng = float(ap['longitude'] or 0)
        d = haversine(lat, lng, alat, alng)
        if d < min_dist:
            min_dist = d
            nearest_p = ap['name']
    c['min_dist'] = min_dist
    c['nearest_p'] = nearest_p
    c['curr_district_places'] = dist_place_counts.get(c['district'], 0)
    print(f"[{c['district']:15} (Current: {c['curr_district_places']})] {c['name']:42} | Cat: {c['category']:10} | MinDist: {c['min_dist']:5.1f}km ({c['nearest_p']})")
