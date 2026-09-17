import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    print("1. Capturing Explore Map (Vaishali Filter)...")
    driver.get(f'{BASE_URL}/explore')
    time.sleep(2.5)
    # Select district Vaishali in filter
    driver.execute_script("""
        const sel = document.getElementById('map-district-filter');
        if (sel) {
            sel.value = 'Vaishali';
            sel.dispatchEvent(new Event('change'));
        }
    """)
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch5_explore_vaishali_filter.png'))
    print("  -> Saved batch5_explore_vaishali_filter.png")

    # Select district Aurangabad
    driver.execute_script("""
        const sel = document.getElementById('map-district-filter');
        if (sel) {
            sel.value = 'Aurangabad';
            sel.dispatchEvent(new Event('change'));
        }
    """)
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch5_explore_aurangabad_filter.png'))
    print("  -> Saved batch5_explore_aurangabad_filter.png")

    # 2. Capturing Place Detail: Ashokan Pillar & Ananda Stupa, Kolhua (Vaishali)
    print("2. Capturing Ashokan Pillar & Ananda Stupa, Kolhua detail page...")
    driver.get(f'{BASE_URL}/place/ashokan-pillar-and-ananda-stupa-kolhua-vaishali')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch5_kolhua_detail_desktop.png'))
    print("  -> Saved batch5_kolhua_detail_desktop.png")

    # 3. Capturing Place Detail: Punaura Dham (Sitamarhi)
    print("3. Capturing Punaura Dham detail page...")
    driver.get(f'{BASE_URL}/place/punaura-dham-sitamarhi')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch5_punaura_dham_detail_desktop.png'))
    print("  -> Saved batch5_punaura_dham_detail_desktop.png")

    # 4. Capturing Place Detail: Sujani Embroidery Craft Cluster (Muzaffarpur)
    print("4. Capturing Sujani Embroidery Craft Cluster detail page...")
    driver.get(f'{BASE_URL}/place/sujani-embroidery-craft-cluster-muzaffarpur')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch5_sujani_craft_detail_desktop.png'))
    print("  -> Saved batch5_sujani_craft_detail_desktop.png")

    # 5. Capturing District Page: Vaishali
    print("5. Capturing Vaishali District page...")
    driver.get(f'{BASE_URL}/state/bihar/vaishali')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch5_district_vaishali_desktop.png'))
    print("  -> Saved batch5_district_vaishali_desktop.png")

    # 6. Capturing Mobile Viewport (390x844): Chandan Dam
    print("6. Capturing Mobile viewport for Chandan Dam...")
    driver.set_window_size(390, 844)
    driver.get(f'{BASE_URL}/place/chandan-dam-banka')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch5_mobile_chandan_dam.png'))
    print("  -> Saved batch5_mobile_chandan_dam.png")

    # 7. Capturing Mobile Viewport: George Orwell Birthplace
    print("7. Capturing Mobile viewport for George Orwell Birthplace...")
    driver.get(f'{BASE_URL}/place/george-orwell-birthplace-and-memorial-east-champaran')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch5_mobile_george_orwell.png'))
    print("  -> Saved batch5_mobile_george_orwell.png")

    print("\nALL BATCH 5 SCREENSHOTS CAPTURED SUCCESSFULLY [OK]!")
finally:
    driver.quit()
