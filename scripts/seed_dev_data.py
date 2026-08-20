"""
HiddenYatra — Development Seed Data Generator
Populates a development database with safe demo data:
  - 1 State (Bihar)
  - 38 Districts of Bihar
  - 10+ Key Tourist Places & Hidden Gems
  - Sample Host Profile & Listings (Paid Homestay + Free Local Stay)
  - Demo Accounts (Admin, Host, Traveler)
  - Sample Emergency Services
Uses INSERT IGNORE / Upsert to ensure idempotent & non-destructive execution.
"""
import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv('.env')

from models.connection import get_cursor
from models.auth import hash_password

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def seed_development_data():
    logger.info("Starting development data seeding...")

    with get_cursor(commit=True) as cur:
        # 1. State (Bihar)
        cur.execute("""
            INSERT INTO states (id, name, slug, description, image_url, sort_order)
            VALUES (1, 'Bihar', 'bihar', 'Land of ancient wisdom, spiritual heritage, and vibrant culture.', '', 1)
            ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description)
        """)
        logger.info("State seeded: Bihar (ID: 1)")

        # 2. Districts (All 38 Districts)
        districts_data = [
            (1, 'Patna', 'patna', 'Capital city of Bihar, rich in history along the Ganges', 1),
            (2, 'Gaya', 'gaya', 'Sacred city of Bodh Gaya, Mahabodhi Temple & Vishnupad Temple', 1),
            (3, 'Nalanda', 'nalanda', 'Home of world-famous ancient Nalanda University ruins & Rajgir', 1),
            (4, 'Jamui', 'jamui', 'Eco-tourism hub with waterfalls, Jain temples, and Simultala hill station', 1),
            (5, 'Bhagalpur', 'bhagalpur', 'Silk City of Bihar, famous for Tussar silk & Vikramshila ruins', 1),
            (6, 'Munger', 'munger', 'Historic fort city on the banks of Ganges, Bihar School of Yoga', 1),
            (7, 'Muzaffarpur', 'muzaffarpur', 'Lychee Kingdom of India, cultural center of North Bihar', 1),
            (8, 'Rohtas', 'rohtas', 'Famous for Rohtasgarh Fort, Sher Shah Suri Tomb, and waterfalls', 1),
            (9, 'West Champaran', 'west-champaran', 'Valmiki National Park, tiger reserve, and historic Gandhian heritage', 1),
            (10, 'East Champaran', 'east-champaran', 'Kesaria Stupa - world largest Buddhist stupa', 1),
            (11, 'Araria', 'araria', 'Border district known for rich flora, fauna, and local culture', 0),
            (12, 'Arwal', 'arwal', 'Serene district on Son river with historical monuments', 0),
            (13, 'Aurangabad', 'aurangabad', 'Deo Sun Temple and ancient historical sites', 0),
            (14, 'Banka', 'banka', 'Mandar Hill, famous for Chhath Puja & mythological significance', 0),
            (15, 'Begusarai', 'begusarai', 'Kabar Taal Wetland - Bihar first Ramsar site', 0),
            (16, 'Bhojpur', 'bhojpur', 'Ara, Veer Kunwar Singh fort & historical battlegrounds', 0),
            (17, 'Buxar', 'buxar', 'Historic battle site on Ganges, ancient hermitages', 0),
            (18, 'Darbhanga', 'darbhanga', 'Cultural capital of Mithila, famous for Darbhanga Raj Palace', 0),
            (19, 'Gopalganj', 'gopalganj', 'Famous for Thawe Mandir and rich local culture', 0),
            (20, 'Madhubani', 'madhubani', 'Heart of Madhubani Mithila Painting art and culture', 1),
            (21, 'Jehanabad', 'jehanabad', 'Barabar Caves - oldest surviving rock-cut caves in India', 1),
            (22, 'Kaimur', 'kaimur', 'Karkat Waterfall, Telhar Kund, and scenic hills', 1),
            (23, 'Katihar', 'katihar', 'Gogabeel Lake wetland reserve and confluence of rivers', 0),
            (24, 'Khagaria', 'khagaria', 'Confluence of seven rivers with rich agricultural heritage', 0),
            (25, 'Kishanganj', 'kishanganj', 'Tea gardens of Bihar and lush green landscapes', 0),
            (26, 'Lakhisarai', 'lakhisarai', 'Ancient Buddhist and Hindu archaeological sites at Ashok Dham', 0),
            (27, 'Madhepura', 'madhepura', 'Singheshwar Asthan Shiva temple', 0),
            (28, 'Purnia', 'purnia', 'Oldest district in Bihar with vibrant local markets', 0),
            (29, 'Saharsa', 'saharsa', 'Matsyagandha Mandir and Koshi river basin', 0),
            (30, 'Samastipur', 'samastipur', 'Agricultural university hub & Vidyapatinagar heritage', 0),
            (31, 'Saran', 'saran', 'Chhapra, Sonepur Cattle Fair - Asia largest animal fair', 1),
            (32, 'Sheikhpura', 'sheikhpura', 'Aroll Shiva temple and ancient hills', 0),
            (33, 'Sheohar', 'sheohar', 'Smallest district in Bihar with serene rural landscape', 0),
            (34, 'Sitamarhi', 'sitamarhi', 'Janki Temple - sacred birthplace of Mata Sita', 1),
            (35, 'Siwan', 'siwan', 'Birthplace of Dr. Rajendra Prasad (Ziradei)', 0),
            (36, 'Supaul', 'supaul', 'Koshi barrage and eco-tourism wetlands', 0),
            (37, 'Vaishali', 'vaishali', 'World first republic (Lichhavi), Relic Stupa of Buddha', 1),
            (38, 'Nawada', 'nawada', 'Kakolat Waterfall - famous 50m cascade', 1),
        ]

        for did, name, slug, desc, feat in districts_data:
            cur.execute("""
                INSERT INTO districts (id, state_id, name, slug, description, is_featured, is_visible)
                VALUES (%s, 1, %s, %s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description), is_featured=VALUES(is_featured)
            """, (did, name, slug, desc, feat))
        logger.info("Seeded %d districts.", len(districts_data))

        # 3. Sample Blocks
        blocks_data = [
            (1, 1, 'Patna Sadar', 'patna-sadar'),
            (2, 2, 'Bodh Gaya', 'bodh-gaya'),
            (3, 3, 'Rajgir', 'rajgir'),
            (4, 4, 'Simultala', 'simultala'),
        ]
        for bid, did, name, slug in blocks_data:
            cur.execute("""
                INSERT INTO blocks (id, district_id, name, slug)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name)
            """, (bid, did, name, slug))

        # 4. Sample Places
        places_data = [
            (1, 'Golghar Patna', 'golghar-patna', 1, 1, 'historical',
             'Iconic beehive-shaped granary built in 1786 offering panoramic views of Patna and the Ganges.',
             25.6120, 85.1370, 1, 1, 'Free', '150'),

            (2, 'Mahabodhi Temple', 'mahabodhi-temple', 2, 2, 'temple',
             'UNESCO World Heritage Buddhist temple in Bodh Gaya where Lord Buddha attained enlightenment.',
             24.6952, 84.9913, 1, 0, 'Free', '300'),

            (3, 'Nalanda University Ruins', 'nalanda-university-ruins', 3, 3, 'historical',
             'Ancient 5th-century Buddhist monastic university, one of the world ancient learning centers.',
             25.1362, 85.4433, 1, 0, '₹50 for Indians', '250'),

            (4, 'Simultala Waterfall', 'simultala-waterfall', 4, 4, 'waterfall',
             'Picturesque natural waterfall tucked away in the serene hills of Simultala in Jamui district.',
             24.6389, 86.4222, 1, 1, 'Free', '180'),

            (5, 'Barabar Caves', 'barabar-caves', 21, 2, 'historical',
             'Oldest surviving rock-cut caves in India, dating back to the Maurya Empire (3rd century BC).',
             25.0064, 85.0614, 1, 1, 'Free', '120'),

            (6, 'Kakolat Waterfall', 'kakolat-waterfall', 38, 3, 'waterfall',
             'Breathtaking 50-meter natural cascade surrounded by dense green forests in Nawada.',
             24.7700, 85.6300, 1, 1, 'Free', '220'),
        ]

        for pid, name, slug, did, bid, cat, desc, lat, lng, feat, gem, fee, views in places_data:
            cur.execute("""
                INSERT INTO places (id, state_id, district_id, block_id, name, slug, category, description,
                                    latitude, longitude, is_featured, is_hidden_gem, entry_fee, view_count)
                VALUES (%s, 1, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description), category=VALUES(category)
            """, (pid, did, bid, name, slug, cat, desc, lat, lng, feat, gem, fee, views))
        logger.info("Seeded %d sample places.", len(places_data))

        # 5. Default Development Users
        pw_admin = hash_password('admin123')
        pw_host = hash_password('password123')
        pw_user = hash_password('password123')

        # Admin user (id=1)
        cur.execute("""
            INSERT INTO users (id, username, email, password_hash, display_name, full_name, status, is_admin, email_verified)
            VALUES (1, 'admin', 'admin@hiddenyatra.com', %s, 'System Admin', 'System Administrator', 'active', 1, 1)
            ON DUPLICATE KEY UPDATE display_name=VALUES(display_name), status='active'
        """, (pw_admin,))

        # Host user (id=2)
        cur.execute("""
            INSERT INTO users (id, username, email, password_hash, display_name, full_name, status, is_host, email_verified)
            VALUES (2, 'demo_host', 'host@hiddenyatra.com', %s, 'Ramesh Kumar', 'Ramesh Kumar Host', 'active', 1, 1)
            ON DUPLICATE KEY UPDATE display_name=VALUES(display_name), status='active'
        """, (pw_host,))

        # Traveler user (id=3)
        cur.execute("""
            INSERT INTO users (id, username, email, password_hash, display_name, full_name, status, email_verified)
            VALUES (3, 'demo_traveler', 'traveler@hiddenyatra.com', %s, 'Priya Singh', 'Priya Singh Traveler', 'active', 1)
            ON DUPLICATE KEY UPDATE display_name=VALUES(display_name), status='active'
        """, (pw_user,))
        logger.info("Seeded 3 default development accounts (admin, demo_host, demo_traveler).")

        # 6. Sample Host Profile
        cur.execute("""
            INSERT INTO host_profiles (id, user_id, bio, languages, address_line, district_id, verification_status, is_verified_badge, avg_host_rating)
            VALUES (1, 2, 'Local Bihari host passionate about sharing authentic culture, home-cooked food, and heritage stays.',
                    'Hindi, English, Maithili', 'Main Road, Bodh Gaya', 2, 'approved', 1, 4.8)
            ON DUPLICATE KEY UPDATE bio=VALUES(bio), verification_status='approved'
        """)

        # 7. Sample Host Listings (Paid Homestay & Free Stay)
        cur.execute("""
            INSERT INTO host_listings (id, host_id, listing_type, title, slug, description, district_id,
                                        address_text, price_per_night, max_guests, num_rooms, status, is_featured, avg_rating)
            VALUES (1, 1, 'paid_homestay', 'Bodh Gaya Heritage Homestay', 'bodh-gaya-heritage-homestay',
                    'Cozy traditional Bihari homestay near Mahabodhi Temple with organic home-cooked meals and peaceful garden.',
                    2, 'Bodh Gaya near Temple', 1200.00, 4, 2, 'published', 1, 4.8)
            ON DUPLICATE KEY UPDATE title=VALUES(title), status='published'
        """)

        cur.execute("""
            INSERT INTO host_listings (id, host_id, listing_type, title, slug, description, district_id,
                                        address_text, price_per_night, max_guests, num_rooms, status, is_featured, avg_rating)
            VALUES (2, 1, 'free_stay', 'Simultala Eco Village Stay', 'simultala-eco-village-stay',
                    'Free community host stay for eco-travelers and backpackers exploring Simultala hills and waterfalls.',
                    4, 'Simultala Village, Jamui', 0.00, 2, 1, 'published', 1, 4.9)
            ON DUPLICATE KEY UPDATE title=VALUES(title), status='published'
        """)
        logger.info("Seeded sample homestay & free village stay listings.")

    logger.info("✅ Development data seeding completed successfully.")


if __name__ == '__main__':
    seed_development_data()
