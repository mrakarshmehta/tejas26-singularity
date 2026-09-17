import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'http://127.0.0.1:5000'
ARTIFACT_DIR = r'C:\Users\AKARSH RAJ\.gemini\antigravity-ide\brain\3a66ab24-01c5-4697-b84b-ebeb409fca98'

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1280,1400')
driver = webdriver.Chrome(options=options)

try:
    # 1. Desktop: Select Gaya & Nalanda, search & pick places
    driver.get(f'{BASE_URL}/itinerary')
    time.sleep(0.6)

    # Select Gaya & Nalanda in JS directly for clean state
    driver.execute_script("""
        selectDistrict(2, 'Gaya');
        selectDistrict(3, 'Nalanda');
    """)
    time.sleep(0.5)

    # Select Rajgir, Nalanda University Ruins, and Great Buddha Statue
    driver.execute_script("""
        togglePlaceRow(9, 'Rajgir (Rajagriha)', 3, 'Nalanda', 'historical');
        togglePlaceRow(8, 'Nalanda University Ruins', 3, 'Nalanda', 'historical');
        togglePlaceRow(7, 'Great Buddha Statue, Bodh Gaya', 2, 'Gaya', 'tourist_spot');
    """)
    time.sleep(0.5)

    # Target screenshot of the Destination Section
    dest_el = driver.find_element(By.ID, 'destination-section')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dest_el)
    time.sleep(0.3)
    dest_el.screenshot(os.path.join(ARTIFACT_DIR, 'destination_section_detailed.png'))

    # Full form screenshot
    form_el = driver.find_element(By.ID, 'planner-form')
    form_el.screenshot(os.path.join(ARTIFACT_DIR, 'full_trip_planner_form.png'))

    # 2. Click Generate AI Trip Plan
    gen_btn = driver.find_element(By.ID, 'btn-generate')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", gen_btn)
    time.sleep(2.0)

    # Results screenshot
    results_el = driver.find_element(By.ID, 'trip-results')
    driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", results_el)
    time.sleep(0.5)
    results_el.screenshot(os.path.join(ARTIFACT_DIR, 'generated_itinerary_results.png'))

    # 3. Mobile Viewport (375x812)
    driver.set_window_size(375, 1000)
    driver.get(f'{BASE_URL}/itinerary')
    time.sleep(0.6)

    driver.execute_script("""
        selectDistrict(2, 'Gaya');
        selectDistrict(3, 'Nalanda');
        togglePlaceRow(9, 'Rajgir (Rajagriha)', 3, 'Nalanda', 'historical');
        togglePlaceRow(8, 'Nalanda University Ruins', 3, 'Nalanda', 'historical');
    """)
    time.sleep(0.5)

    mob_dest = driver.find_element(By.ID, 'destination-section')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mob_dest)
    time.sleep(0.3)
    mob_dest.screenshot(os.path.join(ARTIFACT_DIR, 'mobile_destination_view.png'))
    driver.save_screenshot(os.path.join(ARTIFACT_DIR, 'mobile_full_page.png'))

finally:
    driver.quit()
    print("All target screenshots saved successfully.")
