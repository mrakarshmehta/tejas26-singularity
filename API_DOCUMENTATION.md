# 🗺️ HiddenYatra — API Documentation

## Overview

HiddenYatra exposes comprehensive RESTful JSON endpoints for location discovery, regional heritage circuits, multilingual audio guides, seasonal festival calendars, GI handicrafts, traveler safety & emergency helplines, transit fare calculations, and AI trip planning.

---

## 1. Regional Heritage & Cultural Discovery Endpoints

### 1.1 Thematic Cultural Circuits
* **URL:** GET /api/v1/circuits
* **Query Params:** 	heme (optional: spiritual, heritage, 
ature)
* **Response:**
`json
{
  "status": "success",
  "count": 5,
  "circuits": [
    {
      "id": 1,
      "slug": "buddhist-circuit",
      "title": "Enlightenment Trail (Buddhist Circuit)",
      "theme": "Spiritual & Heritage",
      "total_distance_km": 340,
      "duration_days": 4,
      "stops": [
        { "order": 1, "place_name": "Mahabodhi Temple", "district": "Gaya", "lat": 24.6961, "lng": 84.9913 }
      ]
    }
  ]
}
`

* **URL:** GET /api/v1/circuits/<slug>
* **Response:** Returns specific circuit metadata, stops sequence, and transit duration recommendations.

---

### 1.2 Multilingual Audio Guide Metadata
* **URL:** GET /api/v1/places/<slug>/audio
* **Response:**
`json
{
  "status": "success",
  "audio_guide": {
    "place_slug": "golghar",
    "title": "Acoustic Whispers of the Great Granary",
    "duration_sec": 180,
    "narrator": "HiddenYatra Heritage Voices",
    "languages": {
      "en": { "audio_url": "/static/audio/golghar_en.mp3", "transcript": "..." },
      "hi": { "audio_url": "/static/audio/golghar_hi.mp3", "transcript": "..." },
      "bho": { "audio_url": "/static/audio/golghar_bho.mp3", "transcript": "..." }
    }
  }
}
`

---

### 1.3 Cultural Festivals Calendar
* **URL:** GET /api/v1/festivals
* **Query Params:** month (e.g. November), district (e.g. Patna)
* **Response:**
`json
{
  "status": "success",
  "count": 6,
  "festivals": [
    {
      "slug": "chhath-puja",
      "name": "Chhath Puja Mahaparv",
      "month": "October / November",
      "primary_districts": ["Patna", "Gaya", "Bhagalpur", "All Bihar"],
      "rituals_highlights": ["Arghya to rising and setting Sun at holy ghats", "Thekua prasad preparation"]
    }
  ]
}
`

---

### 1.4 GI-Certified Handicrafts & Artisan Guilds
* **URL:** GET /api/v1/crafts
* **Query Params:** district (optional)
* **Response:**
`json
{
  "status": "success",
  "count": 5,
  "crafts": [
    {
      "slug": "madhubani-mithila-painting",
      "name": "Madhubani (Mithila) Painting",
      "gi_status": true,
      "origin_districts": ["Madhubani", "Darbhanga"],
      "prominent_villages": ["Ranti", "Jitwarpur"]
    }
  ]
}
`

* **URL:** GET /api/v1/crafts/<slug>
* **Response:** Full craft history, materials used, technique breakdown, and verified artisan workshops.

---

### 1.5 Responsible Traveler Code & Eco-Pledge
* **URL:** POST /api/v1/eco/pledge
* **Headers:** Content-Type: application/json
* **Body:**
`json
{
  "name": "Rohan Sharma",
  "email": "rohan@example.com",
  "state_origin": "Delhi"
}
`
* **Response:**
`json
{
  "status": "success",
  "message": "Thank you Rohan Sharma! You are now a certified Responsible Traveler for Bihar.",
  "badge": "🌿 Bihar Eco-Heritage Guardian",
  "certificate_code": "HY-ECO-84210"
}
`

---

## 2. Safety & Emergency Services Endpoints

### 2.1 Statewide Helplines & District Control Rooms
* **URL:** GET /api/v1/safety/emergency
* **Query Params:** district (optional: patna, gaya, 
alanda, etc.)
* **Response:**
`json
{
  "status": "success",
  "statewide_helplines": [
    { "service": "ERSS Unified Emergency", "number": "112", "priority": 1 },
    { "service": "Women Safety Helpline", "number": "1091", "priority": 2 },
    { "service": "Medical Ambulance", "number": "108", "priority": 4 }
  ],
  "district_safety": {
    "district": "Patna",
    "police_control_room": "+91-612-2201977",
    "tourist_police_desk": "+91-612-2215354"
  }
}
`

### 2.2 24/7 Medical & Trauma Facilities
* **URL:** GET /api/v1/safety/medical
* **Query Params:** district (optional)
* **Response:**
`json
{
  "status": "success",
  "count": 3,
  "facilities": [
    {
      "name": "Patna Medical College & Hospital (PMCH)",
      "type": "Government Apex Hospital",
      "phone": "+91-612-2300080",
      "emergency_24x7": true,
      "trauma_center": true
    }
  ]
}
`

---

## 3. Transit & Mobility Endpoints

### 3.1 Transport Hubs Directory
* **URL:** GET /api/v1/transport/hubs
* **Response:** Returns categorized commercial airports, major railway junctions, and BSRTC bus depots.

### 3.2 Inter-District Transit Matrix
* **URL:** GET /api/v1/transport/routes
* **Query Params:** origin, destination
* **Response:** Returns distance in km, train duration, road duration, and recommended routes.

### 3.3 Live Local Fare Estimator
* **URL:** GET /api/v1/transport/estimate-fare
* **Query Params:**
  - ehicle_type: uto_reserved | uto_shared | e_rickshaw | cab_hatchback | cab_suv | us_bsrtc
  - distance_km: float (e.g. 12)
  - is_night: boolean (	rue / alse)
* **Response:**
`json
{
  "status": "success",
  "fare_estimate": {
    "vehicle_type": "auto_reserved",
    "vehicle_title": "Reserved Auto-rickshaw (Full Auto)",
    "distance_km": 12.0,
    "base_fare_inr": 40.0,
    "additional_distance_fare_inr": 140.0,
    "night_surcharge_inr": 0.0,
    "total_estimated_fare_inr": 180,
    "pricing_unit": "entire vehicle (up to 3 passengers)"
  }
}
`

---

## 4. AI Trip Planner & Cultural Integration

### 4.1 Cultural Highlights for Itineraries
* **URL:** GET /itinerary/api/cultural-highlights
* **Query Params:** month (e.g. November), district (e.g. Gaya)
* **Response:** Returns active seasonal festivals and thematic circuits traversing requested destinations.