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
    print("1. Capturing Explore Map (Bhagalpur Filter)...")
    driver.get(f'{BASE_URL}/explore')
    time.sleep(2.5)
    driver.execute_script("""
        const sel = document.getElementById('map-district-filter');
        if (sel) {
            sel.value = 'Bhagalpur';
            sel.dispatchEvent(new Event('change'));
        }
    """)
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_explore_bhagalpur_filter.png'))
    print("  -> Saved batch6_explore_bhagalpur_filter.png")

    # 2. Capturing Place Detail: Kahalgaon Rock-Cut Temples (Bhagalpur)
    print("2. Capturing Kahalgaon Rock-Cut Temples detail page...")
    driver.get(f'{BASE_URL}/place/kahalgaon-rock-cut-temples-bhagalpur')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_kahalgaon_detail_desktop.png'))
    print("  -> Saved batch6_kahalgaon_detail_desktop.png")

    # 3. Capturing Place Detail: Vishwa Shanti Stupa & Ratnagiri Ropeway (Nalanda)
    print("3. Capturing Vishwa Shanti Stupa & Ratnagiri Ropeway detail page...")
    driver.get(f'{BASE_URL}/place/vishwa-shanti-stupa-and-ratnagiri-ropeway-nalanda')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_vishwa_shanti_detail_desktop.png'))
    print("  -> Saved batch6_vishwa_shanti_detail_desktop.png")

    # 4. Capturing Place Detail: Shringirishi Dham (Lakhisarai)
    print("4. Capturing Shringirishi Dham detail page...")
    driver.get(f'{BASE_URL}/place/shringirishi-dham-lakhisarai')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_shringirishi_detail_desktop.png'))
    print("  -> Saved batch6_shringirishi_detail_desktop.png")

    # 5. Capturing Place Detail: Girihinda Pahar & Shiv Temple (Sheikhpura)
    print("5. Capturing Girihinda Pahar & Shiv Temple detail page...")
    driver.get(f'{BASE_URL}/place/girihinda-pahar-and-shiv-temple-sheikhpura')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_girihinda_detail_desktop.png'))
    print("  -> Saved batch6_girihinda_detail_desktop.png")

    # 6. Capturing District Page: Sheikhpura
    print("6. Capturing Sheikhpura District page...")
    driver.get(f'{BASE_URL}/state/bihar/sheikhpura')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_district_sheikhpura_desktop.png'))
    print("  -> Saved batch6_district_sheikhpura_desktop.png")

    # 7. Capturing District Page: Lakhisarai
    print("7. Capturing Lakhisarai District page...")
    driver.get(f'{BASE_URL}/state/bihar/lakhisarai')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_district_lakhisarai_desktop.png'))
    print("  -> Saved batch6_district_lakhisarai_desktop.png")

    # 8. Capturing Mobile Viewport: Matsyagandha Lake & Raktakali Temple
    print("8. Capturing Mobile Viewport (390x844) for Matsyagandha Lake...")
    driver.set_window_size(390, 844)
    driver.get(f'{BASE_URL}/place/matsyagandha-lake-and-raktakali-temple-saharsa')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_mobile_matsyagandha.png'))
    print("  -> Saved batch6_mobile_matsyagandha.png")

    # 9. Capturing Mobile Viewport: Kajha Kothi Eco Park
    print("9. Capturing Mobile Viewport (390x844) for Kajha Kothi Eco Park...")
    driver.get(f'{BASE_URL}/place/kajha-kothi-eco-park-purnia')
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'batch6_mobile_kajha_kothi.png'))
    print("  -> Saved batch6_mobile_kajha_kothi.png")

    print("\nAll Batch 6 screenshots captured successfully!")

finally:
    driver.quit()
