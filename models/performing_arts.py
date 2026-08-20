"""
Bihar Folk Performing Arts, Theater & Musical Traditions Model
Catalog of indigenous theatrical genres, classical folk song forms,
traditional musical instruments, and verified cultural performer guilds.
"""

PERFORMING_ARTS_DB = [
    {
        "id": "art-bidesiya-theater",
        "slug": "bidesiya-folk-theater",
        "title": "Bidesiya Folk Theater (Bhikhari Thakur Legacy)",
        "region": "Bhojpur, Saran, Siwan, Patna",
        "category": "Folk Drama & Social Theater",
        "creator": "Bhikhari Thakur ('Shakespeare of Bhojpuri')",
        "instruments": ["Dholak", "Harmonium", "Jhal / Manjira", "Kartal"],
        "icon": "🎭",
        "summary": "The definitive folk theater form of Bihar combining poignant songs, satirical wit, and socio-economic critique.",
        "description": "Created in the early 20th century by legendary playwright Bhikhari Thakur. Bidesiya captures the emotional anguish of rural women left behind in Bihar villages as their husbands migrated to Calcutta, Rangoon, and Assam for labor.",
        "cultural_backstory": "Performed overnight under open skies with male actors playing all roles (Launda Naach). Uses colloquial Bhojpuri verses that sparked major social reform movements across northern India.",
        "key_themes": ["Migration and Longing (Viraha)", "Caste Reform", "Women's Empowerment", "Anti-Dowry & Social Ethics"]
    },
    {
        "id": "art-chhau-mask-dance",
        "slug": "manbhum-chhau-dance",
        "title": "Chhau Martial Mask Dance",
        "region": "Seraikela & Chota Nagpur Border",
        "category": "Martial Folk Dance & UNESCO Intangible Heritage",
        "creator": "Ancient Tribal & Royal Guilds",
        "instruments": ["Dhamsa (War Kettle Drum)", "Dhol", "Shehnai", "Mohuri"],
        "icon": "👺",
        "summary": "Acrobatic martial dance enacting episodes from the Ramayana, Mahabharata, and indigenous tribal legends.",
        "description": "Performers don stylized clay and papier-mâché masks representing gods, demons, lions, and peacocks. Characterized by thunderous war-drum rhythms, dynamic athletic leaps, and mock sword combat.",
        "cultural_backstory": "Historically patronized by kings as martial fitness training for warriors during the springtime Chaitra Parva festival.",
        "key_themes": ["Triumph of Righteousness", "Martial Valour", "Nature & Forest Totems"]
    },
    {
        "id": "art-domkach-women-dance",
        "slug": "domkach-wedding-theater",
        "title": "Domkach Intimate Wedding Theater & Dance",
        "region": "Mithila, Magadha & Bhojpur (All Bihar)",
        "category": "Celebratory Women's Folk Theater",
        "creator": "Rural Female Collectives",
        "instruments": ["Dholak", "Thali (Brass Plate)", "Bansuri"],
        "icon": "💃",
        "summary": "Humorous midnight satire, singing, and rhythmic circle dance performed exclusively by women.",
        "description": "Enacted inside the bridegroom's house by female relatives throughout the night after the men depart for the wedding procession (Baraat). Protects the house from evil spirits through laughter and theatrical parody.",
        "cultural_backstory": "Features witty improvised dialogues, cross-dressing impersonations, and playful riddles that foster female solidarity and joyous release.",
        "key_themes": ["Domestic Satire", "Mother-in-law & Daughter-in-law Wit", "Festive Protection"]
    },
    {
        "id": "art-kajari-monsoon-song",
        "slug": "bihari-kajari-monsoon-songs",
        "title": "Kajari & Jhumar Monsoon Melodies",
        "region": "Bhojpur, Buxar, Rohtas",
        "category": "Semi-Classical Seasonal Folk Music",
        "creator": "Ancient Gangetic Troubadours",
        "instruments": ["Sarangi", "Dholak", "Kartal", "Flute"],
        "icon": "🌧️",
        "summary": "Soulful seasonal ballads greeting the arrival of dark rain clouds and dancing peacocks.",
        "description": "Sung during the holy monsoon month of Shravana on swings under village mango groves. Blends classical ragas (Des, Megh, Pilu) with rustic Bhojpuri verses expressing Radha-Krishna romance and longing.",
        "cultural_backstory": "Kajari is celebrated in both rural village gatherings and classical Hindustani concerts, praised for its undulating vocal microtones imitating falling raindrops.",
        "key_themes": ["Monsoon Rains", "Swings under Kadamba Trees", "Romantic Longing"]
    },
    {
        "id": "art-sohar-birth-chants",
        "slug": "mithila-sohar-childbirth-chants",
        "title": "Mithila & Magahi Sohar Ceremonial Chants",
        "region": "Mithila (Darbhanga, Madhubani) & Magadha",
        "category": "Sacred Rite-of-Passage Song",
        "creator": "Maithil Matriarchs",
        "instruments": ["Dholak", "Kashtha Tarang", "Kartal"],
        "icon": "👶",
        "summary": "Sacred celebratory blessing chants sung upon the birth of a child in the household.",
        "description": "Sung during the Chhathi and Namakarana (naming ceremony) rituals. Draws lyrical parallels between the newborn baby and the cosmic birth of Lord Rama in Ayodhya or Lord Krishna in Gokul.",
        "cultural_backstory": "Composed in sweet Maithili and Magahi idioms, passed down orally across fifty generations of women bards.",
        "key_themes": ["Divine Blessings", "Maternal Joy", "Lineage Continuity"]
    }
]

