import sys
import math
sys.path.insert(0, '.')
from models.connection import get_db

sys.stdout.reconfigure(encoding='utf-8')

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon1 - lon2)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

conn = get_db()
cur = conn.cursor()
cur.execute("""
    SELECT p.id, p.name, p.slug, p.category, d.id AS district_id, d.name AS district_name, p.latitude, p.longitude
    FROM places p
    JOIN districts d ON d.id = p.district_id
    WHERE p.deleted_at IS NULL
""")
active_places = cur.fetchall()

test_candidates = [
    ('Ara House', 'Bhojpur', 16, 'historical', 25.5539, 84.6680),
    ('Sun Temple, Tarari', 'Bhojpur', 16, 'historical', 25.2650, 84.4530),
    ('Chandradhari Museum', 'Darbhanga', 18, 'historical', 26.1550, 85.8980),
    ('Ahilya Sthan, Ahiyari', 'Darbhanga', 18, 'cultural', 26.2917, 85.8015),
    ('Baba Garibnath Temple', 'Muzaffarpur', 7, 'temple', 26.1205, 85.3912),
    ('Kandaha Sun Temple', 'Saharsa', 29, 'historical', 25.8820, 86.4670),
    ('Mata Puran Devi Temple', 'Purnia', 28, 'cultural', 25.7725, 87.4580),
    ('Baba Brahmeshwar Nath Temple, Brahmpur', 'Buxar', 17, 'temple', 25.5992, 84.2882),
    ('Gunawa Ji (Jain Tirth)', 'Nawada', 38, 'cultural', 24.8944, 85.5312),
    ('Ambika Sthan, Aami', 'Saran', 31, 'cultural', 25.6881, 85.0062),
    ('Lakri Dargah', 'Gopalganj', 19, 'cultural', 26.3150, 84.4720),
    ('Baba Tileshwar Nath Mandir, Sukhpur', 'Supaul', 36, 'temple', 26.0620, 86.6080),
    ('Khudneshwar Asthan', 'Samastipur', 30, 'cultural', 25.7610, 85.6890),
    ('Lali Pahadi Archaeological Site', 'Lakhisarai', 26, 'historical', 25.1764, 85.9981),
    ('Manihari Ganga Ghat', 'Katihar', 23, 'cultural', 25.3370, 87.6250),
]

print(f"{'Candidate':<38} | {'District':<12} | {'Nearest Place':<35} | {'Min Dist (km)':<14}")
print("-" * 105)
for name, dist, did, cat, lat, lng in test_candidates:
    nearest = None
    min_d = 99999.0
    for ap in active_places:
        d = haversine_km(lat, lng, ap['latitude'], ap['longitude'])
        if d < min_d:
            min_d = d
            nearest = ap
    print(f"{name:<38} | {dist:<12} | {nearest['name'][:34]:<35} | {min_d:6.2f} km")
