# HiddenYatra — System Architecture Blueprint

## 1. System Architecture Overview

HiddenYatra is a modern, responsive web application and PWA dedicated to uncovering Bihar's cultural heritage, spiritual circuits, GI-tagged crafts, regional gastronomy, wildlife sanctuaries, and community-based rural tourism.

`
+-------------------------------------------------------------------------+
|                              Client Layer                               |
|   Responsive Web UI  |  PWA Service Worker (v6)  |  Interactive Canvas  |
|   (Vanilla JS/CSS3)  |  (Offline Fallbacks)      |  (360° Photo Spheres)|
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                           Application Server                            |
|                            Flask Blueprint Core                         |
|   +-------------------+  +-------------------+  +-------------------+   |
|   |  Routes (Main)    |  |  Routes (API v1)  |  | Routes (Itinerary)|   |
|   |  /virtual-tours   |  |  /api/v1/panos    |  | /api/budget-est   |   |
|   |  /gastronomy      |  |  /api/v1/gastro   |  | /api/highlights   |   |
|   |  /wildlife        |  |  /api/v1/wildlife |  | /api/universal-sr |   |
|   |  /volunteer       |  |  /api/v1/vol      |  |                   |   |
|   +-------------------+  +-------------------+  +-------------------+   |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                               Data Layer                                |
|   MySQL Relational DB | Memory Index Engine | Structured Python Models  |
|   - Places & Reviews  | - Universal Search  | - 360 Panoramas           |
|   - Districts & Stays | - Geo-Proximity     | - Gastronomy & Trails     |
|   - Audit & Security  | - Instant Scoring   | - Wildlife Sanctuaries    |
|                       |                     | - Volunteer Matching      |
+-------------------------------------------------------------------------+
`

## 2. Core Subsystems

### 2.1 Virtual 360° Photo Spheres (models/panoramas.py)
- High-definition 8K panoramic photo sphere viewer.
- Interactive coordinate pitch/yaw hotspots.
- Multilingual narration audio ties (en, hi, bho, tib, zh, ja, ur).

### 2.2 Gastronomy & Culinary Trails (models/gastronomy.py)
- Authentic recipe lore, ingredients, and GI certification.
- Dietary filtering: Vegan, Gluten-Free, High-Protein.
- Curated regional food trail itineraries (Grand Magadha, Mithilanchal).

### 2.3 Wildlife & Eco-Sanctuaries (models/wildlife.py)
- Valmiki Tiger Reserve, Vikramshila Dolphin Sanctuary, Kanwar Lake Ramsar Wetland.
- Safari bookings, permit rules, and endangered species tracking.

### 2.4 Rural Immersion & Volunteerism (models/volunteer.py)
- Artisan residencies (Madhubani folk art), Makhana harvesting exchanges, and Nalanda docent programs.
- Automated skill matching and candidate registration engine.

### 2.5 Universal Cross-Domain Search (models/search_engine.py)
- Instant multi-entity resolver spanning all 7 discovery domains.

### 2.6 Traveler Safety & Mobility (models/safety.py, models/transport.py)
- 24/7 SOS 112 quick-dial, district control rooms, and trauma hospitals.
- Transit hubs, distance matrices, and real-time commute fare estimator.
## v2.7.0 Extended Subsystem Architecture Map

- **Archaeology & Epigraphy Module** (models/archaeology.py)
- **Weather & Microclimate Advisory** (models/weather.py)
- **Folk Performing Arts & Music** (models/performing_arts.py)
- **Certified Local Tour Guides** (models/guides.py)
- **Eco-Trails & Hill Treks** (models/treks.py)
- **GI Souvenirs & Artisan Crafts** (models/souvenirs.py)
- **Ancient Intellectual Heritage** (models/intellectual_heritage.py)
- **Trip Budget Planner** (models/budget_planner.py)
- **Heritage Trivia Quiz** (models/quiz.py)
- **Universal Cross-Domain Search** (models/search_engine.py)
- **PWA Service Worker v7** (static/sw.js)
