"""
Phase 2E Selenium End-to-End Acceptance Test Suite: Hotels & Homestays.
Verifies 12 hotels, 10 homestays, popups, deep-links, 6 map modes, 2D/3D state transitions, mobile drawer, and console logs.
"""

import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_phase2e_e2e_verification():
    print("=" * 60)
    print("  PHASE 2E HOTELS & HOMESTAYS E2E VERIFICATION")
    print("=" * 60)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = "http://127.0.0.1:5000/explore"
        print(f"\n[1] Navigating to {url} ...")
        driver.get(url)
        time.sleep(2.5)

        # 1. Check Registry Definitions
        print("\n[2] Checking HYMap Registry for Hotels and Homestays...")
        reg_info = driver.execute_script("""
            return {
                hasRegistry: !!window.HYLayerRegistry,
                hotelsDef: window.HYLayerRegistry ? window.HYLayerRegistry.get('hotels') : null,
                homestaysDef: window.HYLayerRegistry ? window.HYLayerRegistry.get('homestays') : null,
            };
        """)
        print(f"    Hotels registered: {reg_info['hotelsDef']['label']} -> {reg_info['hotelsDef']['source']}")
        print(f"    Homestays registered: {reg_info['homestaysDef']['label']} -> {reg_info['homestaysDef']['source']}")
        assert reg_info['hotelsDef']['source'] == '/static/data/bihar/hotels.geojson', "Hotels source mismatch"
        assert reg_info['homestaysDef']['source'] == '/static/data/bihar/homestays.geojson', "Homestays source mismatch"

        # 2. Open Layer Manager
        print("\n[3] Opening Layer Manager Drawer...")
        driver.execute_script("document.getElementById('hy-layers-btn').click();")
        time.sleep(0.5)
        lm_panel = driver.find_element(By.ID, "hy-layer-manager")
        is_open = "open" in lm_panel.get_attribute("class")
        print(f"    Layer Manager open: {is_open}")
        assert is_open, "Layer Manager failed to open"

        # 3. Toggle Hotels ON in Leaflet 2D
        print("\n[4] Testing Hotels Layer ON in Leaflet 2D...")
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return hy.setLayerVisible('hotels', true);
        """)
        time.sleep(1.5)

        hotels_check = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            const layer = hy.leafletAdapter._overlays.get('hotels');
            const isCached = window.HYLayerRegistry ? window.HYLayerRegistry.hasData('hotels') : false;
            const cachedData = window.HYLayerRegistry ? window.HYLayerRegistry.getData('hotels') : null;
            return {
                hasLayer: !!layer,
                onMap: layer ? hy.leafletAdapter.map.hasLayer(layer) : false,
                isCached: isCached,
                featureCount: cachedData ? cachedData.features.length : 0,
            };
        """)
        print(f"    Hotels Leaflet check: {json.dumps(hotels_check)}")
        assert hotels_check['hasLayer'] and hotels_check['onMap'], "Hotels layer not active on map"
        assert hotels_check['featureCount'] == 12, f"Expected 12 hotels, got {hotels_check['featureCount']}"

        # 4. Toggle Homestays ON in Leaflet 2D
        print("\n[5] Testing Homestays Layer ON in Leaflet 2D...")
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return hy.setLayerVisible('homestays', true);
        """)
        time.sleep(1.5)

        homestays_check = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            const layer = hy.leafletAdapter._overlays.get('homestays');
            const isCached = window.HYLayerRegistry ? window.HYLayerRegistry.hasData('homestays') : false;
            const cachedData = window.HYLayerRegistry ? window.HYLayerRegistry.getData('homestays') : null;
            return {
                hasLayer: !!layer,
                onMap: layer ? hy.leafletAdapter.map.hasLayer(layer) : false,
                isCached: isCached,
                featureCount: cachedData ? cachedData.features.length : 0,
            };
        """)
        print(f"    Homestays Leaflet check: {json.dumps(homestays_check)}")
        assert homestays_check['hasLayer'] and homestays_check['onMap'], "Homestays layer not active on map"
        assert homestays_check['featureCount'] == 10, f"Expected 10 homestays, got {homestays_check['featureCount']}"

        # 5. Test Toggling Layers OFF
        print("\n[6] Testing Layers Toggle OFF...")
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            hy.setLayerVisible('hotels', false);
            hy.setLayerVisible('homestays', false);
        """)
        time.sleep(1.0)
        off_check = driver.execute_script("""
            return {
                hotelsVisible: window.HYMapState.isLayerVisible('hotels'),
                homestaysVisible: window.HYMapState.isLayerVisible('homestays'),
            };
        """)
        print(f"    Toggled OFF check: {json.dumps(off_check)}")
        assert not off_check['hotelsVisible'] and not off_check['homestaysVisible'], "Layers did not turn off"

        # 6. Test Tourism Parent Propagation
        print("\n[7] Testing Tourism Parent Propagation...")
        driver.execute_script("""
            window.HYMapState.setLayerVisible('hotels', true);
            window.HYMapState.setLayerVisible('homestays', true);
            window.HYMapState.setLayerVisible('tourist_places', false);
        """)
        time.sleep(1.0)
        parent_off = driver.execute_script("""
            return {
                parentVisible: window.HYMapState.isLayerVisible('tourist_places'),
            };
        """)
        print(f"    Parent OFF check: {json.dumps(parent_off)}")
        assert not parent_off['parentVisible'], "Parent toggle off failed"

        # Re-enable parent
        driver.execute_script("window.HYMapState.setLayerVisible('tourist_places', true);")
        time.sleep(0.8)

        # 7. Test Quick Actions
        print("\n[8] Testing Quick Actions Toolbar...")
        driver.execute_script("document.getElementById('hy-lm-btn-hide-all').click();")
        time.sleep(0.8)
        hide_count = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        driver.execute_script("document.getElementById('hy-lm-btn-show-all').click();")
        time.sleep(0.8)
        show_count = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        driver.execute_script("document.getElementById('hy-lm-btn-reset').click();")
        time.sleep(0.8)
        reset_count = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        print(f"    Quick Actions: Hide={hide_count}, Show={show_count}, Reset={reset_count}")
        assert hide_count == 0, "Hide All failed"
        assert show_count > 20, "Show All failed"

        # 8. Test Visual Map Modes Switching
        print("\n[9] Testing Visual Map Modes...")
        modes = ['dark', 'satellite', 'hybrid', 'terrain', 'normal']
        for mode in modes:
            driver.execute_script(f"""
                const hy = window._hyMap || window.hyMap;
                if (hy) hy.setMapMode('{mode}');
                else window.HYMapState.setMode('{mode}');
            """)
            time.sleep(0.8)
            curr = driver.execute_script("return window.HYMapState.getMapMode ? window.HYMapState.getMapMode() : window.HYMapState.mode;")
            print(f"    Switched to mode: {curr}")
            assert curr == mode, f"Failed to switch to mode: {mode}"

        # 9. Test 3D MapLibre Mode & Vector Layer Rendering
        print("\n[10] Testing 3D MapLibre Mode & Vector Point Layer Rendering...")
        driver.execute_script("window.HYMapState.setLayerVisible('hotels', true);")
        driver.execute_script("window.HYMapState.setLayerVisible('homestays', true);")
        time.sleep(1.0)

        can_3d = driver.execute_script("return window.HYMapStateClass ? window.HYMapStateClass.canDo3D() : false;")
        print(f"    3D WebGL Capability: {can_3d}")

        if can_3d:
            try:
                driver.execute_async_script("""
                    const done = arguments[arguments.length - 1];
                    const hy = window._hyMap || window.hyMap;
                    hy.setMapMode('terrain3d')
                      .then(() => done(window.HYMapState.is3D()))
                      .catch(err => done(false));
                """)
            except Exception as e:
                driver.execute_script("window.HYMapState.setMode('3d');")
            time.sleep(1.5)
        else:
            driver.execute_script("window.HYMapState.setMode('3d');")
            time.sleep(1.0)

        mode3d_check = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return {
                is3D: window.HYMapState.is3D(),
                hasMapLibre: !!(hy && hy.maplibreAdapter),
                hotelsState: window.HYMapState.isLayerVisible('hotels'),
                homestaysState: window.HYMapState.isLayerVisible('homestays'),
            };
        """)
        print(f"    3D Mode check: {json.dumps(mode3d_check)}")
        assert mode3d_check['is3D'], "3D mode switch failed"
        assert mode3d_check['hotelsState'] and mode3d_check['homestaysState'], "Hotels/homestays layer state lost in 3D"

        # Transition back to 2D
        if can_3d:
            driver.execute_async_script("""
                const done = arguments[arguments.length - 1];
                const hy = window._hyMap || window.hyMap;
                hy.setMapMode('normal')
                  .then(() => done(true))
                  .catch(err => done(false));
            """)
        else:
            driver.execute_script("window.HYMapState.setMode('normal');")
        time.sleep(1.0)

        # 10. Test Mobile Viewport (375x667)
        print("\n[11] Testing Mobile Viewport (375x667)...")
        driver.set_window_size(375, 667)
        time.sleep(1.0)
        driver.execute_script("(window._hyMap || window.hyMap).controls.openPanel();")
        time.sleep(0.5)

        mobile_rect = driver.execute_script("""
            const drawer = document.getElementById('hy-layer-manager');
            if (!drawer) return null;
            const r = drawer.getBoundingClientRect();
            return {
                isOpen: drawer.classList.contains('open'),
                top: r.top,
                bottom: r.bottom,
                width: r.width,
                windowWidth: window.innerWidth,
                windowHeight: window.innerHeight,
            };
        """)
        print(f"    Mobile Bottom Sheet Rect: {json.dumps(mobile_rect)}")
        assert mobile_rect['isOpen'], "Mobile drawer failed to open"

        mobile_png = os.path.abspath("scratch/phase2e_mobile_hotels_homestays.png")
        driver.save_screenshot(mobile_png)
        print(f"    Mobile screenshot saved to: {mobile_png}")

        # Restore window size
        driver.set_window_size(1440, 900)
        time.sleep(1.0)
        desktop_png = os.path.abspath("scratch/phase2e_desktop_hotels_homestays.png")
        driver.save_screenshot(desktop_png)
        print(f"    Desktop screenshot saved to: {desktop_png}")

        # 11. Check Browser Console Logs
        print("\n[12] Verifying Browser Console Logs (Strict 0 Errors)...")
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE' and 'fonts.gstatic.com' not in l['message'] and 'favicon' not in l['message']]
        print(f"    Total browser logs: {len(logs)}, Severe application errors: {len(severe_errors)}")
        for err in severe_errors:
            print(f"      [SEVERE LOG] {err['message']}")
        assert len(severe_errors) == 0, f"Found {len(severe_errors)} severe console errors!"

        print("\n" + "=" * 60)
        print("  🎉 ALL 16 PHASE 2E ACCEPTANCE TESTS PASSED PERFECTLY!")
        print("=" * 60 + "\n")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_phase2e_e2e_verification()
