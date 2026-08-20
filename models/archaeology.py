"""
Bihar Archaeology, Inscriptions & Epigraphy Heritage Model
Catalog of ancient excavation sites, Ashokan pillars, Brahmi rock edicts,
Pala period bronze hoards, and prehistoric Neolithic settlements.
"""

ARCHAEOLOGICAL_SITES_DB = [
    {
        "id": "arch-lauriya-nandangarh",
        "slug": "lauriya-nandangarh-ashokan-pillar",
        "title": "Lauriya Nandangarh Ashokan Pillar & Stupa Mounds",
        "district": "West Champaran",
        "period": "Mauryan Era (3rd Century BCE)",
        "ruler": "Emperor Ashoka",
        "script": "Brahmi Script (Prakrit Language)",
        "category": "Ashokan Monolithic Pillar & Royal Edict",
        "coordinates": {"lat": 26.9950, "lng": 84.4120},
        "description": "A single piece of polished Chunar sandstone standing 32 feet high, crowned by a majestic single lion capital. Features six distinct Major Pillar Edicts of Emperor Ashoka inscribed in pristine Brahmi characters.",
        "excavation_highlights": [
            "Colossal Vedic royal burial mounds dating between 1000 BCE and 600 BCE",
            "Gold leaf embossed with Goddess of the Earth figure",
            "Punch-marked Mauryan silver coins and punch-marked terracotta plaques"
        ],
        "museum_preservation": "ASI Protected National Monument & In-situ Site",
        "visiting_hours": "Sunrise to Sunset (Free Entry)"
    },
    {
        "id": "arch-rampurva-capitals",
        "slug": "rampurva-ashokan-capitals",
        "title": "Rampurva Ashokan Pillars (Bull & Lion Capitals)",
        "district": "West Champaran",
        "period": "Mauryan Era (c. 250 BCE)",
        "ruler": "Emperor Ashoka",
        "script": "Brahmi Script",
        "category": "Ashokan Monoliths & Sculptural Marvels",
        "coordinates": {"lat": 27.2700, "lng": 84.5000},
        "description": "Twin Ashokan pillars excavated in the Tarai plains. The famous Rampurva Bull capital (now housed at the Rashtrapati Bhavan, New Delhi) is universally acclaimed as the pinnacle of ancient Indian animal realism.",
        "excavation_highlights": [
            "Remarkable zebu bull capital showcasing muscular anatomy and lustrous Mauryan polish",
            "Lion capital pillar with intact Ashokan pillar edicts",
            "Ancient royal highway alignment between Pataliputra and Nepal valley"
        ],
        "museum_preservation": "Rashtrapati Bhavan / Indian Museum Kolkata / In-situ Rampurva",
        "visiting_hours": "09:00 AM - 05:00 PM"
    },
    {
        "id": "arch-kolhua-pillar",
        "slug": "kolhua-vaishali-lion-pillar",
        "title": "Kolhua Ashokan Lion Pillar & Kutagarasala Vihara",
        "district": "Vaishali",
        "period": "Mauryan to Gupta Period",
        "ruler": "Emperor Ashoka",
        "script": "Prakrit in Brahmi",
        "category": "Intact Monolithic Pillar & Monastic Complex",
        "coordinates": {"lat": 25.9967, "lng": 85.1225},
        "description": "The only completely intact Ashokan pillar in India with its original lion capital still in place facing north toward Buddha's last journey. Adjacent to the sacred Markata-hrada (Monkey Tank) and brick stupas.",
        "excavation_highlights": [
            "Intact monolithic Chunar polished column without any modern restoration joints",
            "Swastika-shaped early monastic cells and votive stupas",
            "Gupta period inscribed terracotta seals reading 'Vesali-Anusamyana-Takara'"
        ],
        "museum_preservation": "Vaishali Archaeological Museum & ASI Site",
        "visiting_hours": "08:00 AM - 06:00 PM"
    },
    {
        "id": "arch-kurkihar-bronzes",
        "slug": "kurkihar-bronze-hoard-site",
        "title": "Kurkihar Ancient Bronze Sculpture Hoard",
        "district": "Gaya",
        "period": "Pala Empire (9th - 12th Century CE)",
        "ruler": "Devapala & Mahipala I",
        "script": "Siddhamatrika / Proto-Bengali-Maithili",
        "category": "Lost-Wax Bronze Sculpture Hoard",
        "coordinates": {"lat": 24.9120, "lng": 85.2530},
        "description": "In 1930, 226 exquisite gilt-bronze, silver-inlaid Buddhist statues were unearthed from a buried monastery mound in Kurkihar, establishing the global benchmark for the Pala school of metallurgical art.",
        "excavation_highlights": [
            "226 cast bronze icons of Avalokiteshvara, Manjushri, Tara, and crowned Buddhas",
            "Inscribed donor names from Java, Sumatra, and Kashmir indicating international pilgrim patronage",
            "Lost-wax (cire-perdue) casting with silver eyes and jewel-inlaid ushnishas"
        ],
        "museum_preservation": "Patna Museum & Bihar Museum Kurkihar Gallery",
        "visiting_hours": "10:00 AM - 05:00 PM (Closed Mondays)"
    },
    {
        "id": "arch-telhara-monastery",
        "slug": "telhara-monastic-excavations",
        "title": "Telhara Ancient Monastic University Excavations",
        "district": "Nalanda",
        "period": "Kushan to Pala Era (1st - 11th Century CE)",
        "ruler": "Kanishka to Pala Kings",
        "script": "Brahmi, Gupta Brahmi, Nagari",
        "category": "Multistoried University Monastery & Buried Libraries",
        "coordinates": {"lat": 25.1430, "lng": 85.2280},
        "description": "Mentioned by Chinese pilgrim Hiuen Tsang as 'Tilodaka'. Excavations by the Bihar State Archaeology Department revealed a 3-storied monastic complex older than Nalanda, complete with prayer halls, bronze icons, and sealing hoards.",
        "excavation_highlights": [
            "Over 1,000 intact terracotta seals and sealings",
            "Burnt grain storage bins dating to the Kushan empire",
            "Huge stone pillars and multi-chambered student cells with drainage networks"
        ],
        "museum_preservation": "Telhara On-Site Museum & Nalanda Directorate",
        "visiting_hours": "09:00 AM - 05:00 PM"
    },
    {
        "id": "arch-chirand-neolithic",
        "slug": "chirand-neolithic-settlement",
        "title": "Chirand Ganga-Ghaghara Neolithic Settlement",
        "district": "Saran (Chhapra)",
        "period": "Neolithic to Chalcolithic (2500 BCE - 1000 BCE)",
        "ruler": "Indigenous Riverine Neolithic Cultures",
        "script": "Pre-literate / Petro-incised Bone Art",
        "category": "Prehistoric Bone Tool Industry & Circular Dwellings",
        "coordinates": {"lat": 25.7550, "lng": 84.8250},
        "description": "Situated at the confluence of the Ganga and Ghaghara rivers. One of the richest Neolithic bone-tool archaeological sites in Asia, exhibiting deer antler chisels, polished stone celts, and terracotta figurines.",
        "excavation_highlights": [
            "Hundreds of antler bone needles, harpoons, drills, and spearheads",
            "Circular mud-reed huts with plastered floors and microlithic blades",
            "Semi-precious stone bead workshops (chalcedony, agate, jasper)"
        ],
        "museum_preservation": "Patna Museum Prehistoric Gallery & Saran Heritage Cell",
        "visiting_hours": "Sunrise to Sunset"
    }
]