FOLK_INSTRUMENTS_DB = [
    {
        "name": "Dholak",
        "category": "Membranophone (Double-Headed Hand Drum)",
        "materials": "Sheesham or Mango wood shell, goat skin heads",
        "role": "The rhythmic heartbeat of Bihar folk music, wedding songs, and Chhath geet."
    },
    {
        "name": "Dhamsa",
        "category": "Membranophone (War Kettle Drum)",
        "materials": "Riveted iron bowl, heavy buffalo hide",
        "role": "Produces thunderous low-frequency pulses during Chhau martial dance leaps."
    },
    {
        "name": "Shehnai",
        "category": "Aerophone (Double-Reed Oboe)",
        "materials": "Marwar wood body, brass flare, reed mouth",
        "role": "Immortalized by Bharat Ratna Ustad Bismillah Khan of Dumraon, Bihar; central to temple rituals and marriages."
    },
    {
        "name": "Kartal & Jhal",
        "category": "Idiophone (Brass Clappers / Cymbals)",
        "materials": "Bell metal / Bell brass",
        "role": "Provides high-frequency syncopated claps in devotional Bhajans and Bidesiya theater."
    }
]

def get_all_performing_arts():
    """Return all cataloged folk theater, dance, and music forms."""
    return PERFORMING_ARTS_DB

def get_art_by_slug(slug):
    """Retrieve performing art by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for art in PERFORMING_ARTS_DB:
        if art["slug"] == s or art["id"] == s:
            return art
    return None

def get_arts_by_region(region):
    """Filter performing arts by cultural region (e.g. Mithila, Bhojpur, Magadha)."""
    if not region or region.lower() == 'all':
        return PERFORMING_ARTS_DB
    r_clean = region.lower().strip()
    return [a for a in PERFORMING_ARTS_DB if r_clean in a["region"].lower() or "all bihar" in a["region"].lower()]

def get_all_folk_instruments():
    """Return catalog of traditional Bihar musical instruments."""
    return FOLK_INSTRUMENTS_DB

FOLK_ARTIST_GUILDS_DB = [
    {
        "id": "guild-bhikhari-thakur-trust",
        "name": "Bhikhari Thakur Folk Theater Repertory",
        "genre": "Bidesiya & Launda Naach",
        "base_location": "Kutubpur, Saran (Chhapra) & Patna",
        "district": "Saran",
        "lead_exponent": "Jainendra Dost & Senior Folk Artists",
        "performance_season": "Year-round (Peak in Autumn & Winter)",
        "contact_note": "Available for cultural festival performances and rural theater workshops."
    },
    {
        "id": "guild-mithila-sohar-mandali",
        "name": "Mithilanchal Maithili Sangeet Parishad",
        "genre": "Sohar, Samdauni & Batgamani",
        "base_location": "Darbhanga & Madhubani",
        "district": "Madhubani",
        "lead_exponent": "Smt. Sharda Sinha Legacy Guild Artists",
        "performance_season": "Festival occasions (Kojagara, Chhath, Weddings)",
        "contact_note": "Specializes in traditional acoustic Maithili choral harmonies."
    },
    {
        "id": "guild-buxar-kajari-samiti",
        "name": "Bhojpur Kajari & Biraha Gaayan Mandal",
        "genre": "Kajari & Nirgun Spiritual Ballads",
        "base_location": "Buxar & Ara",
        "district": "Buxar",
        "lead_exponent": "Master Kabir Panthi Folk Vocalists",
        "performance_season": "Shravana Monsoon & Makar Sankranti",
        "contact_note": "Performs traditional open-air jhula songs and Kabir nirgun verses."
    }
]

def get_all_folk_guilds():
    """Return verified folk performing artist troupes and cultural repertories."""
    return FOLK_ARTIST_GUILDS_DB

def get_guild_by_id(guild_id):
    """Retrieve artist guild by ID."""
    if not guild_id:
        return None
    g_clean = guild_id.lower().strip()
    for g in FOLK_ARTIST_GUILDS_DB:
        if g["id"] == g_clean or g_clean in g["name"].lower():
            return g
    return None