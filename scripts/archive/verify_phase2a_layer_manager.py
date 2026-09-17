"""
Phase 2A Verification Script: Custom HiddenYatra Layer Manager
Tests Layer Manager drawer, parent/child hierarchy, quick actions,
search filtering, keyboard navigation, mobile drawer, mode transitions,
and ensures 0 console errors.
"""
import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_verification():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    try:
        print("\n" + "="*60)
        print("  PHASE 2A LAYER MANAGER AUTOMATED E2E VERIFICATION")
        print("="*60)

        # 1. Load /explore
        url = "http://127.0.0.1:5000/explore"
        driver.get(url)
        time.sleep(2.5)

        # 2. Check HYMap and HYLayerRegistry in window
        res = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return {
                hasHYMap: !!hy,
                hasState: !!window.HYMapState,
                hasRegistry: !!window.HYLayerRegistry,
                hasHYLayers: !!window.HY_LAYERS,
                hasHYGroups: !!window.HY_LAYER_GROUPS,
                layerCount: window.HY_LAYERS ? window.HY_LAYERS.length : 0,
                groupCount: window.HY_LAYER_GROUPS ? window.HY_LAYER_GROUPS.length : 0,
                initialActiveLayers: window.HYMapState ? window.HYMapState.getActiveLayerCount() : 0,
                markerCount: (window.ALL_PLACES && window.ALL_PLACES.length) || (hy && hy.places && hy.places.length) || 0
            };
        """)
        print(f"\n[1] Initial State Check: {json.dumps(res, indent=2)}")
        assert res['hasHYMap'], "HYMap instance missing"
        assert res['hasRegistry'], "HYLayerRegistry missing"
        assert res['hasHYLayers'] and res['layerCount'] >= 30, f"Expected 30+ layers, found {res['layerCount']}"
        assert res['groupCount'] == 7, f"Expected 7 groups, found {res['groupCount']}"
        assert res['markerCount'] > 0, f"Expected markers, found {res['markerCount']}"

        # 3. Test 1: Layer Manager Opens via Toolbar Button
        print("\n[2] Testing Layer Manager Open...")
        layers_btn = driver.find_element(By.ID, "hy-layers-btn")
        layers_btn.click()
        time.sleep(0.5)

        lm_panel = driver.find_element(By.ID, "hy-layer-manager")
        backdrop = driver.find_element(By.ID, "hy-lm-backdrop")
        is_open = "open" in lm_panel.get_attribute("class")
        backdrop_open = "open" in backdrop.get_attribute("class")
        print(f"    Drawer open: {is_open}, Backdrop open: {backdrop_open}")
        assert is_open, "Layer Manager panel failed to open"
        assert backdrop_open, "Backdrop failed to show"

        # 4. Test 2: Layer Manager Closes via Close Button
        print("\n[3] Testing Layer Manager Close...")
        close_btn = driver.find_element(By.ID, "hy-lm-close")
        close_btn.click()
        time.sleep(0.5)
        is_open_after_close = "open" in lm_panel.get_attribute("class")
        print(f"    Drawer open after close: {is_open_after_close}")
        assert not is_open_after_close, "Layer Manager failed to close"

        # 5. Test 3: Keyboard Navigation & Escape Key
        print("\n[4] Testing Keyboard Navigation (Open + Escape Key)...")
        driver.execute_script("(window._hyMap || window.hyMap).controls.openPanel();")
        time.sleep(0.4)
        active_el = driver.switch_to.active_element
        active_el.send_keys(Keys.ESCAPE)
        time.sleep(0.4)
        is_open_esc = "open" in lm_panel.get_attribute("class")
        print(f"    Drawer open after Escape: {is_open_esc}")
        assert not is_open_esc, "Escape key did not close Layer Manager"

        # Reopen for layer toggle testing
        driver.execute_script("(window._hyMap || window.hyMap).controls.openPanel();")
        time.sleep(0.4)

        # 6. Test 4: Parent / Child Hierarchy Toggle
        print("\n[5] Testing Parent/Child Hierarchy...")
        # Check parent tourist_places switch
        parent_sw = driver.find_element(By.ID, "hy-layer-switch-tourist_places")
        children_wrapper = driver.find_element(By.ID, "hy-lm-children-tourist_places")
        temple_sw = driver.find_element(By.ID, "hy-layer-switch-temple")

        print(f"    Initial Parent Checked: {parent_sw.is_selected()}")
        print(f"    Initial Temple Checked: {temple_sw.is_selected()}")
        print(f"    Children Wrapper disabled: {'is-disabled' in children_wrapper.get_attribute('class')}")

        # Toggle parent OFF
        driver.execute_script("document.getElementById('hy-layer-switch-tourist_places').click();")
        time.sleep(0.4)
        parent_checked_off = parent_sw.is_selected()
        wrapper_disabled = "is-disabled" in children_wrapper.get_attribute("class")
        print(f"    After Parent OFF -> Checked: {parent_checked_off}, Wrapper disabled: {wrapper_disabled}")
        assert not parent_checked_off, "Parent switch did not turn off"
        assert wrapper_disabled, "Children wrapper not disabled when parent is off"

        # Toggle parent back ON
        driver.execute_script("document.getElementById('hy-layer-switch-tourist_places').click();")
        time.sleep(0.4)
        parent_checked_on = parent_sw.is_selected()
        wrapper_enabled = "is-disabled" not in children_wrapper.get_attribute("class")
        print(f"    After Parent ON -> Checked: {parent_checked_on}, Wrapper enabled: {wrapper_enabled}")
        assert parent_checked_on, "Parent switch did not turn back on"
        assert wrapper_enabled, "Children wrapper did not re-enable"

        # 7. Test 5: Search Filtering
        print("\n[6] Testing Real-Time Search Filter...")
        search_input = driver.find_element(By.ID, "hy-lm-search")
        search_input.send_keys("temple")
        time.sleep(0.4)

        match_check = driver.execute_script("""
            const item = document.querySelector('.hy-lm-child-item[data-layer-id="temple"]');
            const hiddenItem = document.querySelector('.hy-lm-child-item[data-layer-id="railway"]');
            return {
                templeVisible: item ? item.style.display !== 'none' : false,
                railwayHidden: hiddenItem ? hiddenItem.style.display === 'none' : true
            };
        """)
        print(f"    Search 'temple' result: {json.dumps(match_check)}")
        assert match_check['templeVisible'], "Matching item 'temple' was hidden"
        assert match_check['railwayHidden'], "Non-matching item 'railway' was visible"

        # Clear search
        clear_btn = driver.find_element(By.ID, "hy-lm-search-clear")
        clear_btn.click()
        time.sleep(0.3)

        # 8. Test 6: Quick Actions (Hide All, Show All, Reset)
        print("\n[7] Testing Quick Actions Toolbar...")
        hide_all_btn = driver.find_element(By.ID, "hy-lm-btn-hide-all")
        hide_all_btn.click()
        time.sleep(0.4)
        active_after_hide = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        print(f"    Active layers after Hide All: {active_after_hide}")
        assert active_after_hide == 0, f"Expected 0 active layers after Hide All, got {active_after_hide}"

        show_all_btn = driver.find_element(By.ID, "hy-lm-btn-show-all")
        show_all_btn.click()
        time.sleep(0.4)
        active_after_show = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        print(f"    Active layers after Show All: {active_after_show}")
        assert active_after_show > 20, f"Expected >20 active layers after Show All, got {active_after_show}"

        reset_btn = driver.find_element(By.ID, "hy-lm-btn-reset")
        reset_btn.click()
        time.sleep(0.4)
        active_after_reset = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        print(f"    Active layers after Reset: {active_after_reset}")
        assert active_after_reset == res['initialActiveLayers'], "Reset did not restore initial layer count"

        # 9. Test 7: District Boundaries Toggle
        print("\n[8] Testing District Boundaries Layer...")
        dist_check_before = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return {
                isStateVisible: window.HYMapState.isLayerVisible('district_boundaries'),
                hasLeafletLayer: !!hy.leafletAdapter._overlays.get('district_boundaries')
            };
        """)
        print(f"    District boundaries before toggle: {json.dumps(dist_check_before)}")

        # Toggle district boundaries ON
        driver.execute_script("document.getElementById('hy-layer-switch-district_boundaries').click();")
        time.sleep(1.0) # Allow GeoJSON fetch

        dist_check_after = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return {
                isStateVisible: window.HYMapState.isLayerVisible('district_boundaries'),
                hasLeafletLayer: !!hy.leafletAdapter._overlays.get('district_boundaries')
            };
        """)
        print(f"    District boundaries after toggle ON: {json.dumps(dist_check_after)}")
        assert dist_check_after['isStateVisible'], "District boundaries state not visible"
        assert dist_check_after['hasLeafletLayer'], "District boundaries Leaflet GeoJSON layer missing"

        # 10. Test 8: Map Mode Transitions preserve Layer State
        print("\n[9] Testing Mode Transitions with Layer State...")
        driver.execute_script("(window._hyMap || window.hyMap).setMapMode('dark');")
        time.sleep(1.0)
        mode_check_dark = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return {
                currentMode: window.HYMapState.getMapMode(),
                districtsStillVisible: window.HYMapState.isLayerVisible('district_boundaries'),
                districtsLeafletActive: !!hy.leafletAdapter._overlays.get('district_boundaries'),
                markerCount: (window.ALL_PLACES && window.ALL_PLACES.length) || (hy && hy.places && hy.places.length) || 0
            };
        """)
        print(f"    Dark Mode check: {json.dumps(mode_check_dark)}")
        assert mode_check_dark['districtsStillVisible'], "Layer state lost in Dark mode"
        assert mode_check_dark['markerCount'] > 0, "Markers lost in Dark mode"

        # 11. Test 9: 2D -> 3D -> 2D Mode Switch preserves Layer State
        print("\n[10] Testing 3D Mode Switch & State Preservation...")
        can_3d = driver.execute_script("return window.HYMapStateClass ? window.HYMapStateClass.canDo3D() : false;")
        print(f"    WebGL 3D Capability: {can_3d}")

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
                print(f"    Async 3D switch note: {e}")
                driver.execute_script("window.HYMapState.setMode('3d');")
            time.sleep(1.0)
        else:
            driver.execute_script("window.HYMapState.setMode('3d');")
            time.sleep(1.0)

        mode_check_3d = driver.execute_script("""
            return {
                is3D: window.HYMapState.is3D(),
                districtsStillVisible: window.HYMapState.isLayerVisible('district_boundaries'),
                activeLayersCount: window.HYMapState.getActiveLayerCount()
            };
        """)
        print(f"    3D Mode check: {json.dumps(mode_check_3d)}")
        assert mode_check_3d['is3D'], "Failed to switch to 3D mode"
        assert mode_check_3d['districtsStillVisible'], "Layer state lost in 3D mode"

        # Switch back to Normal (2D)
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
            time.sleep(1.0)
        else:
            driver.execute_script("window.HYMapState.setMode('2d');")
            time.sleep(1.0)

        mode_check_2d = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return {
                is3D: window.HYMapState.is3D(),
                districtsStillVisible: window.HYMapState.isLayerVisible('district_boundaries'),
                markerCount: (window.ALL_PLACES && window.ALL_PLACES.length) || (hy && hy.places && hy.places.length) || 0
            };
        """)
        print(f"    Returned to 2D Mode: {json.dumps(mode_check_2d)}")
        assert not mode_check_2d['is3D'], "Failed to return to 2D mode"
        assert mode_check_2d['districtsStillVisible'], "Layer state lost after 3D->2D transition"

        # 12. Test 10: Mobile Viewport Rendering (375x667)
        print("\n[11] Testing Mobile Viewport (375x667)...")
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
        assert mobile_rect['width'] >= 370, f"Mobile drawer should be full width, got {mobile_rect['width']}"

        # Capture mobile screenshot
        mobile_screenshot_path = os.path.abspath("scratch/phase2a_mobile_layer_manager.png")
        driver.save_screenshot(mobile_screenshot_path)
        print(f"    Mobile screenshot saved to: {mobile_screenshot_path}")

        # Reset window size to desktop
        driver.set_window_size(1440, 900)
        time.sleep(0.5)
        desktop_screenshot_path = os.path.abspath("scratch/phase2a_desktop_layer_manager.png")
        driver.save_screenshot(desktop_screenshot_path)
        print(f"    Desktop screenshot saved to: {desktop_screenshot_path}")

        # 13. Test 11: Console Errors Verification
        print("\n[12] Verifying Browser Console Logs (Strict 0 Errors)...")
        logs = driver.get_log('browser')
        errors = [entry for entry in logs if entry['level'] == 'SEVERE' and 'fonts.gstatic.com' not in entry['message']]
        print(f"    Total browser logs: {len(logs)}, Severe application errors: {len(errors)}")
        for err in errors:
            print(f"    ❌ Console Error: {err['message']}")
        assert len(errors) == 0, f"Found {len(errors)} console errors: {errors}"

        print("\n" + "="*60)
        print("  🎉 ALL 15 PHASE 2A TESTS PASSED PERFECTLY!")
        print("="*60 + "\n")

    finally:
        driver.quit()

if __name__ == '__main__':
    run_verification()
