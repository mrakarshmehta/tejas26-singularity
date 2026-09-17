# 🗺️ HiddenYatra — Comprehensive API Documentation

## Overview

HiddenYatra exposes RESTful JSON endpoints for location discovery, thematic heritage circuits, multilingual audio guides, seasonal festival calendars, certified GI crafts, traveler safety & emergency helplines, transit mobility, virtual 360 tours, culinary heritage trails, wildlife sanctuaries, rural volunteerism, and universal search.

---

## 1. Regional Heritage & Discovery Endpoints

### 1.1 Thematic Cultural Circuits
* GET /api/v1/circuits — Retrieve all thematic heritage trails (Buddhist, Jain, Ganga, Mithila, Sufi, Eco).
* GET /api/v1/circuits/<slug> — Retrieve single circuit with stop sequence and transit stats.

### 1.2 Multilingual Audio Guides
* GET /api/v1/places/<slug>/audio — Retrieve audio guide stream metadata, narrators, and multilingual transcripts (en, hi, bho).

### 1.3 Cultural Festivals Calendar
* GET /api/v1/festivals — List festivals with optional ?month=... or ?district=... query.
* GET /api/v1/festivals/<slug> — Dedicated festival rituals and celebration guide.

### 1.4 Certified GI Handicrafts
* GET /api/v1/crafts — List Bihar GI-tagged crafts and artisan directories.
* GET /api/v1/crafts/<slug> — Craft history, raw materials, technique, and verified workshop guilds.

### 1.5 Responsible Traveler Code & Eco-Pledge
* POST /api/v1/eco/pledge — Submit digital pledge and generate certificate code (HY-ECO-XXXXX).

---

## 2. Safety & Emergency Services Endpoints

### 2.1 Statewide Helplines & District Control Rooms
* GET /api/v1/safety/emergency — Statewide priority numbers (112, 1091, 181, 108, 1070) and district police desks.

### 2.2 24/7 Medical & Trauma Centers
* GET /api/v1/safety/medical — 24/7 government medical colleges and trauma centers (PMCH, ANMMCH, VIMS, etc.).

---

## 3. Transit & Mobility Endpoints

### 3.1 Transport Hubs & Corridors
* GET /api/v1/transport/hubs — Commercial airports (PAT, GAY, DBR), railway junctions, and BSRTC bus depots.
* GET /api/v1/transport/routes — Inter-district transit travel times and highway recommendations.

### 3.2 Commute Fare Estimator
* GET /api/v1/transport/estimate-fare?vehicle_type=auto_reserved&distance_km=10&is_night=false — Real-time formula-based fare breakdown.

---

## 4. Virtual 360° Tours & Viewpoint Endpoints

### 4.1 Viewpoints Catalog
* GET /api/v1/panoramas — List all 8K UHD 360 photo spheres with optional ?district=... or ?category=....

### 4.2 Coordinate Hotspots
* GET /api/v1/panoramas/<slug>/hotspots — Interactive pitch/yaw coordinate hotspots and historical architectural callouts.

---

## 5. Culinary Heritage & Gastronomy Endpoints

### 5.1 Dishes Catalog
* GET /api/v1/gastronomy/dishes — Traditional delicacies with optional ?dietary=vegan|gluten-free or ?gi=true.
* GET /api/v1/gastronomy/dishes/<slug> — Cultural backstory, key ingredients, and verified heritage sweetmakers.

### 5.2 Regional Food Trails
* GET /api/v1/gastronomy/trails — Curated culinary journeys (Grand Magadha Trail, Mithilanchal Royal Flavors).

---

## 6. Wildlife Sanctuaries & Eco-Nature Reserves Endpoints

### 6.1 Sanctuaries Directory
* GET /api/v1/wildlife/sanctuaries — Protected reserves (Valmiki Tiger Reserve, Vikramshila Dolphin Sanctuary, Kanwar Lake).
* GET /api/v1/wildlife/sanctuaries/<slug> — Wildlife profile, key fauna, safari options, and permit booking info.
* GET /api/v1/wildlife/guidelines — Forest conservation and safari conduct guidelines.
* GET /api/v1/wildlife/species — Distinct species checklist across reserves.

---

## 7. Rural Immersion & Cultural Volunteerism Endpoints

