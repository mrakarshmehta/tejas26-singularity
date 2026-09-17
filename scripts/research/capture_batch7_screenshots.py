import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://127.0.0.1:5000'
ARTIFACT_DIR = r'C:\Users\AKARSH RAJ\.gemini\antigravity-ide\brain\135efbcd-8f42-408e-abf7-f6b2a19445bb'
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# ── DESKTOP OPTIONS ──
options_desktop = Options()
options_desktop.add_argument('--headless=new')
options_desktop.add_argument('--disable-gpu')
options_desktop.add_argument('--no-sandbox')
options_desktop.add_argument('--window-size=1400,1000')

driver = webdriver.Chrome(options=options_desktop)

try:
    # 1. Explore Map with Batch 7 Markers (e.g. West Champaran)
    print("1. Capturing Explore Map with West Champaran filter...")
    driver.get(f'{BASE_URL}/explore')
    time.sleep(2.5)
    driver.execute_script("""
        const sel = document.getElementById('map-district-filter');
        if (sel) {
            sel.value = 'West Champaran';
            sel.dispatchEvent(new Event('change'));
        }
    """)
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch7_explore_west_champaran_filter.png'))
    print("  -> Saved batch7_explore_west_champaran_filter.png")

    # 2. Batch 7 Detail Page Desktop (Bhitiharwa Gandhi Ashram)
    print("2. Capturing Bhitiharwa Gandhi Ashram detail page desktop...")
    driver.get(f'{BASE_URL}/place/bhitiharwa-gandhi-ashram-west-champaran')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch7_bhitiharwa_detail_desktop.png'))
    print("  -> Saved batch7_bhitiharwa_detail_desktop.png")

    # 3. Affected District Page (Siwan or West Champaran)
    print("3. Capturing District Page: West Champaran...")
    driver.get(f'{BASE_URL}/state/bihar/west-champaran')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch7_district_west_champaran_desktop.png'))
    print("  -> Saved batch7_district_west_champaran_desktop.png")

finally:
    driver.quit()

# ── MOBILE OPTIONS ──
options_mobile = Options()
options_mobile.add_argument('--headless=new')
options_mobile.add_argument('--disable-gpu')
options_mobile.add_argument('--no-sandbox')
options_mobile.add_argument('--window-size=375,812')

mobile_driver = webdriver.Chrome(options=options_mobile)

try:
    # 4. Batch 7 Mobile Detail Page (Baba Mahendra Nath Temple, Mehdar)
    print("4. Capturing Baba Mahendra Nath Temple mobile detail page...")
    mobile_driver.get(f'{BASE_URL}/place/baba-mahendra-nath-temple-mehdar-siwan')
    time.sleep(1.5)
    mobile_driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch7_mobile_mahendra_nath.png'))
    print("  -> Saved batch7_mobile_mahendra_nath.png")

    # 5. Mobile Detail Page (Ramrekha Ghat)
    print("5. Capturing Ramrekha Ghat mobile detail page...")
    mobile_driver.get(f'{BASE_URL}/place/ramrekha-ghat-buxar')
    time.sleep(1.5)
    mobile_driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch7_mobile_ramrekha_ghat.png'))
    print("  -> Saved batch7_mobile_ramrekha_ghat.png")

finally:
    mobile_driver.quit()

print("All Batch 7 screenshots captured successfully.")
