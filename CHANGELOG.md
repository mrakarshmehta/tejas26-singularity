# HiddenYatra — Changelog

All notable changes to the HiddenYatra project are documented in this file.

---

## [2.5.0] — 2026-08-21 (52-Commit Milestone Release)

### Added
- **Thematic Cultural Circuits**: Complete trail navigation subsystem covering Buddhist, Jain, Ganga River, Mithila Art, Sufi, and Eco-Wildlife circuits with distance metrics and stop itineraries.
- **Multilingual Audio Guides**: Place audio narration support with interactive audio player bar, playback rate selector, and multilingual transcripts (English, Hindi, Bhojpuri).
- **Seasonal Festival Calendar**: Cultural celebrations calendar with monthly filter, district queries, rituals guide, and traveler tips.
- **Certified GI Handicrafts Directory**: Bihar GI crafts catalog with artisan guild workshop directories, raw material guides, and verified cluster locations.
- **Responsible Traveler Code & Eco-Pledge**: Sustainable tourism framework with digital pledge signing, certificate generator, and eco-heritage guardian badge.
- **Bihar Traveler Safety Hub**: 24/7 SOS 112 quick-dial, statewide priority helplines (108, 1091, 181, 1070), district police control rooms, and trauma hospital directory.
- **Transit & Commute Mobility Portal**: Gateway airport guides, major rail corridors (Vande Bharat lines), BSRTC bus depots, inter-district transit matrix, and live local fare estimator widget.
- **AI Trip Planner Cultural Enrichment**: Intelligent syncing between travel month/districts and active cultural festivals & thematic trails.
- **PWA Service Worker Offline Enhancements**: Caching for safety directory, transport guides, and circuits with offline navigation fallback.

### Fixed & Tested
- Fixed unit test indentation in 	ests/test_itinerary.py and contract assertions in 	ests/test_discovery_contract.py.
- Added dedicated test suites: 	ests/test_safety.py, 	ests/test_transport.py, 	ests/test_circuits.py, 	ests/test_festivals.py, 	ests/test_crafts.py, 	ests/test_eco.py, 	ests/test_places_audio.py, and 	ests/test_milestone_52.py.

---

## [2.4.0] — 2026-08-20
### Added
- Multi-day itinerary pacing configurations and travel budget estimation engine.
- Homestay date availability validation and dynamic stay pricing calculator.
- Community submission review workflows and helpful review vote toggles.
- Haversine proximity radius calculator and custom category SVG map markers.
- PWA offline navigation fallback with dedicated offline guide route.
- Admin structured audit logging and live telemetry metrics.
- Password complexity verification and OTP sliding-window rate limiting.

---

## [1.2.0] — 2026-08-06
### Added
- Created AUDIT.md, FIXES.md, TECH_DEBT.md, and CHANGELOG.md.
- Added automated test modules for community, reviews, user photos, and wishlist.