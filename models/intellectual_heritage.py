"""
Bihar Intellectual Heritage, Ancient Scholars & Monastic Libraries Model
Chronicles the philosophers, astronomers, mathematicians, and grammarians
who shaped global intellectual history from ancient Pataliputra, Nalanda, and Mithila.
"""

ANCIENT_SCHOLARS_DB = [
    {
        "id": "scholar-aryabhata",
        "slug": "aryabhata-astronomer-mathematician",
        "name": "Aryabhata (Master Astronomer & Mathematician)",
        "era": "Classical Gupta Period (c. 476 - 550 CE)",
        "birthplace_connection": "Khagaul ('Astronomical Vault'), Near Pataliputra",
        "primary_treatise": "Aryabhatiya & Arya-siddhanta",
        "field": "Astronomy, Trigonometry, Mathematical Calculus",
        "icon": "🔭",
        "breakthrough_discoveries": [
            "Calculated π (Pi) accurately to 4 decimal places: 3.1416",
            "Discovered the Earth is spherical and rotates daily on its axis",
            "Correctly proved that lunar and solar eclipses are caused by planetary shadows, not mythical demons",
            "Introduced the table of sines (jya) that laid the foundation for modern trigonometry"
        ],
        "biography": "Aryabhata conducted his cosmic sky observations at Khagaul observatory near Pataliputra. At just 23 years old, he composed the revolutionary 121-verse 'Aryabhatiya', fundamentally revolutionizing planetary computation."
    },
    {
        "id": "scholar-chanakya-kautilya",
        "slug": "chanakya-kautilya-statecraft-philosopher",
        "name": "Chanakya (Vishnugupta / Kautilya)",
        "era": "Mauryan Empire (c. 375 - 283 BCE)",
        "birthplace_connection": "Imperial Pataliputra Court & Takshashila",
        "primary_treatise": "Arthashastra & Chanakya Niti",
        "field": "Statecraft, Geopolitics, Economics & Jurisprudence",
        "icon": "📜",
        "breakthrough_discoveries": [
            "Formulated the Saptanga theory of statecraft (Seven Limbs of Sovereign State)",
            "Devised the Mandala geopolitical alliance theory of neighboring states",
            "Pioneered detailed fiscal treasury management, market regulations, and espionage networks"
        ],
        "biography": "Architect of the pan-Indian Mauryan Empire under Chandragupta Maurya. His 'Arthashastra' remains the world's most comprehensive ancient manual on political realism, treasury economics, and civic administration."
    },
    {
        "id": "scholar-shilabhadra-nalanda",
        "slug": "acharya-shilabhadra-nalanda-chancellor",
        "name": "Acharya Shilabhadra (Venerable Nalanda Chancellor)",
        "era": "Harsha Era (c. 529 - 645 CE)",
        "birthplace_connection": "Nalanda Mahavihara",
        "primary_treatise": "Buddhabhumi-sutra Commentary & Yogacara Texts",
        "field": "Buddhist Epistemology, Logic (Pramana) & Monastic Administration",
        "icon": "🏛️",
        "breakthrough_discoveries": [
            "Headed Nalanda Mahavihara with over 10,000 monks and scholars from across Asia",
            "Personal preceptor to Chinese pilgrim Xuanzang (Hiuen Tsang) for five years",
            "Synthesized Yogacara-Vijnanavada consciousness philosophy"
        ],
        "biography": "Celebrated across Tang Dynasty China, Korea, and Tibet as the supreme master of Buddhist logic. When Xuanzang arrived at Nalanda in 637 CE, the 106-year-old Shilabhadra personally transmitted sacred Sanskrit manuscripts to him."
    },
    {
        "id": "scholar-vidyapati-maithil",
        "slug": "mahakavi-vidyapati-maithil-kokil",
        "name": "Mahakavi Vidyapati ('Maithil Kokil')",
        "era": "Oiniwar Dynasty (c. 1352 - 1448 CE)",
        "birthplace_connection": "Bisafi Village, Madhubani, Mithila",
        "primary_treatise": "Padavali, Purusha Pariksha, Kirtilata",
        "field": "Classical Lyric Poetry, Ethics, Sanskrit & Maithili Literature",
        "icon": "🪕",
        "breakthrough_discoveries": [
            "Pioneered vernacular literary expression by composing sublime lyrics in pure Maithili",
            "Created the Vaishnava Radha-Krishna bridal mysticism that inspired Chaitanya Mahaprabhu and Rabindranath Tagore",
            "Composed 'Purusha Pariksha' — an encyclopedic moral fable collection on character ethics"
        ],
        "biography": "Court poet of King Shiva Simha of Mithila. Legend holds that Lord Shiva was so captivated by Vidyapati's devotional verses that He descended to Earth as the servant 'Ugna' to serve the poet."
    }
]

