# HiddenYatra — Heritage Discovery Subsystems

This document specifies the technical architecture and route contracts for the Bihar Heritage Discovery Milestone.

## 1. Thematic Circuit Engine (`models/circuits.py`)
Provides structured itineraries across core cultural narratives:
- **Buddhist Enlightenment & Monastic Trail** (Bodh Gaya -> Rajgir -> Nalanda -> Vaishali)
- **Sacred Ganga & Solar Heritage Route** (Patna -> Sultanganj -> Bhagalpur -> Munger)
- **Mithila Folk Art & Cultural Odyssey** (Darbhanga -> Madhubani -> Sitamarhi)
- **Ancient Magadha Dynastic & Cave Trail** (Barabar Caves -> Rajgir -> Bihar Sharif)
- **Sufi & Interfaith Harmony Trail** (Maner Sharif -> Bihar Sharif -> Phulwari Sharif)

### Routes & API:
- `GET /circuits` — Browse thematic circuit directory.
- `GET /circuit/<slug>` — Stop itinerary timeline and transit details.
- `GET /api/circuits` — JSON list of all circuits.
- `GET /api/circuits/<slug>` — JSON details and calculated transit distance.

---

## 2. Multilingual Audio Guides (`models/places.py`)
- Provides localized audio stream metadata in English, Hindi, and regional dialects (Maithili, Bhojpuri, Magahi).
- Frontend controller supports speed toggling (0.8x - 1.5x) and full synchronized transcript reading.
- API: `GET /api/places/<id>/audio-guide`

---

## 3. Seasonal Festival Calendar (`models/festivals.py`)
- Documented dates, rituals, and visitor insights for Chhath Puja, Sonepur Mela, Rajgir Mahotsav, Sama Chakeva, Buddha Jayanti, and Shravani Mela.
- Routes: `GET /festivals`, `GET /festival/<slug>`, `GET /api/festivals`

---

## 4. GI Crafts & Artisan Guilds (`models/crafts.py`)
- Curates Bihar's registered Geographical Indication (GI) products: Madhubani Painting, Bhagalpuri Tussar Silk, Sikki Grass Craft, Manjusha Art, and Sujini Embroidery.
- Routes: `GET /crafts`, `GET /craft/<slug>`, `GET /api/crafts`

---

## 5. Eco-Heritage & Responsible Traveler Code (`models/eco.py`)
- Zero-Trace Heritage Preservation, Living Sacred Ritual Respect, and Direct Local Artisan Spending.
- Digital pledge certificate generation via `POST /api/eco/pledge`.
