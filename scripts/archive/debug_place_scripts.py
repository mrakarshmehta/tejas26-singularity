import requests
r = requests.get("http://127.0.0.1:5000/place/golghar")
print("Length of response:", len(r.text))
print("Contains google_maps_api_key in HTML:", "maps.googleapis.com" in r.text)
for line in r.text.splitlines():
    if "script" in line.lower() or "leaflet" in line.lower() or "place-map" in line.lower():
        print("  >", line.strip())
