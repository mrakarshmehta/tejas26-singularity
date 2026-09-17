import requests, json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

s = requests.Session()

# Check itinerary page for export/PDF
r = s.get("http://127.0.0.1:5000/itinerary")
text = r.text.lower()
print("=== ITINERARY PAGE AUDIT ===")
print("has export btn:", "export" in text or "download" in text)
print("has pdf:", "pdf" in text)
print("has print:", "print" in text)
print("has html2canvas:", "html2canvas" in text)
print("has jspdf:", "jspdf" in text)

# Check for food/stay matching in itinerary template
raw = r.text
print("\nhas recommended_foods:", "recommended_foods" in raw or "food_recommendations" in raw)
print("has recommended_hotels:", "recommended_hotels" in raw or "stay_recommendation" in raw)
print("has budget section:", "budget" in raw.lower() and "cost" in raw.lower())

# Check cultural/heritage pages
pages = {
    "festivals": "/festivals",
    "crafts": "/crafts",
    "performing-arts": "/performing-arts",
    "archaeology": "/archaeology",
    "scholars": "/intellectual-heritage",
    "gastronomy": "/gastronomy",
    "souvenirs": "/souvenirs",
    "treks": "/treks",
    "wildlife": "/wildlife",
    "weather": "/weather",
    "transport": "/transport",
    "safety": "/safety",
    "volunteer": "/volunteer",
    "eco-pledge": "/eco-pledge",
    "quiz": "/quiz",
    "virtual-tours": "/virtual-tours",
    "stays": "/stays",
    "budget-planner": "/budget-planner",
    "circuits": "/circuits",
}

print("\n=== CULTURAL/HERITAGE PAGES ===")
for name, path in pages.items():
    try:
        resp = s.get(f"http://127.0.0.1:5000{path}")
        has_content = len(resp.text) > 1000
        print(f"  {name}: status={resp.status_code} content={'YES' if has_content else 'MINIMAL'} ({len(resp.text)} bytes)")
    except Exception as e:
        print(f"  {name}: ERROR {e}")

# Admin panel
print("\n=== ADMIN PANEL ===")
r_admin = s.get("http://127.0.0.1:5000/admin/login")
print("Admin login page:", r_admin.status_code)
r_admin_dash = s.get("http://127.0.0.1:5000/admin/")
print("Admin dashboard (no login):", r_admin_dash.status_code, "(should redirect/403)")

# Proximity clustering check
print("\n=== ITINERARY ENGINE INTERNALS ===")
with open("routes/itinerary.py", "r", encoding="utf-8") as f:
    itin_code = f.read()
print("has haversine:", "haversine" in itin_code)
print("has proximity/cluster:", "proximity" in itin_code.lower() or "cluster" in itin_code.lower())
print("has budget calc:", "budget" in itin_code.lower() and "cost" in itin_code.lower())
print("has food matching:", "food" in itin_code.lower())
print("has stay matching:", "hotel" in itin_code.lower() or "stay" in itin_code.lower())
print("has dedup:", "seen" in itin_code or "duplicate" in itin_code.lower() or "used" in itin_code)

# Auth check
print("\n=== AUTH ===")
r_signup = s.get("http://127.0.0.1:5000/signup")
print("Signup page:", r_signup.status_code)
has_email_verify = "verify" in r_signup.text.lower() or "otp" in r_signup.text.lower()
print("Has email verification flow:", has_email_verify)
r_login = s.get("http://127.0.0.1:5000/login")
print("Login page:", r_login.status_code)

# Mobile check
print("\n=== MOBILE RESPONSIVENESS ===")
with open("static/css/main.css", "r", encoding="utf-8") as f:
    main_css = f.read()
media_queries = len(re.findall(r'@media', main_css))
print("Media queries in main.css:", media_queries)
with open("templates/base.html", "r", encoding="utf-8") as f:
    base = f.read()
print("Has viewport meta:", "viewport" in base)
print("Has manifest:", "manifest" in base)
print("Has service worker:", "serviceWorker" in base or "sw.js" in base)

# Security
print("\n=== SECURITY ===")
print("CSRF protection:", "_csrf_token" in base or "csrf_token" in base)
with open("app.py", "r", encoding="utf-8") as f:
    app_code = f.read()
print("has CSP:", "Content-Security-Policy" in app_code)
print("has rate limiting:", "limiter" in app_code.lower() or "rate" in app_code.lower())
print("has secure headers:", "X-Frame-Options" in app_code or "X-Content-Type" in app_code)

# Data coverage
print("\n=== DATABASE COVERAGE ===")
r_explore = s.get("http://127.0.0.1:5000/explore")
match = re.search(r'const ALL_PLACES = (\[.*?\]);', r_explore.text)
if match:
    places = json.loads(match.group(1))
    print(f"Total places: {len(places)}")
    hidden = sum(1 for p in places if p.get("is_hidden_gem"))
    print(f"Hidden gems: {hidden}")
    with_images = sum(1 for p in places if p.get("cover_image"))
    print(f"With cover images: {with_images}")
    with_coords = sum(1 for p in places if p.get("latitude") and p.get("longitude"))
    print(f"With coordinates: {with_coords}")

# Check food data
r_food = s.get("http://127.0.0.1:5000/food-culture")
print(f"\nFood & Culture page: {r_food.status_code}, {len(r_food.text)} bytes")

# Stays check
r_stays = s.get("http://127.0.0.1:5000/stays")
print(f"Stays/Local Stays page: {r_stays.status_code}, {len(r_stays.text)} bytes")
has_listings = "listing" in r_stays.text.lower() or "homestay" in r_stays.text.lower()
print(f"Has stay listings: {has_listings}")
