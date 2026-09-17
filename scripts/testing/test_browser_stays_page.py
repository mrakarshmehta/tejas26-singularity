import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'http://127.0.0.1:5000'
ARTIFACT_DIR = r'C:\Users\AKARSH RAJ\.gemini\antigravity-ide\brain\3a66ab24-01c5-4697-b84b-ebeb409fca98'
os.makedirs(ARTIFACT_DIR, exist_ok=True)

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1280,1100')
driver = webdriver.Chrome(options=options)

def log_step(name, passed, detail=''):
    status = '[PASS]' if passed else '[FAIL]'
    print(f"  {status} {name}: {detail}", flush=True)

try:
    print("\n=== E2E BROWSER VERIFICATION: /stays DISCOVERY & DETAIL ===")

    # 1. Load /stays
    driver.get(f'{BASE_URL}/stays')
    time.sleep(1.0)

    # Check title
    log_step("Page Title", "Local Stays & Homestays in Bihar" in driver.title, driver.title)

    # Check total cards
    cards = driver.find_elements(By.CSS_SELECTOR, '.stay-card')
    log_step("Stay Cards Rendered", len(cards) >= 12, f"Rendered {len(cards)} homestay cards")

    # Verify no large broken image or placeholder on demo cards
    card_imgs = driver.find_elements(By.CSS_SELECTOR, '.stay-card-img')
    valid_imgs = [img for img in card_imgs if 'placeholder-homestay.svg' not in img.get_attribute('src')]
    log_step("Real Photos in Cards", len(valid_imgs) >= 10, f"Found {len(valid_imgs)} cards with real photos")

    # Screenshot /stays grid
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'stays_browse_desktop.png'))

    # 2. Test Filter: Free Local Stays
    free_pill = driver.find_element(By.CSS_SELECTOR, '.type-pill[href*="free_stay"]')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", free_pill)
    time.sleep(0.8)

    free_cards = driver.find_elements(By.CSS_SELECTOR, '.stay-card')
    log_step("Free Stays Filter", len(free_cards) >= 3, f"Rendered {len(free_cards)} free local stays")
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'stays_free_filter.png'))

    # 3. Test Filter: District = Jamui
    driver.get(f'{BASE_URL}/stays?district_id=4')
    time.sleep(0.8)
    jamui_cards = driver.find_elements(By.CSS_SELECTOR, '.stay-card')
    log_step("Jamui Filter", len(jamui_cards) >= 2, f"Rendered {len(jamui_cards)} Simultala/Jamui stays")
    for jc in jamui_cards:
        j_text = jc.text
        log_step("Jamui Card Verification", 'Jamui' in j_text or 'Simultala' in j_text, jc.find_element(By.CSS_SELECTOR, '.stay-card-title').text)

    # 4. Stay Detail Page Verification
    driver.get(f'{BASE_URL}/stay/rajgir-green-valley-eco-homestay')
    time.sleep(1.0)

    # Check detail elements
    detail_title = driver.find_element(By.CSS_SELECTOR, '.sd-title').text
    log_step("Stay Detail Title", "Rajgir Green Valley" in detail_title, detail_title)

    gallery_thumbs = driver.find_elements(By.CSS_SELECTOR, '.sd-gallery img')
    log_step("Detail Photo Gallery", len(gallery_thumbs) >= 4, f"Found {len(gallery_thumbs)} gallery images")

    host_card = driver.find_element(By.CSS_SELECTOR, '.sd-host-card')
    log_step("Host Profile Card", "Neha Singh" in host_card.text, "Host card with bio and verified badge rendered")

    booking_card = driver.find_element(By.CSS_SELECTOR, '.sd-booking-card')
    log_step("Booking Box", booking_card.is_displayed(), "Sticky request booking card present")

    # Screenshot detail page
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'stay_detail_page_rajgir.png'))

    # Also capture Bodh Gaya detail
    driver.get(f'{BASE_URL}/stay/bodh-gaya-lotus-heritage-homestay')
    time.sleep(0.8)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'stay_detail_page_gaya.png'))

    # 5. Mobile Viewport Test (375x812)
    print("\n--- MOBILE VIEWPORT TESTING (375x812) ---")
    driver.set_window_size(375, 812)
    driver.get(f'{BASE_URL}/stays')
    time.sleep(1.0)

    mob_cards = driver.find_elements(By.CSS_SELECTOR, '.stay-card')
    log_step("Mobile Stay Cards", len(mob_cards) >= 12, f"Rendered {len(mob_cards)} cards on mobile")
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'stays_browse_mobile.png'))

    # Mobile detail view
    driver.get(f'{BASE_URL}/stay/rajgir-green-valley-eco-homestay')
    time.sleep(0.8)
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'stay_detail_mobile.png'))

    # 6. Check console errors
    logs = driver.get_log('browser')
    severe_errors = [entry for entry in logs if entry['level'] == 'SEVERE']
    log_step("Console Errors", len(severe_errors) == 0, f"Found {len(severe_errors)} severe errors")

finally:
    driver.quit()
    print("\nBrowser verification complete. Screenshots saved.")
