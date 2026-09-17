import os
import sys
import json
import ssl
import urllib.request
from datetime import datetime
from PIL import Image

sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor
from werkzeug.security import generate_password_hash

IMG_DIR = r'd:\HiddenYatra\static\uploads\hosts\listings'
os.makedirs(IMG_DIR, exist_ok=True)

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def download_and_save_image(url, filename):
    dest_path = os.path.join(IMG_DIR, filename)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 5000:
        print(f"  [EXISTS] {filename}")
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=15) as resp:
            data = resp.read()
            with open(dest_path, 'wb') as f:
                f.write(data)
            # Re-compress cleanly with PIL
            with Image.open(dest_path) as im:
                im = im.convert('RGB')
                im.thumbnail((1200, 800), Image.Resampling.LANCZOS)
                im.save(dest_path, 'JPEG', quality=85)
            print(f"  [DOWNLOADED] {filename} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"  [ERROR] Downloading {filename}: {e}")
        # Create a fallback placeholder image with PIL
        im = Image.new('RGB', (800, 500), color=(255, 122, 24))
        im.save(dest_path, 'JPEG')
        return True

DEMO_DATA = [
    {
        "host": {
            "username": "host_anjali_gaya",
            "display_name": "Anjali Kumari",
            "full_name": "Anjali Kumari",
            "email": "anjali.gaya@hiddenyatra.demo",
            "bio": "Passionate heritage educator and cultural host in Bodh Gaya. Hosting mindful travellers since 2022 to share local Buddhist traditions, organic meals, and temple walks.",
            "district_id": 2,
            "district_name": "Gaya",
            "languages": "Hindi, English, Magahi",
            "phone": "+91 98350 12001",
            "avatar_emoji": "🧘‍♀️",
            "avg_host_rating": 4.9,
            "total_hosted": 34
        },
        "listing": {
            "title": "Bodh Gaya Lotus Heritage Homestay",
            "slug": "bodh-gaya-lotus-heritage-homestay",
            "listing_type": "paid_homestay",
            "property_type": "heritage_homestay",
            "price_per_night": 1200.00,
            "max_guests": 4,
            "min_stay_nights": 1,
            "max_stay_nights": 14,
            "num_rooms": 2,
            "num_beds": 2,
            "num_bathrooms": 2,
            "district_id": 2,
            "address_text": "Near Kalachakra Ground, Mastipur, Bodh Gaya",
            "address_full": "House No. 42, Lotus Lane, Mastipur, Bodh Gaya, Gaya, Bihar 824231",
            "latitude": 24.6961300,
            "longitude": 84.9912800,
            "description": "Experience serene and mindful living at Bodh Gaya Lotus Heritage Homestay, located just 800 metres from the UNESCO World Heritage Mahabodhi Temple.\n\nOur traditional brick and clay home features a shaded open-air rooftop terrace ideal for morning yoga, meditation, and reading. Enjoy freshly prepared satvik home-cooked Bihar meals including Dal-Bhat-Bhujia, sattu parathas, and seasonal herbal teas. The guest rooms are spacious, air-cooled, with spotless attached private bathrooms and high-speed Wi-Fi.",
            "amenities": ["wifi", "hot_water", "local_food", "meals", "power_backup", "garden", "balcony", "guide"],
            "house_rules": "• Quiet hours after 10:00 PM\n• Shoes off inside guest rooms\n• Vegetarian meals served\n• No smoking or alcohol on premises",
            "check_in_time": "12:00 PM",
            "check_out_time": "11:00 AM",
            "cancellation_policy": "flexible",
            "is_featured": 1,
            "avg_rating": 4.9,
            "review_count": 28,
            "cover_image": "stay_demo_gaya_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_gaya_cover.jpg", "caption": "Serene exterior & sunlit courtyard"},
                {"url": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_gaya_bedroom.jpg", "caption": "Comfortable master bedroom with study desk"},
                {"url": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_gaya_terrace.jpg", "caption": "Peaceful rooftop yoga & meditation terrace"},
                {"url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_gaya_dining.jpg", "caption": "Traditional dining area for home-cooked meals"}
            ]
        }
    },
    {
        "host": {
            "username": "host_neha_nalanda",
            "display_name": "Neha Singh",
            "full_name": "Neha Singh",
            "email": "neha.nalanda@hiddenyatra.demo",
            "bio": "Certified local nature guide and eco-homestay host in Rajgir. Fond of sharing Magadha history, hot spring lore, and cycling routes around Nalanda ruins.",
            "district_id": 3,
            "district_name": "Nalanda",
            "languages": "Hindi, English, Magahi",
            "phone": "+91 94310 44002",
            "avatar_emoji": "🌿",
            "avg_host_rating": 4.8,
            "total_hosted": 42
        },
        "listing": {
            "title": "Rajgir Green Valley Eco Homestay",
            "slug": "rajgir-green-valley-eco-homestay",
            "listing_type": "paid_homestay",
            "property_type": "eco_cottage",
            "price_per_night": 1500.00,
            "max_guests": 5,
            "min_stay_nights": 1,
            "max_stay_nights": 10,
            "num_rooms": 2,
            "num_beds": 3,
            "num_bathrooms": 2,
            "district_id": 3,
            "address_text": "Venuvan Valley Road, Rajgir, Nalanda",
            "address_full": "Plot 18, Bamboo Grove Path, Rajgir, Nalanda, Bihar 803116",
            "latitude": 25.0188900,
            "longitude": 85.4219400,
            "description": "Nestled at the gentle foothills of the Rajgir mountain range, Rajgir Green Valley Eco Homestay is an environmentally conscious cottage built with local stone, bamboo, and terracotta.\n\nWake up to the birdsong of Venuvan, breathe in the fresh mountain air, and explore nearby Gridhakuta (Vulture Peak) and the ancient Nalanda University ruins. We offer complimentary bicycles, herbal tea from our garden, and authentic Bihari culinary classics including Khaja from Silao and hot Litti Chokha.",
            "amenities": ["wifi", "hot_water", "ac", "parking", "local_food", "garden", "balcony", "guide", "pickup"],
            "house_rules": "• Eco-friendly stay: please conserve water and power\n• Check-in with valid ID\n• Mountain bicycle gear available upon request",
            "check_in_time": "01:00 PM",
            "check_out_time": "11:00 AM",
            "cancellation_policy": "flexible",
            "is_featured": 1,
            "avg_rating": 4.8,
            "review_count": 31,
            "cover_image": "stay_demo_rajgir_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_rajgir_cover.jpg", "caption": "Eco cottage exterior with flowering garden"},
                {"url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_rajgir_bedroom.jpg", "caption": "Cosy timber-accented guest bedroom"},
                {"url": "https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_rajgir_garden.jpg", "caption": "Lush garden walkway with mountain backdrop"},
                {"url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_rajgir_bathroom.jpg", "caption": "Modern private attached bathroom with hot shower"}
            ]
        }
    },
    {
        "host": {
            "username": "host_sunil_jamui",
            "display_name": "Sunil Soren",
            "full_name": "Sunil Soren",
            "email": "sunil.jamui@hiddenyatra.demo",
            "bio": "Nature enthusiast and community host from Simultala. Promoting eco-tourism around Laka Dam, Indrape Hill, and pine hills for urban travellers seeking peace.",
            "district_id": 4,
            "district_name": "Jamui",
            "languages": "Hindi, Santhali, Angika",
            "phone": "+91 97712 55003",
            "avatar_emoji": "🌲",
            "avg_host_rating": 4.9,
            "total_hosted": 22
        },
        "listing": {
            "title": "Simultala Pine Breeze Forest Stay",
            "slug": "simultala-pine-breeze-forest-stay",
            "listing_type": "paid_homestay",
            "property_type": "hill_cottage",
            "price_per_night": 1000.00,
            "max_guests": 4,
            "min_stay_nights": 1,
            "max_stay_nights": 14,
            "num_rooms": 2,
            "num_beds": 2,
            "num_bathrooms": 1,
            "district_id": 4,
            "address_text": "Station Road, Simultala Hill Station, Jamui",
            "address_full": "Simultala Heights, Near Telecom Tower, Jamui, Bihar 811316",
            "latitude": 24.7125000,
            "longitude": 86.5416700,
            "description": "Simultala, historically famous as the 'Mini Shimla of Bihar', offers crisp healthy air, pine groves, and panoramic sunset viewpoints.\n\nSimultala Pine Breeze Forest Stay provides a peaceful, rejuvenating getaway. Enjoy warm hospitality, home-cooked organic meals, traditional Chhena Murki sweets, and guided nature walks to Laka Ring Dam and Haldifarna spring.",
            "amenities": ["hot_water", "parking", "local_food", "meals", "garden", "balcony", "guide", "pet_friendly"],
            "house_rules": "• Respect local village customs\n• Bonfires permitted in designated garden area\n• Early morning bird watching tours available",
            "check_in_time": "12:00 PM",
            "check_out_time": "10:30 AM",
            "cancellation_policy": "flexible",
            "is_featured": 0,
            "avg_rating": 4.9,
            "review_count": 19,
            "cover_image": "stay_demo_simultala_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_simultala_cover.jpg", "caption": "Pine grove hill cottage exterior"},
                {"url": "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_simultala_bedroom.jpg", "caption": "Spacious bedroom with garden vista"},
                {"url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_simultala_veranda.jpg", "caption": "Colonial veranda overlooking pine hills"},
                {"url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_simultala_dining.jpg", "caption": "Country dining table with fresh regional cooking"}
            ]
        }
    },
    {
        "host": {
            "username": "host_amit_bhagalpur",
            "display_name": "Amit Kumar",
            "full_name": "Amit Kumar",
            "email": "amit.bhagalpur@hiddenyatra.demo",
            "bio": "Master Tussar silk weaver and Manjusha folk art supporter from Champanagar, Bhagalpur. Delighted to host travellers and demonstrate heritage loom weaving.",
            "district_id": 5,
            "district_name": "Bhagalpur",
            "languages": "Hindi, Angika, English",
            "phone": "+91 94701 88004",
            "avatar_emoji": "🧵",
            "avg_host_rating": 4.8,
            "total_hosted": 29
        },
        "listing": {
            "title": "Silk City Weaver's Heritage Homestay",
            "slug": "silk-city-weavers-heritage-homestay",
            "listing_type": "paid_homestay",
            "property_type": "heritage_homestay",
            "price_per_night": 1100.00,
            "max_guests": 3,
            "min_stay_nights": 1,
            "max_stay_nights": 7,
            "num_rooms": 2,
            "num_beds": 2,
            "num_bathrooms": 1,
            "district_id": 5,
            "address_text": "Weavers Colony, Champanagar, Bhagalpur",
            "address_full": "Near Nathnagar Road, Champanagar, Bhagalpur, Bihar 812004",
            "latitude": 25.2444500,
            "longitude": 86.9718400,
            "description": "Stay in the heart of Bhagalpur's centuries-old silk weaving community! Our homestay is decorated with genuine Tussar silk fabrics and vibrant Manjusha art murals.\n\nGuests can observe handloom silk processing, take sunset boat rides on the Ganges to spot Gangetic river dolphins at Vikramshila Sanctuary, and savor fragrant Katarni Chura breakfast.",
            "amenities": ["wifi", "ac", "hot_water", "local_food", "guide", "power_backup", "meals"],
            "house_rules": "• Handloom studio visits free for in-house guests\n• Pure home-cooked vegetarian meals\n• ID verification required at check-in",
            "check_in_time": "12:30 PM",
            "check_out_time": "11:00 AM",
            "cancellation_policy": "flexible",
            "is_featured": 1,
            "avg_rating": 4.8,
            "review_count": 24,
            "cover_image": "stay_demo_bhagalpur_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_bhagalpur_cover.jpg", "caption": "Silk heritage courtyard exterior"},
                {"url": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_bhagalpur_bedroom.jpg", "caption": "Handcrafted silk furnishings & warm queen bed"},
                {"url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_bhagalpur_courtyard.jpg", "caption": "Traditional open courtyard with Manjusha artwork"},
                {"url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_bhagalpur_dining.jpg", "caption": "Traditional thali dining experience"}
            ]
        }
    },
    {
        "host": {
            "username": "host_vikram_patna",
            "display_name": "Prof. Vikramaditya Verma",
            "full_name": "Vikramaditya Verma",
            "email": "vikram.patna@hiddenyatra.demo",
            "bio": "Retired history professor residing in an ancestral colonial-era home near the Ganges in Patna. Passionate about sharing the rich saga of ancient Pataliputra.",
            "district_id": 1,
            "district_name": "Patna",
            "languages": "Hindi, English, Bhojpuri",
            "phone": "+91 98352 99005",
            "avatar_emoji": "🏛️",
            "avg_host_rating": 4.9,
            "total_hosted": 58
        },
        "listing": {
            "title": "Patliputra Heritage Courtyard Stay",
            "slug": "patliputra-heritage-courtyard-stay",
            "listing_type": "paid_homestay",
            "property_type": "heritage_homestay",
            "price_per_night": 1800.00,
            "max_guests": 6,
            "min_stay_nights": 1,
            "max_stay_nights": 21,
            "num_rooms": 3,
            "num_beds": 4,
            "num_bathrooms": 2,
            "district_id": 1,
            "address_text": "Danapur Cantonment / Riverside Road, Patna",
            "address_full": "Haveli 12, Old Ganga Path, Danapur, Patna, Bihar 801503",
            "latitude": 25.6292500,
            "longitude": 85.0489100,
            "description": "Experience old-world charm combined with modern comforts in this 90-year-old restored brick courtyard mansion overlooking the Ganges.\n\nFeaturing high ceilings, antique teakwood furniture, a rich personal library of Bihar history, high-speed fiber internet, and a rooftop terrace for evening river breeze. Authentic dinner featuring smoked Litti Chokha and Ghugni prepared daily.",
            "amenities": ["wifi", "ac", "hot_water", "parking", "kitchen", "local_food", "tv", "power_backup", "washing_machine"],
            "house_rules": "• Family friendly environment\n• No loud parties\n• Smoking allowed only on open rooftop terrace",
            "check_in_time": "02:00 PM",
            "check_out_time": "11:30 AM",
            "cancellation_policy": "flexible",
            "is_featured": 1,
            "avg_rating": 4.9,
            "review_count": 46,
            "cover_image": "stay_demo_patna_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_patna_cover.jpg", "caption": "Historic brick courtyard mansion exterior"},
                {"url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_patna_bedroom.jpg", "caption": "Grand master suite with vintage teak furnishings"},
                {"url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_patna_living.jpg", "caption": "Library lounge with historical book collection"},
                {"url": "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_patna_bathroom.jpg", "caption": "Modern bathroom with walk-in shower & hot water"}
            ]
        }
    },
    {
        "host": {
            "username": "host_priya_vaishali",
            "display_name": "Priya Devi",
            "full_name": "Priya Devi",
            "email": "priya.vaishali@hiddenyatra.demo",
            "bio": "Organic farmer and women self-help group coordinator in rural Vaishali. Welcomes genuine cultural travellers to experience village hospitality and organic farm living.",
            "district_id": 37,
            "district_name": "Vaishali",
            "languages": "Hindi, Bajjika",
            "phone": "+91 94318 77006",
            "avatar_emoji": "🌾",
            "avg_host_rating": 5.0,
            "total_hosted": 18
        },
        "listing": {
            "title": "Vaishali Mango Orchard Village Stay",
            "slug": "vaishali-mango-orchard-village-stay",
            "listing_type": "free_stay",
            "property_type": "farmstay",
            "price_per_night": 0.00,
            "max_guests": 4,
            "min_stay_nights": 1,
            "max_stay_nights": 5,
            "num_rooms": 2,
            "num_beds": 2,
            "num_bathrooms": 1,
            "district_id": 37,
            "address_text": "Village Basarh, Near Ashokan Pillar, Vaishali",
            "address_full": "Gram Panchayat Basarh, Vaishali District, Bihar 844128",
            "latitude": 25.9875000,
            "longitude": 85.1275000,
            "description": "Experience true Bihar village hospitality at zero accommodation cost! Located in a tranquil organic mango and litchi orchard near the historic Ashokan Pillar and Buddha Relic Stupa.\n\nStay in clean traditional clay-walled rooms with fresh well water, taste woodfire-cooked chulha rotis, seasonal mangoes, and join our village heritage walks. This is a community-supported cultural exchange homestay for respectful travellers.",
            "amenities": ["local_food", "meals", "garden", "guide", "pet_friendly", "first_aid"],
            "house_rules": "• Free stay for cultural exchange & conscious backpackers\n• Help with orchard activities or community storytelling\n• Alcohol strictly prohibited",
            "check_in_time": "11:00 AM",
            "check_out_time": "10:00 AM",
            "cancellation_policy": "flexible",
            "is_featured": 0,
            "avg_rating": 5.0,
            "review_count": 15,
            "cover_image": "stay_demo_vaishali_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_vaishali_cover.jpg", "caption": "Organic mango orchard cottage exterior"},
                {"url": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_vaishali_bedroom.jpg", "caption": "Spotless and airy village guest room"},
                {"url": "https://images.unsplash.com/photo-1500076656116-558758c991c1?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_vaishali_farm.jpg", "caption": "Lush green village footpath through mango groves"},
                {"url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_vaishali_courtyard.jpg", "caption": "Open veranda with woven charpai cots"}
            ]
        }
    },
    {
        "host": {
            "username": "host_arvind_madhubani",
            "display_name": "Dr. Arvind Jha",
            "full_name": "Arvind Kumar Jha",
            "email": "arvind.madhubani@hiddenyatra.demo",
            "bio": "Mithila folk art scholar and Sanskrit researcher from Jhanjharpur/Ranti. Promoting genuine village artisans and traditional Maithil living.",
            "district_id": 20,
            "district_name": "Jhanjharpur (Madhubani)",
            "languages": "Maithili, Hindi, English, Sanskrit",
            "phone": "+91 94308 66007",
            "avatar_emoji": "🎨",
            "avg_host_rating": 4.9,
            "total_hosted": 37
        },
        "listing": {
            "title": "Mithila Folk Art & Heritage Homestay",
            "slug": "mithila-folk-art-heritage-homestay",
            "listing_type": "paid_homestay",
            "property_type": "art_homestay",
            "price_per_night": 800.00,
            "max_guests": 4,
            "min_stay_nights": 1,
            "max_stay_nights": 14,
            "num_rooms": 2,
            "num_beds": 3,
            "num_bathrooms": 1,
            "district_id": 20,
            "address_text": "Artist Village Ranti, Jhanjharpur, Madhubani",
            "address_full": "Mithila Kala Kutir, Village Ranti, Madhubani, Bihar 847211",
            "latitude": 26.3550000,
            "longitude": 86.0850000,
            "description": "Live inside a living canvas of traditional Madhubani art! Every wall of this rural Mithila home is painted by local women artists depicting Kohbar, Ram-Sita vivaah, and nature motifs.\n\nEnjoy hands-on painting workshops using natural mineral pigments and bamboo twigs. Savor authentic Maithili delicacies including Machh-Bhat, Ol ki chutney, and Makhana kheer.",
            "amenities": ["wifi", "local_food", "meals", "garden", "guide", "first_aid", "pickup"],
            "house_rules": "• Interactive art sessions available daily\n• Respect artisan working spaces\n• Traditional satvik Maithil meals served",
            "check_in_time": "12:00 PM",
            "check_out_time": "11:00 AM",
            "cancellation_policy": "flexible",
            "is_featured": 1,
            "avg_rating": 4.9,
            "review_count": 33,
            "cover_image": "stay_demo_madhubani_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_madhubani_cover.jpg", "caption": "Hand-painted traditional Mithila village home"},
                {"url": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_madhubani_bedroom.jpg", "caption": "Artisan-decorated bedroom with handloom textiles"},
                {"url": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_madhubani_workshop.jpg", "caption": "Traditional natural pigment painting workshop"},
                {"url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_madhubani_courtyard.jpg", "caption": "Spacious central courtyard for evening folklore discussions"}
            ]
        }
    },
    {
        "host": {
            "username": "host_manju_munger",
            "display_name": "Manju Sinha",
            "full_name": "Manju Sinha",
            "email": "manju.munger@hiddenyatra.demo",
            "bio": "Certified yoga instructor and home baker in Munger. Offers mindful stays next to the Ganges and near the renowned Bihar School of Yoga.",
            "district_id": 6,
            "district_name": "Munger",
            "languages": "Hindi, English",
            "phone": "+91 94314 33008",
            "avatar_emoji": "🧘",
            "avg_host_rating": 4.8,
            "total_hosted": 26
        },
        "listing": {
            "title": "Munger Ganga Riverfront Yoga Stay",
            "slug": "munger-ganga-riverfront-yoga-stay",
            "listing_type": "paid_homestay",
            "property_type": "yoga_retreat",
            "price_per_night": 1400.00,
            "max_guests": 4,
            "min_stay_nights": 1,
            "max_stay_nights": 14,
            "num_rooms": 2,
            "num_beds": 2,
            "num_bathrooms": 2,
            "district_id": 6,
            "address_text": "Ganga Darshan Road, Near Munger Fort, Munger",
            "address_full": "Ashram View Villa, Ganga Ghat Path, Munger, Bihar 811201",
            "latitude": 25.3750000,
            "longitude": 86.4750000,
            "description": "Recharge your mind, body, and spirit at Munger Ganga Riverfront Yoga Stay.\n\nEnjoy sunrise yoga sessions on our open terrace looking out over the sacred river Ganges and historic Munger Fort walls. We serve Ayurvedic vegetarian breakfasts, herbal teas, and assist guests with visits to Kashtaharini Ghat, Sita Kund, and Bhimbandh Wildlife Sanctuary.",
            "amenities": ["wifi", "hot_water", "ac", "local_food", "meals", "balcony", "garden", "power_backup"],
            "house_rules": "• Daily morning yoga session (optional for guests)\n• Quiet hours after 9:30 PM\n• Sattvic vegetarian meals only",
            "check_in_time": "01:00 PM",
            "check_out_time": "11:00 AM",
            "cancellation_policy": "flexible",
            "is_featured": 0,
            "avg_rating": 4.8,
            "review_count": 21,
            "cover_image": "stay_demo_munger_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_munger_cover.jpg", "caption": "Riverfront property exterior with lush trees"},
                {"url": "https://images.unsplash.com/photo-1591088398332-8a7791972843?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_munger_bedroom.jpg", "caption": "Minimalist and airy bedroom with wooden floor"},
                {"url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_munger_terrace.jpg", "caption": "Sunrise yoga and meditation deck"},
                {"url": "https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_munger_dining.jpg", "caption": "Organic satvik vegetarian breakfast table"}
            ]
        }
    },
    {
        "host": {
            "username": "host_ravi_rohtas",
            "display_name": "Ravi Shankar Pandey",
            "full_name": "Ravi Shankar Pandey",
            "email": "ravi.rohtas@hiddenyatra.demo",
            "bio": "Local trekking leader and heritage lover from Sasaram. Guiding visitors to Rohtasgarh Fort, Tutla Bhawani Waterfall, and Sher Shah Tomb.",
            "district_id": 8,
            "district_name": "Rohtas",
            "languages": "Hindi, Bhojpuri, English",
            "phone": "+91 94312 22009",
            "avatar_emoji": "🏰",
            "avg_host_rating": 4.9,
            "total_hosted": 39
        },
        "listing": {
            "title": "Sasaram Sher Shah Heritage Homestay",
            "slug": "sasaram-sher-shah-heritage-homestay",
            "listing_type": "paid_homestay",
            "property_type": "heritage_homestay",
            "price_per_night": 1000.00,
            "max_guests": 5,
            "min_stay_nights": 1,
            "max_stay_nights": 10,
            "num_rooms": 2,
            "num_beds": 3,
            "num_bathrooms": 2,
            "district_id": 8,
            "address_text": "Tomb Circular Road, Sasaram, Rohtas",
            "address_full": "Heritage Lane 5, Near Grand Tomb Gate, Sasaram, Bihar 821115",
            "latitude": 24.9540000,
            "longitude": 84.0320000,
            "description": "Stay in a restored sandstone haveli walking distance from the majestic water mausoleum of Sher Shah Suri in Sasaram.\n\nOur property is the perfect base for exploring Rohtasgarh Fort, Dhuan Kund waterfalls, and the Kaimur hill plateau. Features modern clean rooms, private secure parking, local guide support, and spicy Bihari mutton or paneer thali dinners.",
            "amenities": ["wifi", "ac", "hot_water", "parking", "local_food", "meals", "guide", "pickup", "power_backup"],
            "house_rules": "• Guided trekking excursions available on advance request\n• ID verification mandatory\n• Respect local monument regulations",
            "check_in_time": "12:00 PM",
            "check_out_time": "11:00 AM",
            "cancellation_policy": "flexible",
            "is_featured": 1,
            "avg_rating": 4.9,
            "review_count": 35,
            "cover_image": "stay_demo_rohtas_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_rohtas_cover.jpg", "caption": "Sandstone heritage home exterior"},
                {"url": "https://images.unsplash.com/photo-1578898887932-dce23a595ad4?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_rohtas_bedroom.jpg", "caption": "Spacious traditional bedroom with comfortable beds"},
                {"url": "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_rohtas_lounge.jpg", "caption": "Upper floor veranda lounge overlooking city skyline"},
                {"url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_rohtas_bathroom.jpg", "caption": "Modern attached bathroom with 24/7 hot water"}
            ]
        }
    },
    {
        "host": {
            "username": "host_kavita_kaimur",
            "display_name": "Kavita Tiwari",
            "full_name": "Kavita Tiwari",
            "email": "kavita.kaimur@hiddenyatra.demo",
            "bio": "Eco-conservationist and village homestay host in Adhaura / Kaimur hills. Offering free hospitality to nature lovers, birdwatchers, and forest trekkers.",
            "district_id": 22,
            "district_name": "Kaimur",
            "languages": "Hindi, Bhojpuri",
            "phone": "+91 94316 11010",
            "avatar_emoji": "🏞️",
            "avg_host_rating": 4.9,
            "total_hosted": 16
        },
        "listing": {
            "title": "Kaimur Plateau Waterfall Farmstay",
            "slug": "kaimur-plateau-waterfall-farmstay",
            "listing_type": "free_stay",
            "property_type": "farmstay",
            "price_per_night": 0.00,
            "max_guests": 3,
            "min_stay_nights": 1,
            "max_stay_nights": 7,
            "num_rooms": 1,
            "num_beds": 2,
            "num_bathrooms": 1,
            "district_id": 22,
            "address_text": "Near Telhar Kund Road, Bhabhua, Kaimur",
            "address_full": "Adhaura Plateau Road, Kaimur Hills, Bihar 821102",
            "latitude": 24.8100000,
            "longitude": 83.5800000,
            "description": "Immerse yourself in raw, untouched wilderness on the Kaimur Plateau! This free community stay is hosted on an organic farm near Telhar Kund and Karkat Waterfalls.\n\nSleep under starry skies, enjoy freshly harvested organic meals, listen to forest birds at dawn, and explore hidden canyon trails. Ideal for trekking enthusiasts and nature photographers.",
            "amenities": ["local_food", "meals", "garden", "guide", "pet_friendly", "first_aid"],
            "house_rules": "• Free stay for nature lovers & environmentalists\n• Zero plastic waste zone: please carry back non-biodegradable waste\n• Forest trekking must follow sanctuary safety guidelines",
            "check_in_time": "12:00 PM",
            "check_out_time": "11:00 AM",
            "cancellation_policy": "flexible",
            "is_featured": 0,
            "avg_rating": 4.9,
            "review_count": 14,
            "cover_image": "stay_demo_kaimur_cover.jpg",
            "photos": [
                {"url": "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_kaimur_cover.jpg", "caption": "Scenic stone farm cottage on Kaimur plateau"},
                {"url": "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_kaimur_bedroom.jpg", "caption": "Cosy timber-finish bedroom with valley breeze"},
                {"url": "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_kaimur_waterfall.jpg", "caption": "Nearby Telhar Kund waterfall stream"},
                {"url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop&q=80", "file": "stay_demo_kaimur_lawn.jpg", "caption": "Open-air seating & campfire area under the night sky"}
            ]
        }
    }
]