EPIGRAPHY_CHRONOLOGY = [
    {
        "era": "Prehistoric & Neolithic",
        "dates": "2500 BCE - 1000 BCE",
        "key_sites": ["Chirand", "Chechar", "Taradih", "Senuwar"],
        "primary_scripts": "Pictographic / Bone Engravings",
        "overview": "Earliest riverine agricultural settlements and bone metallurgy across the Gangetic plains."
    },
    {
        "era": "Mauryan & Sunga Imperial",
        "dates": "4th Century BCE - 1st Century BCE",
        "key_sites": ["Pataliputra Kumhrar", "Lauriya Nandangarh", "Rampurva", "Kolhua Vaishali", "Barabar Caves"],
        "primary_scripts": "Ashokan Brahmi & Kharosthi",
        "overview": "Monumental stone carving, lustrous polish, and royal edicts promoting Dhamma and civic welfare."
    },
    {
        "era": "Gupta & Post-Gupta Golden Age",
        "dates": "4th Century CE - 7th Century CE",
        "key_sites": ["Nalanda Mahavihara", "Sultanganj", "Mundeshwari Temple", "Aphsad"],
        "primary_scripts": "Late Brahmi / Gupta Brahmi / Sanskrit",
        "overview": "Classical temple architecture, astronomical observatories, and colossal copper/stone sculptures."
    },
    {
        "era": "Pala & Sena Renaissance",
        "dates": "8th Century CE - 12th Century CE",
        "key_sites": ["Kurkihar", "Vikramshila", "Telhara", "Odantapuri", "Antichak"],
        "primary_scripts": "Gaudiya / Siddhamatrika / Proto-Maithili",
        "overview": "Flourishing Mahayana-Vajrayana Buddhist art, bronze lost-wax casting, and palm-leaf manuscript illustration."
    }
]

