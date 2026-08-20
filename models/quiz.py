"""
Bihar Heritage Trivia Quiz & Cultural Gamification Engine
Provides categorized heritage question banks, score evaluation algorithms,
knowledge badges (Mauryan Scholar, Mithila Connoisseur, Magadha Explorer),
and certificate generation.
"""

HERITAGE_QUIZ_DB = [
    {
        "id": "q-aryabhata-discovery",
        "category": "history",
        "difficulty": "Easy",
        "question": "Which ancient astronomer from Pataliputra calculated the accurate value of Pi (3.1416) and proved the Earth rotates on its axis?",
        "options": ["Varahamihira", "Aryabhata", "Brahmagupta", "Bhaskara I"],
        "correct_index": 1,
        "explanation": "Aryabhata composed the revolutionary 'Aryabhatiya' at Khagaul near Pataliputra in 499 CE at just 23 years of age."
    },
    {
        "id": "q-nalanda-library",
        "category": "archaeology",
        "difficulty": "Medium",
        "question": "What was the name of the sacred nine-story library complex at ancient Nalanda Mahavihara?",
        "options": ["Dharmaganja", "Jnana Bhavan", "Vidyapith", "Granthagar"],
        "correct_index": 0,
        "explanation": "Dharmaganja ('Mart of Religion') comprised three immense nine-story library towers: Ratnasagara, Ratnodadhi, and Ratnaranjaka."
    },
    {
        "id": "q-madhubani-pigment",
        "category": "culture",
        "difficulty": "Easy",
        "question": "In traditional Mithila/Madhubani painting, what natural ingredient is historically used to create deep black pigment?",
        "options": ["Crushed Charcoal", "Kajal (Soot from Mustard Oil Lamp)", "Black Rice Paste", "Iron Slag"],
        "correct_index": 1,
        "explanation": "Black lines are traditionally drawn using soot (kajal) collected over an earthen mustard oil lamp, mixed with cow dung or gum arabic."
    },
    {
        "id": "q-silao-khaja-gi",
        "category": "gastronomy",
        "difficulty": "Medium",
        "question": "Which historic town situated between Nalanda and Rajgir is celebrated for its 52-layered crispy GI-certified sweet?",
        "options": ["Maner", "Silao", "Bodh Gaya", "Bakhtiyarpur"],
        "correct_index": 1,
        "explanation": "Silao Khaja received GI certification (GI No. 553) for its distinctive 52 multi-layered crispy flaky crust made with local spring water."
    },
    {
        "id": "q-valmiki-river",
        "category": "wildlife",
        "difficulty": "Master",
        "question": "Which majestic Himalayan river flows through the core zone of Valmiki Tiger Reserve forming the international border with Nepal?",
        "options": ["Kosi River", "Gandak (Narayani) River", "Bagmati River", "Sone River"],
        "correct_index": 1,
        "explanation": "The Gandak River (known as Narayani in Nepal) creates the pristine riverine wetlands of Valmiki Tiger Reserve, home to fish-eating Gharials."
    },
    {
        "id": "q-bhikhari-thakur",
        "category": "culture",
        "difficulty": "Medium",
        "question": "Playwright Bhikhari Thakur, celebrated as the 'Shakespeare of Bhojpuri', is most famous for creating which folk theater genre?",
        "options": ["Nautanki", "Bidesiya", "Swang", "Tamasha"],
        "correct_index": 1,
        "explanation": "Bidesiya addresses the emotional pathos and social realities of rural migration from Bihar to industrial cities."
    }
]