ANCIENT_UNIVERSITIES_DB = [
    {
        "id": "univ-nalanda-mahavihara",
        "slug": "nalanda-monastic-university",
        "name": "Nalanda Mahavihara & Dharmaganja Library",
        "district": "Nalanda",
        "founded_era": "Gupta Empire (5th Century CE by King Kumaragupta I)",
        "peak_capacity": "10,000 monks & students, 2,000 faculty professors",
        "famous_library": "Dharmaganja ('Mart of Religion') housing nine-story library towers: Ratnasagara, Ratnodadhi, and Ratnaranjaka",
        "curriculum": "Grammar, Logic, Medicine, Astronomy, Metaphysics, Sankhya, Mahayana Buddhism",
        "international_alumni": ["Xuanzang (China)", "Yijing (China)", "Padmasambhava (Guru Rinpoche / Tibet)", "Aryadeva (Sri Lanka)"]
    },
    {
        "id": "univ-vikramashila-mahavihara",
        "slug": "vikramashila-tantric-university",
        "name": "Vikramashila Mahavihara",
        "district": "Bhagalpur (Antichak)",
        "founded_era": "Pala Empire (8th Century CE by Emperor Dharmapala)",
        "peak_capacity": "3,000 scholar monks overseen by 6 Gatekeeper Scholars (Dvara-Panditas)",
        "famous_library": "Extensive palm-leaf & birch-bark manuscript repository of Vajrayana tantras",
        "curriculum": "Vajrayana Buddhism, Tantra, Logic, Metaphysics, Lexicography",
        "international_alumni": ["Atisha Dipankara Srijnana (Re-established Buddhism in Tibet)", "Ratnakarashanti", "Abhayakaragupta"]
    },
    {
        "id": "univ-telhara-monastery",
        "slug": "telhara-monastic-complex",
        "name": "Telhara Mahavihara Excavations",
        "district": "Nalanda (Ekangarsarai)",
        "founded_era": "Kushan to Gupta Period (1st Century BCE - 11th Century CE)",
        "peak_capacity": "1,000 resident Mahayana monks",
        "famous_library": "Terracotta seal archive and bronze casting ateliers",
        "curriculum": "Theravada & Mahayana Buddhist doctrine, Sanskrit logic",
        "international_alumni": ["Mentioned extensively in Xuanzang's 7th-century travelogue 'Great Tang Records'"]
    }
]

def get_all_scholars():
    """Return all cataloged ancient scholars and polymaths."""
    return ANCIENT_SCHOLARS_DB

def get_scholar_by_slug(slug):
    """Retrieve scholar profile by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for sch in ANCIENT_SCHOLARS_DB:
        if sch["slug"] == s or sch["id"] == s:
            return sch
    return None

def get_all_ancient_universities():
    """Return catalog of ancient monastic universities and library archives."""
    return ANCIENT_UNIVERSITIES_DB

def get_university_by_slug(slug):
    """Retrieve university archive by slug."""
    if not slug:
        return None
    s = slug.lower().strip()
    for u in ANCIENT_UNIVERSITIES_DB:
        if u["slug"] == s or u["id"] == s:
            return u
    return None

CLASSICAL_TREATISES_DB = [
    {
        "title": "Aryabhatiya",
        "author": "Aryabhata",
        "composed_year": "c. 499 CE",
        "language": "Classical Sanskrit (Sutra Metre)",
        "chapters": ["Gitikapada (Astronomical constants)", "Ganitapada (Mathematics & Geometry)", "Kalakriyapada (Time reckoning)", "Golapada (Sphere & Celestial motion)"],
        "modern_significance": "Pioneered place-value zero notation, square/cube roots, and planetary orbital periods."
    },
    {
        "title": "Arthashastra",
        "author": "Chanakya (Kautilya)",
        "composed_year": "c. 300 BCE",
        "language": "Classical Sanskrit Prose & Shloka",
        "chapters": ["Vinayadhikarika (Discipline & Training)", "Adhyakshaprachara (Duties of Ministers)", "Dharmasthiya (Civil Law)", "Kantakashodhana (Criminal Law & Defense)"],
        "modern_significance": "World's foundational treatise on intelligence gathering, economic governance, and realistic international balance of power."
    },
    {
        "title": "Purusha Pariksha (The Test of a Man)",
        "author": "Mahakavi Vidyapati",
        "composed_year": "c. 1410 CE",
        "language": "Sanskrit & Classical Maithili",
        "chapters": ["Stories on Valour", "Stories on Wit & Intellect", "Stories on Charity & Compassion", "Stories on Truthfulness"],
        "modern_significance": "A masterpiece of ethical storytelling where character is evaluated across moral trials rather than birth or wealth."
    }
]

def get_all_treatises():
    """Return catalog of classical scientific and philosophical treatises."""
    return CLASSICAL_TREATISES_DB

NALANDA_LIBRARY_TOWERS_DB = [
    {
        "tower_name": "Ratnasagara ('Sea of Jewels')",
        "height_stories": 9,
        "specialization": "Sacred Mahayana sutras, Prajnaparamita manuscripts, and illuminated palm-leaf codices",
        "historical_note": "A soaring multi-storied architectural wonder capped with gilded finials visible across the Rajgir valley."
    },
    {
        "tower_name": "Ratnodadhi ('Ocean of Jewels')",
        "height_stories": 9,
        "specialization": "Astronomy, Ayurveda medicine, Sanskrit grammar (Vyakarana), and mathematical treatises",
        "historical_note": "Preserved the original astronomical calculation charts and medicinal herb classifications."
    },
    {
        "tower_name": "Ratnaranjaka ('Jeweled Delight')",
        "height_stories": 9,
        "specialization": "Epistemology (Pramana), Hetuvidya logic, and Yogacara philosophy",
        "historical_note": "Where foreign master scholars like Xuanzang and Yijing spent years translating texts from Sanskrit into Chinese."
    }
]

def get_nalanda_library_towers():
    """Return historical architecture and manuscript specialties of Nalanda's Dharmaganja library towers."""
    return NALANDA_LIBRARY_TOWERS_DB