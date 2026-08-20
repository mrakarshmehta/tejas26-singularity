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

BADGE_TIERS_DB = [
    {"min_percent": 90, "badge": "🏛️ Grand Magadha Mahapandit (Master Explorer)", "color": "#7c2d12"},
    {"min_percent": 75, "badge": "📜 Nalanda Scholar (Heritage Expert)", "color": "#4338ca"},
    {"min_percent": 50, "badge": "🧭 Bihar Yatra Explorer (Curious Traveler)", "color": "#0284c7"},
    {"min_percent": 0, "badge": "🌱 Heritage Novice (Beginning the Journey)", "color": "#16a34a"}
]

def get_all_quiz_questions(category=None):
    """Return quiz questions, optionally filtered by category (without exposing correct index for clients)."""
    if not category or category.lower() == 'all':
        questions = HERITAGE_QUIZ_DB
    else:
        c_clean = category.lower().strip()
        questions = [q for q in HERITAGE_QUIZ_DB if q["category"].lower() == c_clean]

    # Return client-safe list without answer keys for secure rendering
    client_safe = []
    for q in questions:
        client_safe.append({
            "id": q["id"],
            "category": q["category"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "options": q["options"]
        })
    return client_safe

def get_quiz_categories():
    """Return all unique quiz categories."""
    return sorted(list(set(q["category"] for q in HERITAGE_QUIZ_DB)))

def evaluate_quiz_submission(answers_dict):
    """Evaluate submitted answers dictionary { 'q-id': selected_index } and award digital badge."""
    if not answers_dict or not isinstance(answers_dict, dict):
        return {
            "score": 0,
            "total": len(HERITAGE_QUIZ_DB),
            "percentage": 0,
            "badge": BADGE_TIERS_DB[-1]["badge"],
            "results": []
        }

    correct_count = 0
    detailed_results = []

    for q in HERITAGE_QUIZ_DB:
        q_id = q["id"]
        user_choice = answers_dict.get(q_id)
        is_correct = False

        if user_choice is not None:
            try:
                choice_idx = int(user_choice)
                if choice_idx == q["correct_index"]:
                    is_correct = True
                    correct_count += 1
            except (ValueError, TypeError):
                pass

        detailed_results.append({
            "id": q_id,
            "question": q["question"],
            "user_choice": int(user_choice) if user_choice is not None and str(user_choice).isdigit() else None,
            "correct_index": q["correct_index"],
            "is_correct": is_correct,
            "correct_answer": q["options"][q["correct_index"]],
            "explanation": q["explanation"]
        })

    total = len(HERITAGE_QUIZ_DB)
    percentage = round((correct_count / total) * 100, 1) if total > 0 else 0

    awarded_badge = BADGE_TIERS_DB[-1]["badge"]
    badge_color = BADGE_TIERS_DB[-1]["color"]
    for b in BADGE_TIERS_DB:
        if percentage >= b["min_percent"]:
            awarded_badge = b["badge"]
            badge_color = b["color"]
            break

    return {
        "score": correct_count,
        "total": total,
        "percentage": percentage,
        "badge": awarded_badge,
        "badge_color": badge_color,
        "results": detailed_results
    }

def generate_quiz_certificate(user_name, score, total, badge_title):
    """Generate structured digital certificate metadata for heritage quiz achievers."""
    name_clean = user_name.strip() if user_name else "Heritage Explorer"
    cert_id = f"HY-CERT-{abs(hash(name_clean + str(score) + str(total))) % 1000000:06d}"
    return {
        "certificate_id": cert_id,
        "recipient_name": name_clean,
        "score_awarded": f"{score}/{total}",
        "badge_title": badge_title,
        "issuer": "HiddenYatra Heritage Preservation Board",
        "verification_url": f"/quiz/verify-cert?id={cert_id}"
    }