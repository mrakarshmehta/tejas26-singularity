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

def get_all_guides():
    """Return all verified licensed tourist guides."""
    return VERIFIED_GUIDES_DB

def get_guide_by_slug(slug):
    """Retrieve guide profile by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for g in VERIFIED_GUIDES_DB:
        if g["slug"] == s or g["id"] == s:
            return g
    return None

def get_guides_by_district(district):
    """Filter guides by base district."""
    if not district or district.lower() == 'all':
        return VERIFIED_GUIDES_DB
    d_clean = district.lower().strip()
    return [g for g in VERIFIED_GUIDES_DB if d_clean in g["district"].lower()]

def get_guides_by_language(language):
    """Filter guides speaking a particular language."""
    if not language or language.lower() == 'all':
        return VERIFIED_GUIDES_DB
    l_clean = language.lower().strip()
    return [g for g in VERIFIED_GUIDES_DB if any(l_clean in lang.lower() for lang in g.get("languages", []))]

def get_guides_by_specialization(spec):
    """Filter guides by thematic specialization (e.g. Buddhist, Wildlife)."""
    if not spec or spec.lower() == 'all':
        return VERIFIED_GUIDES_DB
    s_clean = spec.lower().strip()
    return [g for g in VERIFIED_GUIDES_DB if any(s_clean in sp.lower() for sp in g.get("specializations", []))]

def validate_guide_inquiry(traveler_name, email, phone, guide_slug, travel_date, group_size=1):
    """Validate tourist guide booking inquiry parameters."""
    if not traveler_name or len(traveler_name.strip()) < 3:
        return False, "Please enter your full name (minimum 3 characters)."
    if not email or '@' not in email or '.' not in email:
        return False, "Please provide a valid email address."
    if not phone or len(phone.strip()) < 8:
        return False, "Please provide a valid contact number."
    if not guide_slug or not get_guide_by_slug(guide_slug):
        return False, f"Invalid or non-existent guide selected: {guide_slug}"
    if not travel_date:
        return False, "Please specify your planned travel date."
    try:
        size = int(group_size)
        if size < 1 or size > 50:
            return False, "Group size must be between 1 and 50 persons."
    except (ValueError, TypeError):
        return False, "Invalid group size specified."

    return True, "Booking inquiry successfully validated."

GUIDE_ETHICS_STANDARDS = [
    {
        "standard_title": "ASI & Ministry Licensing Compliance",
        "description": "All listed guides hold active photographic identity licenses issued by the Archaeological Survey of India (ASI) or Bihar Tourism."
    },
    {
        "standard_title": "Transparent Tariffs & Zero Shopping Commission Steering",
        "description": "Guides are strictly bound to daily fixed fees with a pledge against steering tourists into inflated commission-based souvenir shops."
    },
    {
        "standard_title": "First-Aid & Emergency CPR Certification",
        "description": "Trained in wilderness first-aid, heat exhaustion protocols, and direct integration with Bihar 112 emergency trauma services."
    },
    {
        "standard_title": "Safe & Respectful Solo / Women Traveler Protocols",
        "description": "Adheres to international solo traveler dignity guidelines, respectful cultural photography etiquette, and local community customs."
    }
]

def get_guide_ethics_standards():
    """Return verified guide code of ethics and traveler safety standards."""
    return GUIDE_ETHICS_STANDARDS

def verify_guide_license(license_no):
    """Verify validity and status of guide license number."""
    if not license_no:
        return False, "License number is required."
    l_clean = license_no.strip().upper()
    for g in VERIFIED_GUIDES_DB:
        if g.get("license_number", "").upper() == l_clean:
            return True, {
                "valid": True,
                "guide_name": g["name"],
                "tier": g["license_tier"],
                "district": g["district"],
                "experience_years": g["experience_years"]
            }
    return False, "License number not found in verified official registry."