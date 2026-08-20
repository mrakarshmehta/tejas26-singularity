"""
Verified Local Heritage Tour Guides & Storytellers Model
Provides licensed tourist guides, multilingual proficiencies,
specialization badges (Buddhist, Archaeology, Wildlife, Art), and inquiry booking validation.
"""

VERIFIED_GUIDES_DB = [
    {
        "id": "guide-bodhgaya-dharmapala",
        "slug": "ven-dharmapala-bodh-gaya",
        "name": "Ven. Tenzin Dharmapala",
        "district": "Gaya",
        "base_city": "Bodh Gaya",
        "license_number": "ASI-BR-GY-2018-044",
        "license_tier": "State Certified Senior Heritage Guide",
        "experience_years": 14,
        "languages": ["English", "Hindi", "Tibetan", "Chinese (Mandarin)"],
        "specializations": ["Buddhist Philosophy & Monastic History", "Mahabodhi Tree Meditation Walks", "Ancient Inscriptions"],
        "daily_rate_inr": 2200,
        "rating": 4.96,
        "review_count": 184,
        "bio": "Monastic historian who has guided scholars from across 35 countries through the sacred precincts of Mahabodhi Temple, Dungeshwari Cave, and Sujata Kuti.",
        "avatar_icon": "🧘"
    },
    {
        "id": "guide-nalanda-dr-mishra",
        "slug": "dr-alok-mishra-nalanda-rajgir",
        "name": "Dr. Alok Kumar Mishra",
        "district": "Nalanda",
        "base_city": "Rajgir & Nalanda",
        "license_number": "ASI-BR-NL-2015-012",
        "license_tier": "Ministry of Tourism Certified Regional Guide",
        "experience_years": 18,
        "languages": ["English", "Hindi", "Sanskrit", "Japanese"],
        "specializations": ["Nalanda Mahavihara Archaeology", "Vishwa Shanti Stupa History", "Rajgir Cycling Heritage Trails"],
        "daily_rate_inr": 2500,
        "rating": 4.98,
        "review_count": 240,
        "bio": "Archaeologist with a doctorate on Nalanda terracotta sealings. Specializes in decoding ancient monastic architectural layouts for cultural travelers.",
        "avatar_icon": "📜"
    },
    {
        "id": "guide-mithila-sunita-devi",
        "slug": "sunita-devi-mithila-folk-art",
        "name": "Sunita Devi Jha",
        "district": "Madhubani",
        "base_city": "Jitwarpur & Madhubani",
        "license_number": "BHTD-MD-2020-089",
        "license_tier": "State Certified Cultural Storyteller",
        "experience_years": 10,
        "languages": ["Maithili", "Hindi", "English"],
        "specializations": ["Madhubani Painting Guild Walks", "Village Immersion & Organic Farming", "Aripan Floor Art Workshops"],
        "daily_rate_inr": 1800,
        "rating": 4.92,
        "review_count": 112,
        "bio": "Born into a lineage of national award-winning Mithila painters. Conducts village heritage walks explaining indigenous pigments and folk symbolism.",
        "avatar_icon": "🎨"
    },
    {
        "id": "guide-valmiki-ramesh-tharu",
        "slug": "ramesh-tharu-valmiki-safari",
        "name": "Ramesh Kumar Tharu",
        "district": "West Champaran",
        "base_city": "Valmiki Nagar",
        "license_number": "VTR-FD-2019-021",
        "license_tier": "Forest Department Certified Wildlife Naturalist",
        "experience_years": 12,
        "languages": ["Bhojpuri", "Hindi", "Basic English"],
        "specializations": ["Tiger Tracking & Pugmark Identification", "Birdwatching Expeditions", "Gandak River Boat Ecology"],
        "daily_rate_inr": 1600,
        "rating": 4.95,
        "review_count": 98,
        "bio": "Indigenous Tharu forest tracker with deep ancestral knowledge of the Sal jungle canopy, animal call interpretations, and herbal medicinal plants.",
        "avatar_icon": "🐅"
    },
    {
        "id": "guide-patna-simran-singh",
        "slug": "simran-singh-patna-heritage",
        "name": "Simranjeet Singh",
        "district": "Patna",
        "base_city": "Patna City",
        "license_number": "BHTD-PT-2017-033",
        "license_tier": "Regional Heritage Guide",
        "experience_years": 9,
        "languages": ["English", "Hindi", "Punjabi", "Urdu"],
        "specializations": ["Takht Sri Patna Sahib Sacred Walks", "Mauryan Pataliputra Ruins", "Ganga Heritage Ghats & Food Walks"],
        "daily_rate_inr": 2000,
        "rating": 4.94,
        "review_count": 145,
        "bio": "Old Patna native who brings the rich cosmopolitan history of ancient Pataliputra, Mughal Azimabad, and Sikh spiritual roots to life.",
        "avatar_icon": "🏛️"
    }
]