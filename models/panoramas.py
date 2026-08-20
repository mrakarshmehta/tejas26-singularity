"""
Virtual 360-Degree Panorama & Heritage Viewpoint Experience Model
Provides metadata, coordinate hotspots, 360-degree photo sphere links,
aerial drone perspectives, and immersive historical narration links.
"""

VIRTUAL_PANORAMAS_DB = [
    {
        "id": "pano-mahabodhi-sanctum",
        "slug": "mahabodhi-temple-sanctum",
        "title": "Mahabodhi Temple Inner Sanctum & Vajrasana",
        "place_slug": "mahabodhi",
        "district": "Gaya",
        "category": "Spiritual Heritage",
        "tagline": "Stand beneath the sacred Bodhi Tree where Prince Siddhartha attained supreme enlightenment.",
        "sphere_image_url": "/static/images/panoramas/mahabodhi_sanctum_360.webp",
        "thumbnail_url": "/static/images/panoramas/mahabodhi_thumb.webp",
        "resolution": "8K UHD",
        "capture_altitude_meters": 3,
        "coordinates": {"lat": 24.6961, "lng": 84.9913},
        "audio_narration_available": True,
        "audio_language_codes": ["en", "hi", "bho", "tib"],
        "hotspots": [
            {
                "id": "hs-bodhi-tree",
                "pitch": -5.2,
                "yaw": 110.4,
                "title": "Venerable Sacred Bodhi Tree",
                "description": "Direct descendant of the original Ficus religiosa tree beneath which Lord Buddha meditated."
            },
            {
                "id": "hs-vajrasana",
                "pitch": -12.0,
                "yaw": 125.0,
                "title": "Vajrasana (Diamond Throne)",
                "description": "The polished sandstone slab installed by Emperor Ashoka marking the exact spot of enlightenment."
            },
            {
                "id": "hs-spire",
                "pitch": 45.0,
                "yaw": 0.0,
                "title": "55-Meter Grand Stupa Spire",
                "description": "Ornate architectural masterpiece restored in the 19th century adorned with gold-plated pinnacle."
            }
        ]
    },
    {
        "id": "pano-nalanda-monastery",
        "slug": "ancient-nalanda-monastery-complex",
        "title": "Ancient Nalanda Mahavihara Main Temple Site No. 3",
        "place_slug": "nalanda-ruins",
        "district": "Nalanda",
        "category": "Ancient Education",
        "tagline": "Explore the multi-tiered votive stupas of the world's first global residential university.",
        "sphere_image_url": "/static/images/panoramas/nalanda_temple3_360.webp",
        "thumbnail_url": "/static/images/panoramas/nalanda_thumb.webp",
        "resolution": "8K UHD",
        "capture_altitude_meters": 12,
        "coordinates": {"lat": 25.1357, "lng": 85.4450},
        "audio_narration_available": True,
        "audio_language_codes": ["en", "hi", "zh", "ko"],
        "hotspots": [
            {
                "id": "hs-stupa-stairs",
                "pitch": -8.5,
                "yaw": 35.0,
                "title": "Corner Votive Towers",
                "description": "Intricately carved stucco figures from the Gupta and Pala imperial golden ages."
            },
            {
                "id": "hs-library-ruins",
                "pitch": 0.0,
                "yaw": 180.0,
                "title": "Dharmaganja Library View",
                "description": "Direction towards the legendary nine-story Ratnasagara and Ratnodadhi manuscript repositories."
            }
        ]
    },
    {
        "id": "pano-rajgir-peace-pagoda",
        "slug": "rajgir-vishwa-shanti-stupa",
        "title": "Rajgir Vishwa Shanti Stupa & Ratnagiri Hill",
        "place_slug": "rajgir-peace-pagoda",
        "district": "Nalanda",
        "category": "Spiritual Heritage",
        "tagline": "Gaze over the rugged hills of ancient Rajagriha from the summit of the World Peace Pagoda.",
        "sphere_image_url": "/static/images/panoramas/rajgir_stupa_360.webp",
        "thumbnail_url": "/static/images/panoramas/rajgir_thumb.webp",
        "resolution": "8K UHD",
        "capture_altitude_meters": 400,
        "coordinates": {"lat": 25.0134, "lng": 85.4194},
        "audio_narration_available": True,
        "audio_language_codes": ["en", "hi", "ja"],
        "hotspots": [
            {
                "id": "hs-golden-buddha",
                "pitch": 5.0,
                "yaw": 45.0,
                "title": "Golden Statues of Buddha's Four Life Stages",
                "description": "Depicting Birth, Enlightenment, First Sermon, and Mahaparinirvana."
            },
            {
                "id": "hs-vulture-peak",
                "pitch": -18.0,
                "yaw": 240.0,
                "title": "Gridhakuta (Vulture's Peak) Gorge",
                "description": "Lord Buddha's favorite retreat where the Prajnaparamita and Lotus Sutras were preached."
            }
        ]
    },
    {
        "id": "pano-rohtasgarh-fort",
        "slug": "rohtasgarh-fort-hawa-mahal",
        "title": "Rohtasgarh Fortress Grand Ramparts & Hawa Mahal",
        "place_slug": "rohtasgarh-fort",
        "district": "Rohtas",
        "category": "Military & Royal Heritage",
        "tagline": "Perched atop the Kaimur Plateau 1500 feet above the Son River valley.",
        "sphere_image_url": "/static/images/panoramas/rohtasgarh_360.webp",
        "thumbnail_url": "/static/images/panoramas/rohtasgarh_thumb.webp",
        "resolution": "8K UHD",
        "capture_altitude_meters": 450,
        "coordinates": {"lat": 24.6300, "lng": 83.9200},
        "audio_narration_available": True,
        "audio_language_codes": ["en", "hi"],
        "hotspots": [
            {
                "id": "hs-man-singh-palace",
                "pitch": 2.0,
                "yaw": 85.0,
                "title": "Raja Man Singh Palace",
                "description": "Mughal-Rajput fusion palace fortress built during the governorship of Raja Man Singh I."
            },
            {
                "id": "hs-son-gorge",
                "pitch": -22.0,
                "yaw": 290.0,
                "title": "Son River Chasm & Kaimur Escarpment",
                "description": "Impregnable natural cliff barriers protecting the ancient stronghold."
            }
        ]
    },
    {
        "id": "pano-barabar-caves",
        "slug": "barabar-lomas-rishi-cave",
        "title": "Barabar Caves Lomas Rishi Polished Granite Chamber",
        "place_slug": "barabar-caves",
        "district": "Jehanabad",
        "category": "Ancient Rock-Cut Architecture",
        "tagline": "Enter the world's oldest surviving rock-cut caves carved in the 3rd century BCE under Emperor Ashoka.",
        "sphere_image_url": "/static/images/panoramas/barabar_360.webp",
        "thumbnail_url": "/static/images/panoramas/barabar_thumb.webp",
        "resolution": "8K UHD",
        "capture_altitude_meters": 5,
        "coordinates": {"lat": 25.0064, "lng": 85.0625},
        "audio_narration_available": True,
        "audio_language_codes": ["en", "hi"],
        "hotspots": [
            {
                "id": "hs-elephant-frieze",
                "pitch": 10.0,
                "yaw": 0.0,
                "title": "Elephant Arch Facade",
                "description": "Earliest known depiction of the chaitya arch in Indian rock architecture with procession of carved elephants."
            },
            {
                "id": "hs-glass-mirror-polish",
                "pitch": -5.0,
                "yaw": 90.0,
                "title": "Mauryan Mirror Polish",
                "description": "Flawlessly smoothed granite creating mystical acoustic reverberations for Ajivika meditators."
            }
        ]
    },
    {
        "id": "pano-sasaram-tomb",
        "slug": "sher-shah-suri-tomb-lake",
        "title": "Sher Shah Suri Tomb Floating Mausoleum",
        "place_slug": "sher-shah-suri-tomb",
        "district": "Rohtas",
        "category": "Indo-Islamic Heritage",
        "tagline": "Admire the 122-foot red sandstone dome rising from the center of a square reflective artificial lake.",
        "sphere_image_url": "/static/images/panoramas/sasaram_tomb_360.webp",
        "thumbnail_url": "/static/images/panoramas/sasaram_thumb.webp",
        "resolution": "8K UHD",
        "capture_altitude_meters": 8,
        "coordinates": {"lat": 24.9542, "lng": 84.0294},
        "audio_narration_available": True,
        "audio_language_codes": ["en", "hi", "ur"],
        "hotspots": [
            {
                "id": "hs-dome-summit",
                "pitch": 40.0,
                "yaw": 0.0,
                "title": "Octagonal Sandstone Dome",
                "description": "Engineered by architect Mir Muhammad Aliwal Khan, spanning larger than the dome of the Taj Mahal."
            },
            {
                "id": "hs-bridge-causeway",
                "pitch": -10.0,
                "yaw": 180.0,
                "title": "Stepped Causeway Bridge",
                "description": "Connecting the northern gateway to the island plinth surrounded by calm waters."
            }
        ]
    }
]