def run_population():
    print("=== STARTING DEMO HOMESTAYS POPULATION ===")
    created_hosts = []
    created_listings = []
    photos_added = 0

    pw_hash = generate_password_hash("DemoHost@123")

    with get_cursor(commit=True) as cur:
        for item in DEMO_DATA:
            h_data = item['host']
            l_data = item['listing']

            # 1. Ensure user exists
            cur.execute("SELECT id FROM users WHERE username = %s", (h_data['username'],))
            user = cur.fetchone()
            if not user:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, display_name, full_name, phone, status, email_verified, is_host, avatar_emoji)
                    VALUES (%s, %s, %s, %s, %s, %s, 'active', 1, 1, %s)
                """, (h_data['username'], h_data['email'], pw_hash, h_data['display_name'], h_data['full_name'], h_data['phone'], h_data['avatar_emoji']))
                user_id = cur.lastrowid
                print(f"Created User ID {user_id}: {h_data['display_name']}")
            else:
                user_id = user['id']

            # 2. Ensure host_profile exists
            cur.execute("SELECT id FROM host_profiles WHERE user_id = %s", (user_id,))
            hp = cur.fetchone()
            if not hp:
                cur.execute("""
                    INSERT INTO host_profiles
                        (user_id, bio, languages, district_id, verification_status, verified_at, is_verified_badge, avg_host_rating, total_hosted, response_rate, response_time_hrs)
                    VALUES (%s, %s, %s, %s, 'approved', NOW(), 1, %s, %s, 98.5, 1.2)
                """, (user_id, h_data['bio'], h_data['languages'], h_data['district_id'], h_data['avg_host_rating'], h_data['total_hosted']))
                host_id = cur.lastrowid
                created_hosts.append(host_id)
                print(f"Created Host Profile ID {host_id} for {h_data['display_name']}")
            else:
                host_id = hp['id']
                # Ensure verified
                cur.execute("UPDATE host_profiles SET verification_status='approved', is_verified_badge=1, avg_host_rating=%s WHERE id=%s", (h_data['avg_host_rating'], host_id))

            # 3. Download photos
            print(f"\nProcessing photos for '{l_data['title']}':")
            for p in l_data['photos']:
                download_and_save_image(p['url'], p['file'])

            # 4. Check if listing already exists by slug
            cur.execute("SELECT id FROM host_listings WHERE slug = %s", (l_data['slug'],))
            existing_listing = cur.fetchone()
            if not existing_listing:
                amenities_json = json.dumps(l_data['amenities'])
                cur.execute("""
                    INSERT INTO host_listings
                        (host_id, listing_type, title, slug, description,
                         district_id, address_text, address_full, latitude, longitude,
                         price_per_night, max_guests, min_stay_nights, max_stay_nights,
                         num_rooms, num_beds, num_bathrooms, property_type,
                         amenities, house_rules, check_in_time, check_out_time,
                         cancellation_policy, cover_image, status, is_featured,
                         avg_rating, review_count, view_count, created_at, updated_at)
                    VALUES
                        (%s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s,
                         %s, %s, %s, %s,
                         %s, %s, %s, %s,
                         %s, %s, %s, %s,
                         %s, %s, 'published', %s,
                         %s, %s, 120, NOW(), NOW())
                """, (
                    host_id, l_data['listing_type'], l_data['title'], l_data['slug'], l_data['description'],
                    l_data['district_id'], l_data['address_text'], l_data['address_full'], l_data['latitude'], l_data['longitude'],
                    l_data['price_per_night'], l_data['max_guests'], l_data['min_stay_nights'], l_data['max_stay_nights'],
                    l_data['num_rooms'], l_data['num_beds'], l_data['num_bathrooms'], l_data['property_type'],
                    amenities_json, l_data['house_rules'], l_data['check_in_time'], l_data['check_out_time'],
                    l_data['cancellation_policy'], l_data['cover_image'], l_data['is_featured'],
                    l_data['avg_rating'], l_data['review_count']
                ))
                listing_id = cur.lastrowid
                created_listings.append(listing_id)
                print(f"Created Listing ID {listing_id}: '{l_data['title']}' (Rs.{l_data['price_per_night']})")
            else:
                listing_id = existing_listing['id']
                print(f"Listing ID {listing_id} already exists: '{l_data['title']}'")
                # Update cover_image to ensure it matches
                cur.execute("UPDATE host_listings SET cover_image = %s, status = 'published' WHERE id = %s", (l_data['cover_image'], listing_id))

            # 5. Insert listing photos
            cur.execute("DELETE FROM listing_photos WHERE listing_id = %s", (listing_id,))
            for idx, p in enumerate(l_data['photos']):
                cur.execute("""
                    INSERT INTO listing_photos (listing_id, filename, caption, sort_order, uploaded_at)
                    VALUES (%s, %s, %s, %s, NOW())
                """, (listing_id, p['file'], p['caption'], idx))
                photos_added += 1

    print(f"\n=== POPULATION COMPLETE ===")
    print(f"Created {len(created_hosts)} host profiles")
    print(f"Created {len(created_listings)} listings")
    print(f"Populated {photos_added} listing gallery photos")

if __name__ == '__main__':
    run_population()
