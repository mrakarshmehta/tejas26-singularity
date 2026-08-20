"""
HiddenYatra — Cultural Festivals & Seasonal Celebrations Model
Provides structured data for Bihar's vibrant folk festivals, heritage fairs, and sacred rituals.
"""

BIHAR_FESTIVALS = [
    {
        "id": 1,
        "slug": "chhath-puja",
        "name": "Chhath Puja (Maha Parv)",
        "month_name": "October / November",
        "month_num": 10,
        "duration_days": 4,
        "region": "Pan-Bihar (Ganges Ghats)",
        "primary_districts": ["Patna", "Bhagalpur", "Gaya", "Munger", "Muzaffarpur"],
        "icon": "☀️",
        "category": "Folk & Solar Worship",
        "significance": "The supreme festival of Bihar dedicated to the Sun God (Surya) and Chhathi Maiya. Renowned for its purity, austerity, river ghat arghya offerings at sunrise and sunset, and Thekua prasad.",
        "visitor_tips": "Best viewed at sunrise from the sacred ghats of Patna or Munger. Respect fasting traditions and ritual sanctity."
    },
    {
        "id": 2,
        "slug": "sonpur-mela",
        "name": "Sonepur Cattle & Cultural Fair",
        "month_name": "November / December",
        "month_num": 11,
        "duration_days": 30,
        "region": "Saran / Vaishali (Gandak & Ganga confluence)",
        "primary_districts": ["Saran", "Vaishali"],
        "icon": "🐘",
        "category": "Heritage Fair",
        "significance": "Asia's largest historic cattle fair, held on Kartik Purnima. Steeped in antiquity, dating back to Chandragupta Maurya and the Gajendramoksha legend at Hariharnath Temple.",
        "visitor_tips": "Visit during the first two weeks for vibrant folk theater, horse and cattle exhibits, and carnival atmosphere."
    },
    {
        "id": 3,
        "slug": "rajgir-mahotsav",
        "name": "Rajgir Mahotsav & Dance Festival",
        "month_name": "December",
        "month_num": 12,
        "duration_days": 3,
        "region": "Nalanda (Rajgir)",
        "primary_districts": ["Nalanda"],
        "icon": "🎭",
        "category": "Cultural & Performing Arts",
        "significance": "A premier cultural extravaganza held at the ancient capital of Magadha featuring classical Indian dancers, folk musicians, craft bazaars, and heritage walks.",
        "visitor_tips": "Evening dance recitals set against the Rajgir hill backdrop are spectacular. Combine with hot springs visit."
    },
    {
        "id": 4,
        "slug": "sama-chakeva",
        "name": "Sama Chakeva (Mithila Folk Festival)",
        "month_name": "November",
        "month_num": 11,
        "duration_days": 8,
        "region": "Mithila Region",
        "primary_districts": ["Madhubani", "Darbhanga", "Sitamarhi", "Samastipur"],
        "icon": "🕊️",
        "category": "Folk Tradition",
        "significance": "Celebrates the bond between brothers and sisters in Mithila with clay idols of migratory birds, night folk songs, and farewell immersion rituals.",
        "visitor_tips": "Experience in rural Madhubani villages where women craft handmade clay bird idols."
    },
    {
        "id": 5,
        "slug": "buddha-jayanti-bodh-gaya",
        "name": "Buddha Jayanti & Vesak Global Gathering",
        "month_name": "May",
        "month_num": 5,
        "duration_days": 3,
        "region": "Bodh Gaya",
        "primary_districts": ["Gaya"],
        "icon": "🪔",
        "category": "International Spiritual Gathering",
        "significance": "Commemorates Buddha's birth, enlightenment, and Mahaparinirvana with grand international processions of monks from Japan, Thailand, Sri Lanka, Myanmar, and Tibet.",
        "visitor_tips": "Witness the evening butter lamp illumination ceremony around the sacred Bodhi Tree."
    },
    {
        "id": 6,
        "slug": "shravani-mela-sultanganj",
        "name": "Shravani Mela (Kanwar Yatra Sultanganj)",
        "month_name": "July / August",
        "month_num": 7,
        "duration_days": 30,
        "region": "Bhagalpur to Deoghar Route",
        "primary_districts": ["Bhagalpur", "Banka"],
        "icon": "🌊",
        "category": "Sacred Pilgrimage",
        "significance": "Millions of saffron-clad Kanwariyas collect holy Uttarvahini Ganga water from Sultanganj and undertake a 105 km barefoot trek chanting Bol Bam.",
        "visitor_tips": "Remarkable spiritual spectacle of collective devotion and faith."
    }
]


def get_all_festivals():
    """Return all cultural festivals in the database."""
    return BIHAR_FESTIVALS


def get_festival_by_slug(slug):
    """Retrieve festival details by its unique slug."""
    if not slug:
        return None
    slug_clean = slug.strip().lower()
    for f in BIHAR_FESTIVALS:
        if f['slug'] == slug_clean:
            return f
    return None
