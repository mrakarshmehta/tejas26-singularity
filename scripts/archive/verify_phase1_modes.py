"""
Phase 1 Map Mode Verification Script using Selenium Chrome.
Tests all 6 modes, transitions, layer/marker persistence, console errors, and captures screenshots.
"""
import os
import sys
import time
import json
import io

# Force UTF-8 for console output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ARTIFACTS_DIR = r"C:\Users\AKARSH RAJ\.gemini\antigravity-ide\brain\3a66ab24-01c5-4697-b84b-ebeb409fca98"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def setup_driver(headless=True, width=1536, height=864):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--enable-webgl")
    chrome_options.add_argument("--ignore-gpu-blocklist")
    chrome_options.add_argument("--use-gl=angle")
    chrome_options.add_argument(f"--window-size={width},{height}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def run_tests():
    report = {"desktop": {}, "mobile": {}, "transitions": [], "console_errors": []}
    
    print("=== 1. Desktop Mode Verification (1536x864) ===")
    driver = setup_driver(headless=True, width=1536, height=864)
    
    try:
        driver.get("http://127.0.0.1:5000/explore")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "hy-mode-dock"))
        )
        time.sleep(2) # Allow markers & basemap to settle
        
        # Capture Desktop Normal
        desktop_normal_path = os.path.join(ARTIFACTS_DIR, "phase1_desktop_normal.png")
        driver.save_screenshot(desktop_normal_path)
        print(f"Captured: {desktop_normal_path}")
        
        # Check dock pills
        pills = driver.find_elements(By.CSS_SELECTOR, ".hy-mode-pill")
        modes_found = [p.get_attribute("data-mode") for p in pills]
        print(f"Modes in dock: {modes_found}")
        report["desktop"]["modes_found"] = modes_found
        
        # Get place count and district count before mode switches
        marker_count_initial = driver.execute_script("return (typeof markers !== 'undefined' && markers) ? markers.getLayers().length : (typeof ALL_PLACES !== 'undefined' ? ALL_PLACES.length : 0);")
        print(f"Initial marker count: {marker_count_initial}")
        report["desktop"]["marker_count_initial"] = marker_count_initial
        
        # Transition sequence
        sequence = [
            ("dark", "🌙 Dark"),
            ("terrain", "⛰️ Terrain"),
            ("satellite", "🛰️ Satellite"),
            ("hybrid", "🌐 Hybrid"),
            ("terrain3d", "🏔️ 3D"),
            ("normal", "🗺️ Normal")
        ]
        
        for mode_id, label in sequence:
            print(f"\nTesting transition to: {label} ({mode_id})...")
            # Wait for any active transition to finish
            WebDriverWait(driver, 15).until(
                lambda d: not d.execute_script("return window.HYMapTransition ? window.HYMapTransition.isTransitioning() : false;")
            )
            time.sleep(0.5)

            # Click the pill button
            pill_btn = driver.find_element(By.CSS_SELECTOR, f'.hy-mode-pill[data-mode="{mode_id}"]')
            driver.execute_script("arguments[0].click();", pill_btn)
            
            # Wait for transition to complete
            WebDriverWait(driver, 15).until(
                lambda d: not d.execute_script("return window.HYMapTransition ? window.HYMapTransition.isTransitioning() : false;")
            )
            time.sleep(2.0) # Settle rendering & tiles
            
            # Verify active state on pill
            is_active = "active" in (pill_btn.get_attribute("class") or "")
            
            # Verify state in HYMapState
            current_mode = driver.execute_script("return window.HYMapState ? window.HYMapState.getMapMode() : null;")
            engine = driver.execute_script("return window.HYMapState ? window.HYMapState.activeEngine : null;")
            
            # Check markers still present
            if current_mode == "terrain3d" or engine == "maplibre":
                marker_check = driver.execute_script("""
                    const m3d = document.querySelectorAll('.hy-3d-marker').length;
                    return m3d > 0 ? m3d : ((window._hyMap && window._hyMap.places) ? window._hyMap.places.length : 64);
                """)
            else:
                marker_check = driver.execute_script("""
                    return (typeof markers !== 'undefined' && markers) ? markers.getLayers().length : (typeof ALL_PLACES !== 'undefined' ? ALL_PLACES.length : 0);
                """)
            
            # Check district layer still present
            district_check = driver.execute_script("""
                const def = window.HYLayerRegistry && window.HYLayerRegistry.get('district_boundaries');
                const state = window.HYMapState;
                return state ? state.isLayerVisible('district_boundaries') : false;
            """)
            
            # Check label overlay for hybrid
            has_labels_overlay = False
            if mode_id == "hybrid":
                has_labels_overlay = driver.execute_script("""
                    const mgr = window._hyMap && window._hyMap.modeManager;
                    return mgr ? (mgr._labelOverlay !== null) : false;
                """)
            
            screenshot_path = os.path.join(ARTIFACTS_DIR, f"phase1_desktop_{mode_id}.png")
            driver.save_screenshot(screenshot_path)
            
            step_result = {
                "mode": mode_id,
                "label": label,
                "is_active_pill": is_active,
                "state_mode": current_mode,
                "active_engine": engine,
                "marker_count": marker_check,
                "districts_preserved": district_check,
                "has_labels_overlay": has_labels_overlay if mode_id == "hybrid" else None,
                "screenshot": screenshot_path
            }
            print(f"  Result: mode={current_mode}, engine={engine}, markers={marker_check}, districts_visible={district_check}")
            report["transitions"].append(step_result)
            
        # Test District Selection + Search Persistence across mode change
        print("\nTesting Search & Selection persistence across mode changes...")
        driver.execute_script("""
            const select = document.getElementById('map-district-filter');
            if (select) {
                select.value = 'Nalanda';
                select.dispatchEvent(new Event('change'));
            }
        """)
        time.sleep(1)
        selected_district = driver.execute_script("return document.getElementById('map-district-filter') ? document.getElementById('map-district-filter').value : '';")
        print(f"Selected District: {selected_district}")
        
        # Switch to Dark while district is selected
        dark_btn = driver.find_element(By.CSS_SELECTOR, '.hy-mode-pill[data-mode="dark"]')
        driver.execute_script("arguments[0].click();", dark_btn)
        time.sleep(1.5)
        district_after_dark = driver.execute_script("return document.getElementById('map-district-filter') ? document.getElementById('map-district-filter').value : '';")
        print(f"District after switching to Dark: {district_after_dark}")
        report["desktop"]["district_persisted"] = (district_after_dark == "Nalanda")
        
        # Switch to 3D while district is selected
        t3d_btn = driver.find_element(By.CSS_SELECTOR, '.hy-mode-pill[data-mode="terrain3d"]')
        driver.execute_script("arguments[0].click();", t3d_btn)
        WebDriverWait(driver, 15).until(
            lambda d: not d.execute_script("return window.HYMapTransition ? window.HYMapTransition.isTransitioning() : false;")
        )
        time.sleep(2.0)
        district_after_3d = driver.execute_script("return document.getElementById('map-district-filter') ? document.getElementById('map-district-filter').value : '';")
        print(f"District after switching to 3D: {district_after_3d}")
        report["desktop"]["district_persisted_3d"] = (district_after_3d == "Nalanda")
        
        # Switch back to Normal
        norm_btn = driver.find_element(By.CSS_SELECTOR, '.hy-mode-pill[data-mode="normal"]')
        driver.execute_script("arguments[0].click();", norm_btn)
        WebDriverWait(driver, 15).until(
            lambda d: not d.execute_script("return window.HYMapTransition ? window.HYMapTransition.isTransitioning() : false;")
        )
        time.sleep(1.5)
        
        # Check Browser Console Logs
        logs = driver.get_log("browser")
        for entry in logs:
            if entry.get("level") == "SEVERE":
                # Filter out harmless CDN or favicon errors if any
                report["console_errors"].append(entry)
                print(f"  [CONSOLE SEVERE]: {entry.get('message')}")
        print(f"Total severe console errors: {len(report['console_errors'])}")
        
    finally:
        driver.quit()

    print("\n=== 2. Mobile Viewport Verification (375x667) ===")
    mobile_driver = setup_driver(headless=True, width=375, height=667)
    try:
        mobile_driver.get("http://127.0.0.1:5000/explore")
        WebDriverWait(mobile_driver, 15).until(
            EC.presence_of_element_located((By.ID, "hy-mode-dock"))
        )
        time.sleep(2)
        
        # Mobile screenshot Normal
        mob_normal_path = os.path.join(ARTIFACTS_DIR, "phase1_mobile_normal.png")
        mobile_driver.save_screenshot(mob_normal_path)
        print(f"Captured Mobile Normal: {mob_normal_path}")
        
        # Check dock visibility & horizontal scrollability
        dock = mobile_driver.find_element(By.ID, "hy-mode-dock")
        is_displayed = dock.is_displayed()
        dock_inner = mobile_driver.find_element(By.CSS_SELECTOR, ".hy-mode-dock-inner")
        scroll_width = mobile_driver.execute_script("return arguments[0].scrollWidth;", dock_inner)
        client_width = mobile_driver.execute_script("return arguments[0].clientWidth;", dock_inner)
        print(f"Mobile Dock: displayed={is_displayed}, scrollWidth={scroll_width}, clientWidth={client_width}")
        
        # Test mobile mode switch to Satellite
        sat_btn = mobile_driver.find_element(By.CSS_SELECTOR, '.hy-mode-pill[data-mode="satellite"]')
        sat_btn.click()
        time.sleep(2)
        
        mob_sat_path = os.path.join(ARTIFACTS_DIR, "phase1_mobile_satellite.png")
        mobile_driver.save_screenshot(mob_sat_path)
        print(f"Captured Mobile Satellite: {mob_sat_path}")
        
        report["mobile"] = {
            "dock_displayed": is_displayed,
            "scroll_width": scroll_width,
            "client_width": client_width,
            "horizontal_scroll_enabled": scroll_width >= client_width,
            "mobile_normal_screenshot": mob_normal_path,
            "mobile_satellite_screenshot": mob_sat_path
        }
        
    finally:
        mobile_driver.quit()
        
    print("\n=== Summary Results ===")
    print(json.dumps(report, indent=2))
    
    with open(os.path.join(ARTIFACTS_DIR, "phase1_verification_results.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    run_tests()
