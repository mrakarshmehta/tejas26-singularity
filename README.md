# tejas26-singularity

Official Code Repository for tejas26-singularity at Tejas India Hackathon 2026

---

# 🗺️ HiddenYatra — Bihar Heritage, Culture & Eco-Tourism Portal

HiddenYatra is an immersive digital tourism platform and PWA dedicated to uncovering Bihar's ancient heritage, sacred thematic circuits, GI-tagged handicrafts, authentic gastronomy, wildlife reserves, and rural community immersion.

---

## ✨ Key Features & Subsystems

1. **Thematic Heritage Circuits**: Trail navigation covering Buddhist, Jain, Ganga River, Mithila, Sufi, and Eco circuits.
2. **Multilingual Audio Guides**: Cultural narrations with interactive speed controls and transcripts (English, Hindi, Bhojpuri).
3. **Virtual 360° Photo Spheres**: Immersive 8K panoramas of Mahabodhi Temple, Nalanda Monastery, and Rohtasgarh with interactive hotspots.
4. **Culinary Heritage & Food Trails**: Authentic delicacies (Litti Chokha, GI Silao Khaja, Gaya Tilkut, GI Mithila Makhana) with dietary filters and eatery locators.
5. **Eco-Wildlife & Nature Reserves**: Valmiki Tiger Reserve, Vikramshila Gangetic Dolphin Sanctuary, and Kanwar Lake Ramsar Wetland with safari guides.
6. **Rural Immersion & Cultural Volunteerism**: Folk art residencies, organic Makhana harvesting exchanges, and docent volunteering with automated skill matching.
7. **Universal Cross-Domain Search**: Real-time multi-entity search resolving places, circuits, festivals, crafts, cuisine, and wildlife.
8. **Traveler Safety & Emergency Hub**: 24/7 SOS 112 quick-dial, district police control rooms, and trauma hospital directory.
9. **Transit Mobility Portal**: Airport guides, rail corridors (Vande Bharat lines), and live local fare estimator.
10. **PWA Offline Resilience**: Complete service worker caching for seamless navigation in rural or low-connectivity areas.

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Blueprint Architecture, Jinja2 Templates
- **Database**: MySQL with PyMySQL / PooledDB connection pooling
- **Frontend**: Vanilla JavaScript (ES6+), Vanilla CSS3 Design System, Responsive Layouts
- **PWA**: Service Worker v9 with offline asset caching and navigation fallback
- **Maps**: Google Maps Platform (Advanced Markers) with Leaflet/MapLibre fallback
- **Testing**: Python unittest suite covering contract tests, unit tests, and full ecosystem integration

---

## v2.7.0 Features & New Subsystems

HiddenYatra v2.7.0 brings 9 major cultural subsystems and full universal search integration:
1. **Archaeology & Epigraphy Museum** (/archaeology, /numismatics): Mauryan Ashokan Brahmi pillars, Gupta gold dinars, and excavation timelines.
2. **Weather & Microclimate Advisory** (/weather): 38 district normals, seasonal packing checklists, AQI ratings, and fog advisories.
3. **Folk Performing Arts & Music** (/performing-arts): Bidesiya theater, Chhau dance, Kajari/Sohar chants, and traditional instrument gallery.
4. **Certified Local Tour Guides** (/guides): Licensed ASI guides, multilingual storytellers, and zero-commission booking inquiries.
5. **Eco-Trails & Hill Treks** (/treks): Mandar Hill, Rohtasgarh Plateau canyon expeditions, elevation profiles, and Leave No Trace rules.
6. **GI Souvenirs & Artisan Crafts** (/souvenirs): Mithila Tussar silk, Bhagalpur weaves, golden Sikki grass, and village studio visits.
7. **Ancient Intellectual Heritage** (/intellectual-heritage): Aryabhata, Chanakya, Nalanda 9-story library towers (Dharmaganja).
8. **Trip Budget Planner** (/budget-planner): Multi-currency (7 currencies) cost calculator, itemized expense breakdowns, and tipping etiquette.
9. **Heritage Trivia Quiz** (/quiz): Gamified cultural quiz bank, digital achievement badges, and verifiable certificates.
10. **Universal Cross-Domain Search**: Instant unified search across all 12 cultural dimensions of Bihar.

---

## Tejas 2.2 — Bihar Tourism Enhancements

Built for the Tejas India Hackathon 2.2 (Bihar Tourism problem statement), these features extend the platform's geographic discovery and cultural mapping capabilities.

### Travel Distance Metrics
- Per-hop Haversine distance between consecutive itinerary stops
- Day-wise and total trip distance summaries
- Route efficiency score: `min(100, (straight-line first→last ÷ total distance) × 100)`
- Backtracking detection when a stop is closer to stop[i−2] than 50% of the preceding hop
- Algorithm Details panel exposing all formulas — fully deterministic, **no ML/AI**

### Culture Map Layer
- Interactive map layer rendering 25 verified cultural heritage points across Bihar
- Five sub-layers: Heritage/Archaeology, Festivals, Crafts, Performing Arts, and Local Food
- Integrated into the existing Layer Registry for both Google Maps and Leaflet engines
- Data sourced from existing verified models — no fabricated coordinates

### Bihar Tourism Discovery Snapshot
- Live platform coverage statistics modal on the Explore Map page
- Displays verified place count, district coverage, hidden gems, and culture record totals
- All numbers sourced from real database queries and in-memory model counts

### Shareable Map State
- Map position (lat, lng, zoom) and selected place encoded in shareable URL parameters
- One-click copy-to-clipboard with toast notification
- Map state restored automatically when opening a shared link

### Map UX Improvements
- Smooth animated fly-to on marker selection with intelligent zoom behavior
- Pulse ring animation on selected markers
- Nearby radius overlay showing distance to surrounding places
