import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'http://127.0.0.1:5000'
ARTIFACT_DIR = r'C:\Users\AKARSH RAJ\.gemini\antigravity-ide\brain\135efbcd-8f42-408e-abf7-f6b2a19445bb'
os.makedirs(ARTIFACT_DIR, exist_ok=True)

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1400,1000')

driver = webdriver.Chrome(options=options)

try:
    print("1. Capturing Explore Map...")
    driver.get(f'{BASE_URL}/explore')
    time.sleep(2.5)
    # Select district Rohtas in filter
    driver.execute_script("""
        const sel = document.getElementById('map-district-filter');
        if (sel) {
            sel.value = 'Rohtas';
            sel.dispatchEvent(new Event('change'));
        }
    """)
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch4_explore_rohtas_filter.png'))
    print("  -> Saved batch4_explore_rohtas_filter.png")

    # Select district West Champaran
    driver.execute_script("""
        const sel = document.getElementById('map-district-filter');
        if (sel) {
            sel.value = 'West Champaran';
            sel.dispatchEvent(new Event('change'));
        }
    """)
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch4_explore_west_champaran.png'))
    print("  -> Saved batch4_explore_west_champaran.png")

    # 2. Capturing Place Detail: Jal Mandir, Pawapuri (Nalanda)
    print("2. Capturing Jal Mandir, Pawapuri detail page...")
    driver.get(f'{BASE_URL}/place/jal-mandir-pawapuri-nalanda')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch4_jal_mandir_detail_desktop.png'))
    print("  -> Saved batch4_jal_mandir_detail_desktop.png")

    # 3. Capturing Place Detail: Shergarh Fort (Rohtas)
    print("3. Capturing Shergarh Fort detail page...")
    driver.get(f'{BASE_URL}/place/shergarh-fort-rohtas')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch4_shergarh_fort_detail_desktop.png'))
    print("  -> Saved batch4_shergarh_fort_detail_desktop.png")

    # 4. Capturing District Page: Rohtas
    print("4. Capturing Rohtas District page...")
    driver.get(f'{BASE_URL}/state/bihar/rohtas')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch4_district_rohtas_desktop.png'))
    print("  -> Saved batch4_district_rohtas_desktop.png")

    # 5. Capturing Mobile Viewport (390x844): Kaimur Wildlife Sanctuary
    print("5. Capturing Mobile viewport for Kaimur Wildlife Sanctuary...")
    driver.set_window_size(390, 844)
    driver.get(f'{BASE_URL}/place/kaimur-wildlife-sanctuary-and-adhaura-hills-kaimur')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch4_mobile_kaimur_wildlife.png'))
    print("  -> Saved batch4_mobile_kaimur_wildlife.png")

    # Mobile scrolled
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch4_mobile_kaimur_wildlife_scrolled.png'))
    print("  -> Saved batch4_mobile_kaimur_wildlife_scrolled.png")

    print("\nALL SCREENSHOTS CAPTURED SUCCESSFULLY [OK]!")
finally:
    driver.quit()
