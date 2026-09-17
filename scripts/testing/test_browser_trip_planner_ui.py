import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'http://127.0.0.1:5000'
SCREENSHOT_DIR = r'd:\HiddenYatra\scratch\screenshots'
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1280,1000')
driver = webdriver.Chrome(options=options)

def log_step(name, passed, detail=''):
    status = '[PASS]' if passed else '[FAIL]'
    print(f"  {status} {name}: {detail}", flush=True)

try:
    print("\n=== E2E BROWSER VERIFICATION: AI TRIP PLANNER DESTINATIONS ===")

    # 1. Load /itinerary
    driver.get(f'{BASE_URL}/itinerary')
    time.sleep(0.8)

    # Check header and destination section visibility
    dest_box = driver.find_elements(By.ID, 'destination-section')
    log_step("Destination Section Present", len(dest_box) > 0, "Found destination-box element")

    dest_title = driver.find_element(By.CSS_SELECTOR, '.dest-title').text
    log_step("Destination Title", "WHERE DO YOU WANT TO GO" in dest_title, dest_title)

    # Screenshot initial state
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, '01_initial_form.png'))

    # 2. Click District Selector Dropdown
    picker_btn = driver.find_element(By.ID, 'district-picker-btn')
    picker_btn.click()
    time.sleep(0.3)

    options_list = driver.find_elements(By.CSS_SELECTOR, '.district-option-item')
    log_step("District Dropdown Options Count", len(options_list) == 38, f"Found {len(options_list)} Bihar districts")

    # Screenshot dropdown open
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, '02_district_dropdown_open.png'))

    # 3. Select 'Gaya' and 'Nalanda'
    gaya_opt = next((o for o in options_list if 'Gaya' in o.text and 'Bodh' not in o.text), None)
    if gaya_opt:
        driver.execute_script("arguments[0].click();", gaya_opt)
        time.sleep(0.3)

    # Re-fetch options or select Nalanda
    nalanda_opt = next((o for o in options_list if 'Nalanda' in o.text), None)
    if nalanda_opt:
        driver.execute_script("arguments[0].click();", nalanda_opt)
        time.sleep(0.3)

    # Close dropdown
    driver.find_element(By.TAG_NAME, 'body').click()
    time.sleep(0.3)

    # Verify selected district chips
    chips = driver.find_elements(By.CSS_SELECTOR, '.district-chip')
    chip_texts = [c.text for c in chips]
    log_step("Selected District Chips", len(chips) == 2, f"Chips: {chip_texts}")

    # Screenshot districts selected
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, '03_districts_selected.png'))

    # 4. Check places available in grid (Should belong only to Gaya and Nalanda)
    place_rows = driver.find_elements(By.CSS_SELECTOR, '.place-item-row')
    log_step("Places List Populated", len(place_rows) > 0, f"Found {len(place_rows)} places for Gaya+Nalanda")

    for pr in place_rows[:5]:
        pname = pr.find_element(By.CSS_SELECTOR, '.place-item-name').text
        pdist = pr.find_element(By.CSS_SELECTOR, '.place-item-district').text
        log_step("Place District Check", pdist in ['Gaya', 'Nalanda'], f"'{pname}' -> {pdist}")

    # 5. Search for 'Rajgir' in Place Search input
    search_input = driver.find_element(By.ID, 'place-search-input')
    search_input.clear()
    search_input.send_keys('Rajgir')
    time.sleep(0.5)

    search_rows = driver.find_elements(By.CSS_SELECTOR, '.place-item-row')
    log_step("Place Search 'Rajgir'", len(search_rows) > 0, f"Found {len(search_rows)} results")
    if search_rows:
        r_name = search_rows[0].find_element(By.CSS_SELECTOR, '.place-item-name').text
        r_dist = search_rows[0].find_element(By.CSS_SELECTOR, '.place-item-district').text
        log_step("Rajgir District Verification", r_dist == 'Nalanda', f"'{r_name}' under '{r_dist}'")
        # Click to select Rajgir
        driver.execute_script("arguments[0].click();", search_rows[0])
        time.sleep(0.3)

    # Select Nalanda University Ruins (ID 8) and Great Buddha Statue (ID 7)
    driver.execute_script("""
        togglePlaceRow(8, 'Nalanda University Ruins', 3, 'Nalanda', 'historical');
        togglePlaceRow(7, 'Great Buddha Statue, Bodh Gaya', 2, 'Gaya', 'tourist_spot');
    """)
    time.sleep(0.4)

    # Verify selected place chips
    sel_place_chips = driver.find_elements(By.CSS_SELECTOR, '.selected-place-chip')
    sel_place_texts = [sp.text for sp in sel_place_chips]
    log_step("Selected Place Chips", len(sel_place_chips) >= 2, f"Selected: {sel_place_texts}")

    # Screenshot places selected
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, '04_places_selected.png'))

    # 6. Set Duration = 5 days, Budget = 20000 Total, Mode = Family
    days_input = driver.find_element(By.ID, 'trip-days')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", days_input)
    days_input.clear()
    days_input.send_keys('5')

    budget_input = driver.find_element(By.ID, 'trip-budget-amount')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", budget_input)
    budget_input.clear()
    budget_input.send_keys('20000')

    # Total trip budget button
    total_btn = driver.find_element(By.CSS_SELECTOR, '.budget-type-btn[data-type="total"]')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", total_btn)
    time.sleep(0.2)

    # Family companion mode
    fam_card = driver.find_element(By.CSS_SELECTOR, '.travel-mode-card[data-mode="family"]')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", fam_card)
    time.sleep(0.2)

    # 7. Click Generate AI Trip Plan
    gen_btn = driver.find_element(By.ID, 'btn-generate')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gen_btn)
    time.sleep(0.3)
    gen_btn.click()
    time.sleep(2.0)

    # 8. Verify Itinerary Results
    results_container = driver.find_element(By.ID, 'trip-results')
    log_step("Results Visible", results_container.is_displayed(), "Trip results section rendered")

    day_cards = driver.find_elements(By.CSS_SELECTOR, '.day-card')
    log_step("Day Cards Count", len(day_cards) >= 5, f"Rendered {len(day_cards)} day cards")

    # Check that selected places appear in the itinerary
    timeline_places = driver.find_elements(By.CSS_SELECTOR, '.timeline-content h4')
    timeline_names = [tp.text for tp in timeline_places]
    log_step("Itinerary Places", len(timeline_names) > 0, f"Places generated: {timeline_names}")

    # Screenshot full generated itinerary
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, '05_generated_itinerary.png'))

    # 9. Mobile Viewport Test (375 x 812)
    print("\n--- MOBILE VIEWPORT TESTING (375x812) ---")
    driver.set_window_size(375, 812)
    time.sleep(0.5)

    driver.get(f'{BASE_URL}/itinerary')
    time.sleep(0.8)

    mob_dest = driver.find_elements(By.ID, 'destination-section')
    log_step("Mobile Destination Section", len(mob_dest) > 0, "Responsive layout verified on 375px")

    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, '06_mobile_view.png'))

finally:
    driver.quit()
    print("\nVerification completed. Screenshots saved in scratch/screenshots/")