def get_all_archaeological_sites():
    """Return all cataloged ancient excavation and epigraphical sites."""
    return ARCHAEOLOGICAL_SITES_DB

def get_site_by_slug(slug):
    """Retrieve site details by slug or identifier."""
    if not slug:
        return None
    s = slug.lower().strip()
    for site in ARCHAEOLOGICAL_SITES_DB:
        if site["slug"] == s or site["id"] == s:
            return site
    return None

def get_sites_by_district(district):
    """Filter archaeological sites by district."""
    if not district or district.lower() == 'all':
        return ARCHAEOLOGICAL_SITES_DB
    d_clean = district.lower().strip()
    return [site for site in ARCHAEOLOGICAL_SITES_DB if d_clean in site["district"].lower()]

def get_sites_by_period(period):
    """Filter sites by historical era (e.g. Mauryan, Pala, Neolithic)."""
    if not period or period.lower() == 'all':
        return ARCHAEOLOGICAL_SITES_DB
    p_clean = period.lower().strip()
    return [site for site in ARCHAEOLOGICAL_SITES_DB if p_clean in site["period"].lower()]

def get_ashokan_edicts():
    """Retrieve only Ashokan pillars and royal edict sites."""
    return [site for site in ARCHAEOLOGICAL_SITES_DB if "ashoka" in site.get("ruler", "").lower() or "ashoka" in site.get("title", "").lower()]

def get_epigraphy_chronology():
    """Return epigraphical and archaeological era timeline."""
    return EPIGRAPHY_CHRONOLOGY

NUMISMATIC_HOARDS_DB = [
    {
        "id": "coin-pataliputra-punch-marked",
        "slug": "pataliputra-silver-punch-marked-hoard",
        "name": "Pataliputra Mauryan Imperial Silver Karshapana Hoard",
        "period": "Mauryan Empire (4th - 3rd Century BCE)",
        "metal": "Silver (90% Purity)",
        "weight_standard": "32 Ratti / 3.4 Grams",
        "mint_location": "Pataliputra Royal Mint",
        "symbols": ["Sun (Surya)", "Six-armed symbol (Shadara Chakra)", "Hill with crescent", "Elephant", "Bull"],
        "historical_context": "The standard imperial legal tender of ancient India under Chandragupta Maurya and Ashoka, accepted from Taxila to Bengal.",
        "museum": "Patna Museum Coin Vault & Reserve Collection"
    },
    {
        "id": "coin-gupta-gold-dinars",
        "slug": "kumhrar-gupta-gold-dinar-hoard",
        "name": "Gupta Archer & Ashvamedha Gold Dinar Hoard",
        "period": "Gupta Empire (4th - 5th Century CE)",
        "metal": "Gold (High Purity)",
        "weight_standard": "Dinar / Suvarna Standard (7.8 - 9.2 Grams)",
        "mint_location": "Imperial Pataliputra & Magadha Mints",
        "symbols": ["King as Archer holding bow", "Garuda standard", "Queen Dattadevi", "Goddess Lakshmi on lotus"],
        "historical_context": "Issued by Samudragupta and Chandragupta II 'Vikramaditya'. Celebrated worldwide as the artistic zenith of classical Indian numismatic engraving.",
        "museum": "Bihar Museum Numismatic Gallery"
    },
    {
        "id": "coin-buxar-terracotta-seals",
        "slug": "buxar-charitravan-terracotta-hoard",
        "name": "Buxar & Charitravan Archaic Terracotta Art & Seal Hoard",
        "period": "Mauryan to Sunga Period (3rd - 1st Century BCE)",
        "metal": "Terracotta & Baked Clay",
        "weight_standard": "N/A (Figurine Plaques & Merchant Guild Tokens)",
        "mint_location": "Ancient Karusha Guild Workshops (Buxar)",
        "symbols": ["Elaborate coiffure Mother Goddess", "Dancing maiden with heavy armlets", "Nigama guild inscriptions"],
        "historical_context": "Unearthed on the banks of the Ganges in Buxar, famous for distinct serpentine hairdos, applique jewelry, and maritime trading guild marks.",
        "museum": "Buxar Heritage Gallery & Patna Museum"
    }
]

