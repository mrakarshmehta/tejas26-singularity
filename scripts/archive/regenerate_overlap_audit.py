import sys
import math
import csv
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

conn = get_db()
cur = conn.cursor()

# Get all 138 active places
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
    ORDER BY p.id
""")
active_places = cur.fetchall()

candidates_audit = [
    # Top 10 Approval Ready
    {"name": "Ara House", "district": "Bhojpur", "category": "historical", "lat": 25.5539, "lng": 84.6680, "note": "Scrutinized: distinct 1857 military monument on college campus vs ancient market temple; approved with special scrutiny."},
    {"name": "Ahilya Sthan, Ahiyari", "district": "Darbhanga", "category": "cultural", "lat": 26.2917, "lng": 85.8015, "note": "Clear geographic separation from all active inventory; authentic Ramayana circuit anchor in Jale block."},
    {"name": "Baba Garibnath Temple", "district": "Muzaffarpur", "category": "temple", "lat": 26.1205, "lng": 85.3912, "note": "Scrutinized: 300-year-old major pilgrimage temple vs urban park; approved with special scrutiny."},
    {"name": "Surya Mandir, Kandaha", "district": "Saharsa", "category": "historical", "lat": 25.8820, "lng": 86.4670, "note": "Scrutinized: distinct village/panchayat archaeological Sun temple with 14th C inscription vs Tantric temple; approved with special scrutiny."},
    {"name": "Mata Puran Devi Temple", "district": "Purnia", "category": "cultural", "lat": 25.7725, "lng": 87.4580, "note": "Clear geographic separation from all active inventory; titular eponym heritage site of Purnia."},
    {"name": "Baba Brahmeshwar Nath Temple, Brahmpur", "district": "Buxar", "category": "temple", "lat": 25.5992, "lng": 84.2882, "note": "Clear geographic separation from all active inventory; ancient west-facing Shivalinga and cattle fair hub."},
    {"name": "Gunawa Ji (Jain Tirth)", "district": "Nawada", "category": "cultural", "lat": 24.8944, "lng": 85.5312, "note": "Clear geographic separation from all active inventory; sacred Jain Jal Mandir in Nawada."},
    {"name": "Ambika Sthan, Aami", "district": "Saran", "category": "cultural", "lat": 25.6881, "lng": 85.0062, "note": "Clear geographic separation from all active inventory; ancient Ganga-cliff Shaktipeeth mound at Dighwara."},
    {"name": "Lakri Dargah", "district": "Gopalganj", "category": "cultural", "lat": 26.3150, "lng": 84.4720, "note": "Clear geographic separation from all active inventory; 16th-century Sufi pilgrimage shrine endowed by Aurangzeb."},
    {"name": "Baba Tileshwar Nath Mandir, Sukhpur", "district": "Supaul", "category": "temple", "lat": 26.0620, "lng": 86.6080, "note": "Clear geographic separation from all active inventory; primary spiritual pilgrimage center of lower Kosi basin."},
    # Held Candidates Audited
    {"name": "Chandradhari Museum", "district": "Darbhanga", "category": "historical", "lat": 26.1550, "lng": 85.8980, "note": "Scrutinized: museum inside Darbhanga city, 0.87 km from Raj Palace; held for future batch to prioritize rural Ahilya Sthan."},
    {"name": "Khudneshwar Asthan", "district": "Samastipur", "category": "cultural", "lat": 25.7610, "lng": 85.6890, "note": "Clear geographic separation from all active inventory; held for Batch 9 to preserve 1-per-district balance."},
    {"name": "Lali Pahadi Archaeological Site", "district": "Lakhisarai", "category": "historical", "lat": 25.1764, "lng": 85.9981, "note": "Clear geographic separation from all active inventory; held for Batch 9 as Lakhisarai gained Shringirishi in Batch 6."},
    {"name": "Manihari Ganga Ghat", "district": "Katihar", "category": "cultural", "lat": 25.3370, "lng": 87.6250, "note": "Distinct sacred ghat/ashram; held for Batch 9 as Katihar gained Lakshmipur Gurdwara in Batch 6."},
    {"name": "Sun Temple, Tarari", "district": "Bhojpur", "category": "historical", "lat": 25.2650, "lng": 84.4530, "note": "Clear geographic separation; held in favor of 1857 flagship fortress Ara House for Bhojpur."},
    {"name": "Buddha Relic Stupa", "district": "Vaishali", "category": "historical", "lat": 25.9860, "lng": 85.1270, "note": "Severe proximity (0.14 km from Vaishali birthplace marker); held as subcomponent of Vaishali core complex."},
    {"name": "Nagi Dam Bird Sanctuary", "district": "Jamui", "category": "nature", "lat": 24.8150, "lng": 86.3750, "note": "Clear geographic separation; held to avoid Jamui district saturation (already 11 active places)."},
    {"name": "Kauwadol Hill & Colossal Buddha", "district": "Gaya", "category": "historical", "lat": 24.9920, "lng": 85.0480, "note": "Nearby to Barabar Caves; held to avoid Gaya district saturation (already 12 active places)."},
    {"name": "Chankigarh Fort", "district": "West Champaran", "category": "historical", "lat": 27.0520, "lng": 84.4750, "note": "Clear geographic separation; held to avoid Champaran saturation (already 6 active places)."},
    {"name": "Tomb of Bakhtiyar Khan", "district": "Kaimur", "category": "historical", "lat": 25.0430, "lng": 83.5180, "note": "Nearby Karkatgarh; held to avoid Kaimur saturation (already 4 active places)."}
]

rows = []
for c in candidates_audit:
    min_d = 99999.0
    nearest_p = None
    for ap in active_places:
        d = haversine_km(c['lat'], c['lng'], ap['latitude'], ap['longitude'])
        if d < min_d:
            min_d = d
            nearest_p = ap
            
    if min_d < 1.0:
        cls = "SAME SITE / SEVERE OVERLAP"
    elif min_d < 5.0:
        cls = "NEARBY BUT DISTINCT"
    else:
        cls = "DISTINCT DESTINATION"
        
    rows.append({
        'candidate_name': c['name'],
        'district': c['district'],
        'category': c['category'],
        'latitude': c['lat'],
        'longitude': c['lng'],
        'nearest_place_id': nearest_p['id'],
        'nearest_place_name': nearest_p['name'],
        'nearest_place_district': nearest_p['district_name'],
        'haversine_distance_km': round(min_d, 2),
        'overlap_classification': cls,
        'audit_resolution': c['note']
    })

fieldnames = [
    'candidate_name', 'district', 'category', 'latitude', 'longitude',
    'nearest_place_id', 'nearest_place_name', 'nearest_place_district',
    'haversine_distance_km', 'overlap_classification', 'audit_resolution'
]

with open('BIHAR_BATCH8_OVERLAP_AUDIT.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Regenerated BIHAR_BATCH8_OVERLAP_AUDIT.csv successfully.")
for r in rows[:10]:
    print(f"{r['candidate_name']:<35} | {r['nearest_place_name']:<35} | {r['haversine_distance_km']:>5.2f} km | {r['overlap_classification']}")