### 7.1 Immersion Programs
* GET /api/v1/volunteer/programs — Active village residencies, farming exchanges, and docent opportunities.
* POST /api/v1/volunteer/apply — Submit volunteer registration; returns application ID and skill match percentage.

---

## 8. Universal Cross-Domain Search

### 8.1 Universal Discovery
* GET /api/v1/universal-search?q=<query>&limit=12 — Cross-domain search instantly matching across places, circuits, festivals, crafts, dishes, wildlife, and 360 photo spheres.
### Multi-Currency Trip Budget Planner API

#### 1. Calculate Trip Budget
GET /api/v1/budget/calculate or POST /api/v1/budget/calculate

Query / Payload Parameters:
- tier (string, optional): backpacker, heritage (default), luxury
- days (int, optional): 1 to 30 (default: 3)
- travelers (int, optional): 1 to 20 (default: 2)
- currency (string, optional): INR (default), USD, EUR, GBP, JPY, AUD, SGD

#### 2. Get Travel Tiers
GET /api/v1/budget/tiers

#### 3. Get Currencies
GET /api/v1/budget/currencies

#### 4. Get District Cost Index
GET /api/v1/budget/district-cost-index
### Heritage Trivia Quiz & Explorer Badge API

#### 1. Get Quiz Questions
GET /api/v1/quiz/questions (Optional: ?category=history|culture|archaeology|gastronomy|wildlife)

#### 2. Get Quiz Categories
GET /api/v1/quiz/categories

#### 3. Evaluate Quiz Answers & Unlock Badge
POST /api/v1/quiz/evaluate

Payload:
{
  "answers": {
    "q-aryabhata-discovery": 1,
    "q-nalanda-library": 0
  }
}

#### 4. Issue Digital Certificate
POST /api/v1/quiz/certificate

Payload:
{
  "name": "Priya Sharma",
  "score": 6,
  "total": 6,
  "badge": "Grand Magadha Mahapandit"
}
## Complete Subsystems API Map (v2.7.0)

| Subsystem | Endpoints | Description |
|-----------|-----------|-------------|
| **Archaeology & Epigraphy** | /api/v1/archaeology/sites, /api/v1/archaeology/chronology, /api/v1/archaeology/coins, /api/v1/archaeology/inscriptions | Excavation records, Ashokan pillars, Gupta gold dinars, Brahmi rock edicts. |
| **Weather & Microclimate** | /api/v1/weather/districts, /api/v1/weather/packing-advice, /api/v1/weather/phenomena, /api/v1/weather/alerts | 38 district normals, AQI categories, winter fog index, severe weather protocols. |
| **Folk Performing Arts** | /api/v1/performing-arts, /api/v1/performing-arts/instruments, /api/v1/performing-arts/guilds, /api/v1/performing-arts/seasons | Bidesiya theater, Chhau dance, Kajari/Sohar ballads, instrument gallery. |
| **Verified Tour Guides** | /api/v1/guides, /api/v1/guides/inquire, /api/v1/guides/ethics, /api/v1/guides/verify-license | Certified ASI guides, multilingual storytellers, zero-commission inquiries. |
| **Eco-Trails & Treks** | /api/v1/treks, /api/v1/treks/safety, /api/v1/treks/campsites, /api/v1/treks/fitness | Mandar Hill, Rohtasgarh canyon, elevation gains, Leave No Trace protocols. |
| **GI Souvenirs & Crafts** | /api/v1/souvenirs, /api/v1/souvenirs/guidelines, /api/v1/souvenirs/workshops, /api/v1/souvenirs/authenticity | Madhubani silk, Bhagalpuri weaves, Sikki grass, artisan guild workshops. |
| **Ancient Intellectual Heritage** | /api/v1/scholars, /api/v1/scholars/universities, /api/v1/scholars/treatises, /api/v1/scholars/nalanda-library | Aryabhata, Chanakya, Nalanda 9-story library towers (Dharmaganja). |
| **Trip Budget Planner** | /api/v1/budget/calculate, /api/v1/budget/tiers, /api/v1/budget/currencies, /api/v1/budget/district-cost-index, /api/v1/budget/tipping-guidelines | Multi-currency (7 currencies) itemized cost calculator and tipping guide. |
| **Heritage Trivia Quiz** | /api/v1/quiz/questions, /api/v1/quiz/categories, /api/v1/quiz/evaluate, /api/v1/quiz/certificate | Cultural gamification question bank, badge rewards, and digital certificates. |