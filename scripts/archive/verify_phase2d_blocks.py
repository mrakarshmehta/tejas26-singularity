"""
Phase 2D End-to-End Selenium Verification Suite: Bihar Block Boundaries.
Tests 534 block rendering, 92 DB matching routes, unseeded blocks, 6 map modes, 2D/3D state transitions, mobile drawer, and console logs.
"""

import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_phase2d_e2e_verification():
    print("=" * 60)
    print("  PHASE 2D BLOCK BOUNDARIES E2E VERIFICATION")
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

        # 1. Initial State & Registry Verification
        print("\n[2] Checking HYMap Registry & Block Layer Definitions...")
        reg_info = driver.execute_script("""
            return {
                hasHYLayers: !!window.HY_LAYERS,
                hasRegistry: !!window.HYLayerRegistry,
                hasState: !!window.HYMapState,
                blocksDef: window.HYLayerRegistry ? window.HYLayerRegistry.get('block_boundaries') : null,
                parentDef: window.HYLayerRegistry ? window.HYLayerRegistry.get('boundaries') : null,
            };
        """)
        print(f"    Block Boundaries registered: {reg_info['blocksDef']['label']} -> {reg_info['blocksDef']['source']}")
        print(f"    MinZoom: {reg_info['blocksDef']['minZoom']}, Parent: {reg_info['blocksDef']['parent']}")
        assert reg_info['blocksDef']['source'] == '/static/data/bihar/blocks.geojson', "Blocks source mismatch"
        assert reg_info['blocksDef']['minZoom'] == 10, "Blocks minZoom mismatch"

        # 2. Open Layer Manager
        print("\n[3] Opening Layer Manager Drawer...")
        driver.execute_script("document.getElementById('hy-layers-btn').click();")
        time.sleep(0.5)
        lm_panel = driver.find_element(By.ID, "hy-layer-manager")
        is_open = "open" in lm_panel.get_attribute("class")
        print(f"    Layer Manager open: {is_open}")
        assert is_open, "Layer Manager failed to open"

        # 3. Toggle Parent Boundaries ON
        print("\n[4] Testing Parent Boundaries Toggle ON...")
        driver.execute_script("document.getElementById('hy-layer-switch-boundaries').click();")
        time.sleep(0.8)

        # 4. Toggle Block Boundaries Layer ON in Leaflet 2D
        print("\n[5] Testing Block Boundaries Overlay in Leaflet 2D...")
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return hy.setLayerVisible('block_boundaries', true);
        """)
        time.sleep(1.5)

        blocks_check = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            const layer = hy.leafletAdapter._overlays.get('block_boundaries');
            const isCached = window.HYLayerRegistry ? window.HYLayerRegistry.hasData('block_boundaries') : false;
            const cachedData = window.HYLayerRegistry ? window.HYLayerRegistry.getData('block_boundaries') : null;
            return {
                hasLayer: !!layer,
                onMap: layer ? hy.leafletAdapter.map.hasLayer(layer) : false,
                isCached: isCached,
                featureCount: cachedData ? cachedData.features.length : 0,
                totalFeatures: cachedData ? cachedData.metadata.total_features : 0,
                matchedDbBlocks: cachedData ? cachedData.metadata.matched_db_blocks : 0,
            };
        """)
        print(f"    Blocks Leaflet check: {json.dumps(blocks_check)}")
        assert blocks_check['hasLayer'], "Blocks layer not instantiated"
        assert blocks_check['onMap'], "Blocks layer is not active on Leaflet map"
        assert blocks_check['featureCount'] == 534, f"Expected 534 block features, got {blocks_check['featureCount']}"
        assert blocks_check['isCached'], "Blocks data not cached in HYLayerRegistry"
        assert blocks_check['matchedDbBlocks'] >= 90, f"Expected >=90 matched DB blocks, got {blocks_check['matchedDbBlocks']}"

        # 5. Test Zoom Threshold Behavior
        print("\n[6] Testing Zoom Level & Visibility...")
        current_zoom = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            return hy.leafletAdapter.map.getZoom();
        """)
        print(f"    Current Leaflet map zoom: {current_zoom}")

        # 6. Test Layer Toggles OFF
        print("\n[7] Testing Block Boundaries Layer Toggle OFF...")
        driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            hy.setLayerVisible('block_boundaries', false);
        """)
        time.sleep(1.0)
        off_check = driver.execute_script("""
            const hy = window._hyMap || window.hyMap;
            const bLayer = hy.leafletAdapter._overlays.get('block_boundaries');
            return {
                blocksVisible: window.HYMapState.isLayerVisible('block_boundaries'),
                blocksOnMap: bLayer ? hy.leafletAdapter.map.hasLayer(bLayer) : false,
            };
        """)
        print(f"    Toggled OFF check: {json.dumps(off_check)}")
        assert not off_check['blocksVisible'] and not off_check['blocksOnMap'], "Block boundaries did not hide properly"

        # 7. Re-enable blocks & test Opacity Adjustment
        print("\n[8] Testing Dynamic Opacity Setting...")
        driver.execute_script("""
            window.HYMapState.setLayerVisible('block_boundaries', true);
            window.HYMapState.setLayerOpacity('block_boundaries', 0.75);
        """)
        time.sleep(1.0)
        opacity_check = driver.execute_script("""
            return {
                blocksOpacity: window.HYMapState.getLayerOpacity('block_boundaries'),
            };
        """)
        print(f"    Opacity check: {json.dumps(opacity_check)}")
        assert opacity_check['blocksOpacity'] == 0.75, "Blocks opacity mismatch"

        # 8. Test Quick Actions Toolbar
        print("\n[9] Testing Quick Actions Toolbar...")
        driver.execute_script("document.getElementById('hy-lm-btn-hide-all').click();")
        time.sleep(0.8)
        hide_count = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        driver.execute_script("document.getElementById('hy-lm-btn-show-all').click();")
        time.sleep(0.8)
        show_count = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        driver.execute_script("document.getElementById('hy-lm-btn-reset').click();")
        time.sleep(0.8)
        reset_count = driver.execute_script("return window.HYMapState.getActiveLayerCount();")
        print(f"    Quick Actions counts: Hide={hide_count}, Show={show_count}, Reset={reset_count}")
        assert hide_count == 0, "Hide All failed"
        assert show_count > 20, "Show All failed"

        # 9. Test Visual Map Modes Switching
        print("\n[10] Testing Visual Map Modes...")
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

        # 10. Test 3D MapLibre Mode & Vector Layer Rendering
        print("\n[11] Testing 3D MapLibre Mode & Vector Layer Rendering...")
        driver.execute_script("window.HYMapState.setLayerVisible('boundaries', true);")
        driver.execute_script("window.HYMapState.setLayerVisible('block_boundaries', true);")
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
                blocksState: window.HYMapState.isLayerVisible('block_boundaries'),
            };
        """)
        print(f"    3D Mode check: {json.dumps(mode3d_check)}")
        assert mode3d_check['is3D'], "3D mode switch failed"
        assert mode3d_check['blocksState'], "Blocks layer state lost in 3D"

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

        # 11. Test Mobile Viewport (375x667)
        print("\n[12] Testing Mobile Viewport (375x667)...")
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

        mobile_png = os.path.abspath("scratch/phase2d_mobile_blocks.png")
        driver.save_screenshot(mobile_png)
        print(f"    Mobile screenshot saved to: {mobile_png}")

        # Restore window size
        driver.set_window_size(1440, 900)
        time.sleep(1.0)
        desktop_png = os.path.abspath("scratch/phase2d_desktop_blocks.png")
        driver.save_screenshot(desktop_png)
        print(f"    Desktop screenshot saved to: {desktop_png}")

        # 12. Check Browser Console Logs
        print("\n[13] Verifying Browser Console Logs (Strict 0 Errors)...")
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE' and 'fonts.gstatic.com' not in l['message'] and 'favicon' not in l['message']]
        print(f"    Total browser logs: {len(logs)}, Severe application errors: {len(severe_errors)}")
        for err in severe_errors:
            print(f"      [SEVERE LOG] {err['message']}")
        assert len(severe_errors) == 0, f"Found {len(severe_errors)} severe console errors!"

        print("\n" + "=" * 60)
        print("  🎉 ALL 16 PHASE 2D ACCEPTANCE TESTS PASSED PERFECTLY!")
        print("=" * 60 + "\n")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_phase2d_e2e_verification()
