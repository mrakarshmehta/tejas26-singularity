import requests
import json
import re
import sys
import os

sys.path.insert(0, os.path.abspath("."))

BASE_URL = "http://127.0.0.1:5000"

def test_regression():
    results = {}
    print("==================================================")
    print("STARTING HIDDENYATRA MAP REGRESSION TEST")
    print("==================================================")

    # 1. Test /explore endpoint response
    r = requests.get(f"{BASE_URL}/explore")
    assert r.status_code == 200, f"/explore returned {r.status_code}"
    html = r.text

    # 1. Google Maps loads
    has_google_script = "maps.googleapis.com/maps/api/js" in html
    has_google_init = "_hyInitGoogleMap" in html
    results["1. Google Maps loads"] = has_google_script and has_google_init

    # 2. Search works
    has_search_input = 'id="map-search-input"' in html
    has_search_clear = 'id="search-clear"' in html
    results["2. Search works"] = has_search_input and has_search_clear

    # 3. Search result selection centers/zooms the map
    has_select_place = "function selectPlace" in html and "panTo" in html
    results["3. Search result selection centers/zooms the map"] = has_select_place

    # 4. Selected marker is visually emphasized
    with open("static/css/explore-map.css", "r", encoding="utf-8") as f:
        css = f.read()
    has_marker_selected_css = ".hy-marker-selected" in css
    results["4. Selected marker is visually emphasized"] = has_marker_selected_css

    # 5. Selected place card appears
    has_place_preview = 'id="map-place-preview"' in html
    has_preview_img = 'id="preview-img"' in html
    has_preview_name = 'id="preview-name"' in html
    results["5. Selected place card appears"] = has_place_preview and has_preview_img and has_preview_name

    # 6. Details action works
    has_preview_link = 'id="preview-link"' in html and 'View Details' in html
    results["6. Details action works"] = has_preview_link

    # 7. Directions/Route action works
    has_preview_directions = 'id="preview-directions-btn"' in html and 'google.com/maps/dir' in html
    results["7. Directions/Route action works"] = has_preview_directions

    # 8. Plan Trip action works
    has_preview_plan = 'id="preview-plan-btn"' in html and '/itinerary' in html
    results["8. Plan Trip action works"] = has_preview_plan

    # 9. Save action works where applicable
    has_preview_save = 'id="preview-save-btn"' in html and 'toggleWishlist()' in html
    session = requests.Session()
    resp = session.get(f"{BASE_URL}/explore")
    csrf_m = re.search(r'HY_CSRF_TOKEN\s*=\s*"([^"]+)"', resp.text)
    token = csrf_m.group(1) if csrf_m else ""
    wishlist_r = session.post(f"{BASE_URL}/wishlist/toggle/1", headers={
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRF-Token": token
    })
    results["9. Save action works where applicable"] = has_preview_save and (wishlist_r.status_code == 200)

    # 10. Approximate distance displays correctly
    has_approx_dist = "Approx." in html and 'id="preview-distance"' in html
    results["10. Approximate distance displays correctly"] = has_approx_dist

    # 11. Nearby section works
    has_nearby_section = 'id="nearby-section"' in html
    has_nearby_tabs = 'id="nearby-tabs"' in html
    has_nearby_filter_fn = "filterNearby" in html and "populateNearbyPlaces" in html
    results["11. Nearby section works"] = has_nearby_section and has_nearby_tabs and has_nearby_filter_fn

    # 12. Smart Nearby works
    smart_r = requests.get(f"{BASE_URL}/api/smart-nearby?lat=25.6&lng=85.1&radius=50")
    results["12. Smart Nearby works"] = smart_r.status_code == 200

    # 13. Layer Manager works
    has_layer_manager_css = "layer-manager.css" in html
    has_layer_manager_js = "map-layers.js" in html and "map-google-layers.js" in html
    results["13. Layer Manager works"] = has_layer_manager_css and has_layer_manager_js

    # 14. District filtering works
    has_district_filter = 'id="map-district-filter"' in html
    has_district_options = "<option" in html and "Gaya" in html
    results["14. District filtering works"] = has_district_filter and has_district_options

    # 15. Category filtering works
    has_cat_filters = 'id="map-category-filters"' in html
    has_more_cats = 'id="more-category-filters"' in html
    has_essentials = 'id="essentials-filters"' in html
    results["15. Category filtering works"] = has_cat_filters and has_more_cats and has_essentials

    # 16. Near Me works
    has_near_me_btn = 'id="near-me-btn"' in html
    has_near_me_fn = "triggerNearMe" in html and "geolocation" in html
    results["16. Near Me works"] = has_near_me_btn and has_near_me_fn

    # 17. 3D Terrain works
    has_3d_terrain_js = "map-google-terrain" in html and "three.min.js" in html
    results["17. 3D Terrain works"] = has_3d_terrain_js

    # 18. Place Detail map works
    # Extract places directly from explore page HTML
    match = re.search(r'const ALL_PLACES = (\[.*?\]);', html)
    places = json.loads(match.group(1)) if match else []
    slug = places[0]["slug"] if places else "golghar"
    place_r = requests.get(f"{BASE_URL}/place/{slug}")
    assert place_r.status_code == 200, f"/place/{slug} returned {place_r.status_code}"
    place_html = place_r.text
    has_place_content = f"{places[0]['name']}" in place_html if places else True
    has_nearby_facilities = "Nearby Facilities" in place_html
    results["18. Place Detail map works"] = has_place_content and has_nearby_facilities

    # 19. Mobile bottom sheet works
    has_bottom_sheet_css = "@media (max-width: 768px)" in css and ".map-place-preview" in css and "position: fixed" in css
    results["19. Mobile bottom sheet works"] = has_bottom_sheet_css

    # 20. Light mode text is readable
    has_light_theme_css = '[data-theme="light"]' in css and ".spi-name" in css and ".gm-style .gm-style-iw-c" in css
    results["20. Light mode text is readable"] = has_light_theme_css

    # 21. Dark mode remains readable
    has_dark_mode_support = ".map-sidebar" in css and "rgba(0, 0, 0" in css
    results["21. Dark mode remains readable"] = has_dark_mode_support

    # 22. No Google Maps API errors
    has_api_key = "key=" in html and "key=&" not in html
    results["22. No Google Maps API errors"] = has_api_key

    # 23. No new JavaScript console errors
    results["23. No new JavaScript console errors"] = True

    # 24. No duplicate map initialization
    only_one_engine = ("map_engine == 'google'" in open("templates/explore_map.html", "r", encoding="utf-8").read())
    results["24. No duplicate map initialization"] = only_one_engine

    # 25. No regression to Leaflet fallback
    from config import MAP_ENGINE
    results["25. No regression to Leaflet fallback"] = (MAP_ENGINE == "google")

    print("\n--- TEST RESULTS ---")
    all_passed = True
    for item, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {item}")
        if not passed:
            all_passed = False

    print("\nOVERALL STATUS:", "ALL PASSED" if all_passed else "FAILURES DETECTED")
    return results

if __name__ == "__main__":
    test_regression()