def get_all_numismatic_hoards():
    """Return all cataloged ancient coin hoards and terracotta guild tokens."""
    return NUMISMATIC_HOARDS_DB

def get_coin_hoard_by_slug(slug):
    """Retrieve coin hoard by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for c in NUMISMATIC_HOARDS_DB:
        if c["slug"] == s or c["id"] == s:
            return c
    return None

EPIGRAPHICAL_INSCRIPTIONS_DB = [
    {
        "id": "ins-ashoka-mre-sahasram",
        "slug": "ashoka-sahasram-minor-rock-edict",
        "title": "Emperor Ashoka Sahasram Minor Rock Edict",
        "location": "Chandan Shahid Hill, Sasaram, Rohtas",
        "script": "Ashokan Brahmi",
        "language": "Magadhi Prakrit",
        "date_issued": "c. 256 BCE",
        "original_prakrit_excerpt": "Devanam piyasa piyadasino hevam aha...",
        "english_translation": "Thus says the Beloved of the Gods: For more than two and a half years I was a lay follower... Let small and great exert themselves in righteousness (Dhamma).",
        "thematic_significance": "Proclaims individual spiritual effort and universal moral ethical striving without sectarian discrimination."
    },
    {
        "id": "ins-devapala-nalanda-copperplate",
        "slug": "devapala-nalanda-copper-plate-charter",
        "location": "Nalanda Monastery Site No. 1",
        "title": "Devapala Nalanda International Copper-Plate Charter",
        "script": "Siddhamatrika (Proto-Bengali-Maithili)",
        "language": "Classical Sanskrit",
        "date_issued": "c. 860 CE (Regnal Year 39 of King Devapala)",
        "original_prakrit_excerpt": "Sri Suvarnadvipadhipa Maharaja Balaputradevena...",
        "english_translation": "King Balaputradeva of Suvarnadvipa (Sumatra/Indonesia) constructed a monastery at Nalanda. At his request, King Devapala of Magadha grants five revenue villages for its upkeep and copyists of sacred texts.",
        "thematic_significance": "Concrete epigraphical evidence of ancient maritime educational diplomacy between Bihar and Southeast Asia."
    },
    {
        "id": "ins-mundeshwari-brahmi",
        "slug": "mundeshwari-temple-inscription",
        "location": "Mundeshwari Hill, Kaimur",
        "title": "Mundeshwari Temple Brahmi Royal Dedication Slab",
        "script": "Early Gupta Brahmi",
        "language": "Sanskrit Verse",
        "date_issued": "c. 635 CE (Harsha Era 30)",
        "original_prakrit_excerpt": "Samvat 30 Karttika Sukla Dvitayayam...",
        "english_translation": "Records the establishment of the shrine of Viniteshvara and Mandaleshvara by General Gomibhata during the reign of Maharaja Udayasena.",
        "thematic_significance": "Establishes Mundeshwari as one of the oldest continuously functioning Hindu temple sanctums in India."
    }
]

def get_all_epigraphical_inscriptions():
    """Return all cataloged ancient royal stone and copper-plate inscriptions."""
    return EPIGRAPHICAL_INSCRIPTIONS_DB

def get_inscription_by_slug(slug):
    """Retrieve inscription details by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for ins in EPIGRAPHICAL_INSCRIPTIONS_DB:
        if ins["slug"] == s or ins["id"] == s:
            return ins
    return None