def get_all_panoramas():
    """Return all available 360 virtual panoramas."""
    return VIRTUAL_PANORAMAS_DB

def get_panorama_by_slug(slug):
    """Find a panorama by its slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for p in VIRTUAL_PANORAMAS_DB:
        if p["slug"] == s or p["id"] == s or p["place_slug"] == s:
            return p
    return None

def get_panorama_by_id(pano_id):
    """Find a panorama by its unique ID."""
    if not pano_id:
        return None
    for p in VIRTUAL_PANORAMAS_DB:
        if p["id"] == pano_id:
            return p
    return None

def get_panoramas_by_district(district):
    """Filter panoramas by district name."""
    if not district or district.lower() == 'all':
        return VIRTUAL_PANORAMAS_DB
    d_clean = district.lower().strip()
    return [p for p in VIRTUAL_PANORAMAS_DB if d_clean in p["district"].lower()]

def get_panoramas_by_category(category):
    """Filter panoramas by category theme."""
    if not category or category.lower() == 'all':
        return VIRTUAL_PANORAMAS_DB
    c_clean = category.lower().strip()
    return [p for p in VIRTUAL_PANORAMAS_DB if c_clean in p["category"].lower()]

def get_panorama_hotspots(slug):
    """Retrieve all coordinate hotspots for a given panorama."""
    p = get_panorama_by_slug(slug)
    return p.get("hotspots", []) if p else []