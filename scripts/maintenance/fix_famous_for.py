"""
Clean up famous_for text on all districts and fix place IDs 2-6 name/slug alignment.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
from models.connection import get_db

conn = get_db()
cur = conn.cursor()

FAMOUS_FOR_MAP = {
    1:  'Golghar, Patna Sahib, Bihar Museum, Litti Chokha',
    2:  'Mahabodhi Temple, Bodh Gaya, Vishnupad Temple, Tilkut',
    3:  'Nalanda University Ruins, Rajgir, Silao Khaja',
    4:  'Simultala Hill Station, Nagi Dam, Gidhaur Palace, Jain Heritage',
    5:  'Vikramshila University Ruins, Silk City, Katarni Chawal',
    6:  'Munger Fort, Bhimbandh Hot Springs, Yoga University',
    7:  'Shahi Litchi, Lychee Kingdom, Jubba Sahni Park',
    8:  'Sher Shah Suri Tomb, Rohtasgarh Fort, Sasaram',
    9:  'Valmiki National Park, Tiger Reserve, Gandhi Heritage',
    10: 'Kesariya Stupa, World Largest Buddhist Stupa',
    11: 'Raniganj Vrikshavatika, Indo-Nepal Border Trade',
    12: 'Son River, Madhusudan Temple, Quiet Countryside',
    13: 'Deo Sun Temple, Umga Hills, Ancient Solar Shrine',
    14: 'Mandar Hill, Chhath Sanctuary, Ancient Mythology',
    15: 'Kanwar Lake Bird Sanctuary (Ramsar Site), Simaria Ghat',
    16: 'Veer Kunwar Singh Fort, Jagdishpur, Historic Arrah',
    17: 'Battle of Buxar Memorial, Chausa, Ramrekha Ghat',
    18: 'Darbhanga Raj Palace, Ahilya Sthan, Mithila Culture',
    19: 'Thawe Mandir, Dighwa Dubauli',
    20: 'Mithila Painting, Jitwarpur Art Village, Makhana',
    21: 'Barabar Caves, Nagarjuni Caves, Ancient Ashokan Inscriptions',
    22: 'Mundeshwari Temple, Karkat Waterfall, Telhar Kund, Rohtas Border',
    23: 'Gogabeel Lake Bird Sanctuary, Confluence of Ganga & Koshi',
    24: 'Katyayani Mandir, Confluence of Seven Rivers',
    25: 'Lush Tea Gardens, Kishanganj Fort, Indo-Nepal Border',
    26: 'Ashok Dham Temple, Indradaman Hill Buddhist Monasteries',
    27: 'Singheshwar Sthan, Shiva Pilgrimage, Koshi Basin',
    28: 'Puran Devi Temple, Jalgarh Fort, Historic Purnia',
    29: 'Matsyagandha Mandir, Tara Sthan Mahishi, Koshi Plains',
    30: 'Samastipur Railway Division, Vidyapatinagar, Agricultural University',
    31: 'Sonepur Cattle Fair, Ambika Bhawani Temple, Doriganj',
    32: 'Aroll Shiva Temple, Sheikhpura Hills, Ancient Stupas',
    33: 'Deokuli Shiva Temple, Bagmati River Basin',
    34: 'Janaki Sthan Temple, Punaura Dham, Sacred Birthplace of Sita',
    35: 'Birthplace of Dr. Rajendra Prasad (Ziradei), Don Fort',
    36: 'Koshi Barrage, Bird Watcher Wetlands, Eco Tourism',
    37: 'Birthplace of Democracy (Licchavi), Ashoka Pillar, Buddha Relic Stupa',
    38: 'Kakolat Waterfall, Natural Cascade & Scenic Hills',
}

# Update famous_for on districts
for did, text in FAMOUS_FOR_MAP.items():
    cur.execute("UPDATE districts SET famous_for = %s WHERE id = %s", (text, did))
print(f"✅ Updated famous_for across {len(FAMOUS_FOR_MAP)} districts")

# Align places 2-6 name and slug to match their actual identities
cur.execute("""
    UPDATE places SET 
        name = 'Takht Sri Patna Sahib',
        slug = 'patna-sahib-gurudwara-takht-sri-patna-sahib',
        district_id = 1,
        category = 'religious',
        description = 'One of the five Takhts of Sikhism, birthplace of Tenth Sikh Guru, Guru Gobind Singh Ji.'
    WHERE id = 2
""")

cur.execute("""
    UPDATE places SET 
        name = 'Patna Museum',
        slug = 'patna-museum',
        district_id = 1,
        category = 'museum',
        description = 'State museum of Bihar housing over 50,000 rare antiquities including the famous Didarganj Yakshi.'
    WHERE id = 3
""")

cur.execute("""
    UPDATE places SET 
        name = 'Gandhi Maidan Patna',
        slug = 'gandhi-maidan-patna',
        district_id = 1,
        category = 'historical',
        description = 'Historic 62-acre open park in the heart of Patna, world tallest bronze statue of Mahatma Gandhi.'
    WHERE id = 4
""")

cur.execute("""
    UPDATE places SET 
        name = 'Barabar Caves',
        slug = 'barabar-caves-gaya',
        district_id = 2,
        category = 'historical'
    WHERE id = 5
""")

cur.execute("""
    UPDATE places SET 
        name = 'Vishnupad Temple Gaya',
        slug = 'vishnupad-temple-gaya',
        district_id = 2,
        category = 'religious',
        description = 'Ancient temple dedicated to Lord Vishnu featuring the footprint of Vishnu inscribed in solid rock.'
    WHERE id = 6
""")

# Re-link place 4 (Simultala) from earlier if duplicate existed
# Note: Simultala Hill Station (ID 59) is the main Jamui place at district_id = 4.

conn.commit()
print("✅ Places 2-6 synchronized with authentic names, slugs, and district IDs!")

cur.close()
conn.close()
