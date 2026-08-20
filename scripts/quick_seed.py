import os
import pymysql

c = pymysql.connect(host=os.environ.get('DB_HOST', '127.0.0.1'),
                    port=int(os.environ.get('DB_PORT', '3307')),
                    user=os.environ.get('DB_USER', 'root'),
                    password=os.environ.get('DB_PASSWORD', ''),
                    database=os.environ.get('DB_NAME', 'hiddenyatra'),
                    charset='utf8mb4')
cur = c.cursor()

# State
cur.execute("INSERT IGNORE INTO states (name, slug, description) VALUES ('Bihar', 'bihar', 'Land of ancient wisdom')")
c.commit()
cur.execute("SELECT id FROM states WHERE slug='bihar'")
state_id = cur.fetchone()[0]

# Districts
districts = [
    ('Jamui', 'jamui', 'Known for Jain temples and waterfalls'),
    ('Nalanda', 'nalanda', 'Home of ancient Nalanda University'),
    ('Gaya', 'gaya', 'Sacred city with Bodh Gaya'),
    ('Rajgir', 'rajgir', 'Ancient capital of Magadh'),
    ('Patna', 'patna', 'Capital city of Bihar'),
    ('Munger', 'munger', 'Fort city on the Ganges'),
    ('Bhagalpur', 'bhagalpur', 'Silk city of Bihar'),
]
for name, slug, desc in districts:
    cur.execute(
        'INSERT IGNORE INTO districts (state_id, name, slug, description, is_featured, is_visible) '
        'VALUES (%s,%s,%s,%s,1,1)', (state_id, name, slug, desc))
c.commit()

# Get district IDs
cur.execute('SELECT id, slug FROM districts')
dist_map = {row[1]: row[0] for row in cur.fetchall()}
print(f"Districts: {dist_map}")

# Places (columns: name, slug, state_id, district_id, category, description, latitude, longitude, is_featured, entry_fee, view_count)
places = [
    ('Kali Mandir Jamui', 'kali-mandir-jamui', 'jamui', 'temple',
     'Ancient Kali temple in the heart of Jamui', 24.9264, 86.2263, 1),
    ('Simultala Waterfall', 'simultala-waterfall', 'jamui', 'waterfall',
     'Beautiful waterfall near Simultala hill station', 24.6389, 86.4222, 1),
    ('Giddheswar Temple', 'giddheswar-temple', 'jamui', 'temple',
     'Famous Shiva temple on a hilltop in Jamui', 24.8500, 86.1500, 1),
    ('Patneshwar Temple', 'patneshwar-temple', 'jamui', 'temple',
     'Ancient Shiva temple in Jamui district', 24.9100, 86.2100, 1),
    ('Nalanda University Ruins', 'nalanda-university-ruins', 'nalanda', 'historical',
     'UNESCO World Heritage Site - ancient Buddhist learning center', 25.1362, 85.4433, 1),
    ('Bodh Gaya Temple', 'bodh-gaya-temple', 'gaya', 'temple',
     'Where Lord Buddha attained enlightenment', 24.6961, 84.9911, 1),
    ('Mahabodhi Temple', 'mahabodhi-temple', 'gaya', 'temple',
     'UNESCO World Heritage Buddhist temple in Bodh Gaya', 24.6952, 84.9913, 1),
    ('Rajgir Hot Springs', 'rajgir-hot-springs', 'rajgir', 'nature',
     'Natural hot water springs at Brahmakund', 25.0275, 85.4200, 1),
    ('Griddhakuta Peak', 'griddhakuta-peak', 'rajgir', 'hill',
     'Vulture Peak - Buddhist pilgrimage site', 25.0250, 85.4150, 1),
    ('Patna Sahib Gurudwara', 'patna-sahib-gurudwara', 'patna', 'temple',
     'Birthplace of Guru Gobind Singh Ji', 25.6100, 85.1400, 1),
    ('Golghar Patna', 'golghar-patna', 'patna', 'historical',
     'Iconic beehive-shaped granary built in 1786', 25.6120, 85.1370, 1),
    ('Vikramshila Ruins', 'vikramshila-ruins', 'bhagalpur', 'historical',
     'Ancient Buddhist university ruins', 25.3200, 87.2800, 1),
    ('Munger Fort', 'munger-fort', 'munger', 'historical',
     'Historic fort overlooking the Ganges river', 25.3750, 86.4720, 1),
    ('Kakolat Waterfall', 'kakolat-waterfall', 'nalanda', 'waterfall',
     'Famous 50-meter waterfall in Nalanda district', 25.0500, 85.5200, 1),
    ('Naulakha Palace Rajgir', 'naulakha-palace', 'rajgir', 'historical',
     'Beautiful Jain temple complex near Rajgir', 25.0300, 85.4250, 0),
]

for name, slug, dist_slug, cat, desc, lat, lng, feat in places:
    did = dist_map.get(dist_slug, 1)
    cur.execute(
        'INSERT IGNORE INTO places (name, slug, state_id, district_id, category, description, '
        'latitude, longitude, is_featured, entry_fee, view_count) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (name, slug, state_id, did, cat, desc, lat, lng, feat, 'Free', 150))

c.commit()

cur.execute('SELECT COUNT(*) FROM places')
print(f"Seeded {cur.fetchone()[0]} places")
cur.execute('SELECT COUNT(*) FROM districts')
print(f"Seeded {cur.fetchone()[0]} districts")
c.close()
print("Done! Restart Flask to rebuild search index.")
