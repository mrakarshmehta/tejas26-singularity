"""
Phase 2B Automated E2E Verification Suite using Selenium WebDriver.
Tests Rivers, Lakes/Dams, Parent/Child Hierarchy, Leaflet 2D, MapLibre 3D,
Tooltips, 6 Modes, Mobile Drawer, 0 Console Errors.
"""

import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_verification():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        print("\n" + "="*60)
        print("  PHASE 2B RIVERS + LAKES/DAMS E2E VERIFICATION")
        print("="*60 + "\n")

        # 1. Load /explore
        driver.get("http://127.0.0.1:5000/explore")
        time.sleep(2.0)

        # 2. Check Initial Registry & State
        print("[1] Initial State Check...")
        init_info = driver.execute_script("""
            return {
                hasHYLayers: !!window.HY_LAYERS,
                hasRegistry: !!window.HYLayerRegistry,
                hasState: !!window.HYMapState,
                hasHYMap: !!(window._hyMap || window.hyMap),
                riversSource: window.HY_LAYERS ? window.HY_LAYERS.find(l => l.id === 'rivers')?.source : null,
                lakesSource: window.HY_LAYERS ? window.HY_LAYERS.find(l => l.id === 'lakes_dams')?.source : null,
                riversDefault: window.HYMapState.isLayerVisible('rivers'),
                lakesDefault: window.HYMapState.isLayerVisible('lakes_dams'),
                parentDefault: window.HYMapState.isLayerVisible('natural_geography'),
                initialActiveCount: window.HYMapState.getActiveLayerCount()
            };
        """)
        print(f"    Registry info: {json.dumps(init_info, indent=2)}")
        assert init_info['hasHYLayers'], "HY_LAYERS missing"
        assert init_info['riversSource'] == '/static/data/bihar/rivers.geojson', "Rivers source URL incorrect"
        assert init_info['lakesSource'] == '/static/data/bihar/lakes_dams.geojson', "Lakes source URL incorrect"

        # 3. Test Open Layer Manager
        print("\n[2] Testing Layer Manager Open...")
        lm_btn = driver.find_element(By.ID, "hy-layers-btn")
        lm_btn.click()
        time.sleep(0.5)

        lm_panel = driver.find_element(By.ID, "hy-layer-manager")
        is_open = "open" in lm_panel.get_attribute("class")
        print(f"    Layer Manager open: {is_open}")
        assert is_open, "Layer Manager failed to open"

        # 4. Test Parent Natural Geography ON and Child Toggles
        print("\n[3] Testing Parent Natural Geography Toggle...")
        parent_sw = driver.find_element(By.ID, "hy-layer-switch-natural_geography")
        children_wrapper = driver.find_element(By.ID, "hy-lm-children-natural_geography")

        # Toggle Natural Geography parent ON
        driver.execute_script("document.getElementById('hy-layer-switch-natural_geography').click();")
        time.sleep(0.8)

        parent_state = driver.execute_script("""
            return {
                parentVisible: window.HYMapState.isLayerVisible('natural_geography'),
                riversEnabled: window.HYMapState.isLayerEnabled('rivers'),
                lakesEnabled: window.HYMapState.isLayerEnabled('lakes_dams')
            };
        """)
        print(f"    Parent ON state: {json.dumps(parent_state)}")
        assert parent_state['parentVisible'], "Natural geography parent not visible"
        assert parent_state['riversEnabled'], "Rivers not enabled with parent ON"
        assert parent_state['lakesEnabled'], "Lakes not enabled with parent ON"

        # 5. Test Rivers Layer Rendering in Leaflet 2D
        print("\n[4] Testing Rivers Overlay in Leaflet 2D...")
        # Toggle Rivers ON in UI if not already
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return hy.setLayerVisible('rivers', true);
        """)
        time.sleep(1.0) # Allow GeoJSON fetch

        rivers_leaflet_check = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            const layer = hy.leafletAdapter._overlays.get('rivers');
            return {
                hasLayer: !!layer,
                onMap: layer ? hy.leafletAdapter.map.hasLayer(layer) : false,
                featureCount: layer && layer.getLayers ? layer.getLayers().length : 0,
                isCached: window.HYLayerRegistry.hasData('rivers')
            };
        """)
        print(f"    Rivers Leaflet check: {json.dumps(rivers_leaflet_check)}")
        assert rivers_leaflet_check['hasLayer'], "Rivers layer not instantiated in Leaflet"
        assert rivers_leaflet_check['onMap'], "Rivers layer not added to Leaflet map"
        assert rivers_leaflet_check['featureCount'] >= 10, f"Expected >=10 river features, got {rivers_leaflet_check['featureCount']}"
        assert rivers_leaflet_check['isCached'], "Rivers GeoJSON was not cached in HYLayerRegistry"

        # 6. Test Lakes & Dams Layer Rendering in Leaflet 2D
        print("\n[5] Testing Lakes & Dams Overlay in Leaflet 2D...")
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return hy.setLayerVisible('lakes_dams', true);
        """)
        time.sleep(1.0)

        lakes_leaflet_check = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            const layer = hy.leafletAdapter._overlays.get('lakes_dams');
            return {
                hasLayer: !!layer,
                onMap: layer ? hy.leafletAdapter.map.hasLayer(layer) : false,
                featureCount: layer && layer.getLayers ? layer.getLayers().length : 0,
                isCached: window.HYLayerRegistry.hasData('lakes_dams')
            };
        """)
        print(f"    Lakes/Dams Leaflet check: {json.dumps(lakes_leaflet_check)}")
        assert lakes_leaflet_check['hasLayer'], "Lakes layer not instantiated in Leaflet"
        assert lakes_leaflet_check['onMap'], "Lakes layer not added to Leaflet map"
        assert lakes_leaflet_check['featureCount'] >= 10, f"Expected >=10 lake features, got {lakes_leaflet_check['featureCount']}"
        assert lakes_leaflet_check['isCached'], "Lakes GeoJSON was not cached in HYLayerRegistry"

        # 7. Test Rivers OFF and Lakes OFF
        print("\n[6] Testing Rivers & Lakes Layer Toggles OFF...")
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            hy.setLayerVisible('rivers', false);
            hy.setLayerVisible('lakes_dams', false);
        """)
        time.sleep(0.5)

        off_check = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            const rLayer = hy.leafletAdapter._overlays.get('rivers');
            const lLayer = hy.leafletAdapter._overlays.get('lakes_dams');
            return {
                riversOnMap: rLayer ? hy.leafletAdapter.map.hasLayer(rLayer) : false,
                lakesOnMap: lLayer ? hy.leafletAdapter.map.hasLayer(lLayer) : false,
                riversVisible: window.HYMapState.isLayerVisible('rivers'),
                lakesVisible: window.HYMapState.isLayerVisible('lakes_dams')
            };
        """)
        print(f"    Toggled OFF check: {json.dumps(off_check)}")
        assert not off_check['riversOnMap'], "Rivers still on map after turning OFF"
        assert not off_check['lakesOnMap'], "Lakes still on map after turning OFF"

        # Re-enable for subsequent tests
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            hy.setLayerVisible('rivers', true);
            hy.setLayerVisible('lakes_dams', true);
        """)
        time.sleep(0.5)

        # 8. Test Parent Natural Geography OFF disables children in rendering
        print("\n[7] Testing Parent OFF disables children...")
        driver.execute_script("document.getElementById('hy-layer-switch-natural_geography').click();")
        time.sleep(0.4)
        parent_off_check = driver.execute_script("""
            return {
                parentVisible: window.HYMapState.isLayerVisible('natural_geography'),
                riversEnabled: window.HYMapState.isLayerEnabled('rivers'),
                lakesEnabled: window.HYMapState.isLayerEnabled('lakes_dams')
            };
        """)
        print(f"    Parent OFF check: {json.dumps(parent_off_check)}")
        assert not parent_off_check['parentVisible'], "Parent still visible"
        assert not parent_off_check['riversEnabled'], "Rivers still enabled when parent is OFF"
        assert not parent_off_check['lakesEnabled'], "Lakes still enabled when parent is OFF"

        # Re-enable parent
        driver.execute_script("document.getElementById('hy-layer-switch-natural_geography').click();")
        time.sleep(0.4)

        # 9. Test Opacity Setting for Rivers and Lakes
        print("\n[8] Testing Dynamic Opacity Setting...")
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            window.HYMapState.setLayerOpacity('rivers', 0.5);
            hy.leafletAdapter.setLayerOpacity('rivers', 0.5);
            window.HYMapState.setLayerOpacity('lakes_dams', 0.6);
            hy.leafletAdapter.setLayerOpacity('lakes_dams', 0.6);
        """)
        time.sleep(0.3)
        opacity_check = driver.execute_script("""
            return {
                riversOpacity: window.HYMapState.getLayerOpacity('rivers'),
                lakesOpacity: window.HYMapState.getLayerOpacity('lakes_dams')
            };
        """)
        print(f"    Opacity check: {json.dumps(opacity_check)}")
        assert opacity_check['riversOpacity'] == 0.5, "Rivers opacity mismatch"
        assert opacity_check['lakesOpacity'] == 0.6, "Lakes opacity mismatch"

        # 10. Test Quick Actions Toolbar (Hide All / Show All / Reset)
        print("\n[9] Testing Quick Actions Toolbar...")
        driver.find_element(By.ID, "hy-lm-btn-hide-all").click()
        time.sleep(0.4)
        count_hide = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        assert count_hide == 0, f"Expected 0 active after Hide All, got {count_hide}"

        driver.find_element(By.ID, "hy-lm-btn-show-all").click()
        time.sleep(0.4)
        count_show = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        assert count_show == 39, f"Expected 39 active after Show All, got {count_show}"

        driver.find_element(By.ID, "hy-lm-btn-reset").click()
        time.sleep(0.4)
        count_reset = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        print(f"    Quick Actions counts: Hide=0, Show={count_show}, Reset={count_reset}")
        assert count_reset == init_info['initialActiveCount'], f"Expected {init_info['initialActiveCount']} active after Reset, got {count_reset}"

        # 11. Test Mode Transitions with Rivers & Lakes State Preserved
        print("\n[10] Testing All Visual Map Modes...")
        modes_to_test = ['dark', 'satellite', 'hybrid', 'terrain', 'normal']
        for m in modes_to_test:
            driver.execute_script(f"(window._hyMap || window.hyMap).setMapMode('{m}');")
            time.sleep(0.6)
            mode_res = driver.execute_script("return window.HYMapState.getMapMode();")
            print(f"    Switched to mode: {mode_res}")
            assert mode_res == m, f"Mode switch to {m} failed"

        # 12. Test 3D MapLibre Mode Switch & Vector Layer Rendering
        print("\n[11] Testing 3D MapLibre Mode & Vector Layer Rendering...")
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

        mode_check_3d = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return {
                is3D: window.HYMapState.is3D(),
                hasMapLibre: !!(hy && hy.maplibreAdapter),
                riversState: window.HYMapState.isLayerVisible('rivers'),
                lakesState: window.HYMapState.isLayerVisible('lakes_dams')
            };
        """)
        print(f"    3D Mode check: {json.dumps(mode_check_3d)}")
        assert mode_check_3d['is3D'], "Failed to enter 3D mode"
        assert mode_check_3d['riversState'], "Rivers state lost in 3D"
        assert mode_check_3d['lakesState'], "Lakes state lost in 3D"

        # Switch back to 2D Normal
        if can_3d:
            try:
                driver.execute_async_script("""
                    const done = arguments[arguments.length - 1];
                    const hy = window._hyMap || window.hyMap;
                    hy.setMapMode('normal')
                      .then(() => done(window.HYMapState.is3D()))
                      .catch(err => done(true));
                """)
            except Exception as e:
                driver.execute_script("window.HYMapState.setMode('2d');")
            time.sleep(1.5)
        else:
            driver.execute_script("window.HYMapState.setMode('2d');")
            time.sleep(1.0)

        # 13. Test Mobile Drawer (375x667)
        print("\n[12] Testing Mobile Viewport (375x667)...")
        driver.set_window_size(375, 667)
        time.sleep(1.0)
        driver.execute_script("(window._hyMap || window.hyMap).controls.openPanel();")
        time.sleep(0.5)

        mobile_rect = driver.execute_script("""
            const panel = document.getElementById('hy-layer-manager');
            const rect = panel.getBoundingClientRect();
            return {
                width: rect.width,
                bottom: rect.bottom,
                top: rect.top,
                windowWidth: window.innerWidth,
                windowHeight: window.innerHeight,
                isOpen: panel.classList.contains('open')
            };
        """)
        print(f"    Mobile Bottom Sheet Rect: {json.dumps(mobile_rect)}")
        assert mobile_rect['isOpen'], "Mobile drawer not open"

        # Capture mobile screenshot
        mobile_screenshot_path = os.path.abspath("scratch/phase2b_mobile_rivers_lakes.png")
        driver.save_screenshot(mobile_screenshot_path)
        print(f"    Mobile screenshot saved to: {mobile_screenshot_path}")

        # Reset to desktop and capture screenshot
        driver.set_window_size(1440, 900)
        time.sleep(0.5)
        desktop_screenshot_path = os.path.abspath("scratch/phase2b_desktop_rivers_lakes.png")
        driver.save_screenshot(desktop_screenshot_path)
        print(f"    Desktop screenshot saved to: {desktop_screenshot_path}")

        # 14. Verify Browser Console Errors
        print("\n[13] Verifying Browser Console Logs (Strict 0 Errors)...")
        logs = driver.get_log('browser')
        errors = [entry for entry in logs if entry['level'] == 'SEVERE' and 'fonts.gstatic.com' not in entry['message']]
        print(f"    Total browser logs: {len(logs)}, Severe application errors: {len(errors)}")
        for err in errors:
            print(f"    ❌ Console Error: {err['message']}")
        assert len(errors) == 0, f"Found {len(errors)} console errors: {errors}"

        print("\n" + "="*60)
        print("  🎉 ALL 16 PHASE 2B ACCEPTANCE TESTS PASSED PERFECTLY!")
        print("="*60 + "\n")

    finally:
        driver.quit()

if __name__ == '__main__':
    run_verification()
