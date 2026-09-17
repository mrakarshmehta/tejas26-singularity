import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'http://127.0.0.1:5000'

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1280,900')
driver = webdriver.Chrome(options=options)

try:
    print("\n[1] Logging in as Admin...")
    driver.get(f'{BASE_URL}/admin/login')
    time.sleep(0.3)
    pass_input = driver.find_element(By.NAME, 'password')
    pass_input.send_keys('admin@hidden123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(0.5)
    print(f"    Current URL: {driver.current_url}")

    print("\n[2] Checking Admin Dashboard / Places list...")
    driver.get(f'{BASE_URL}/admin/places')
    time.sleep(0.5)

    # Override window.confirm so it doesn't block headless Chrome
    driver.execute_script("window.confirm = function() { return true; };")

    del_buttons = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/delete/"] button[type="submit"]')
    print(f"    Found {len(del_buttons)} delete buttons in places table.")

    if del_buttons:
        # Get place name from first row
        first_row = driver.find_element(By.CSS_SELECTOR, '.place-row')
        place_name = first_row.find_element(By.CSS_SELECTOR, '.place-name-cell a').text.strip()
        print(f"    First place to test: '{place_name}'")

        # Click the delete button
        del_btn = del_buttons[0]
        print(f"    Clicking delete button for '{place_name}'...")
        del_btn.click()
        time.sleep(0.8)

        print(f"    Post-click URL: {driver.current_url}")
        
        # Check flash messages
        flashes = driver.find_elements(By.CSS_SELECTOR, '.flash-message, .alert')
        for f in flashes:
            print(f"    Flash: {f.text.strip()}")

        # Check Recycle Bin
        print("\n[3] Checking Recycle Bin...")
        driver.get(f'{BASE_URL}/admin/recycle-bin')
        time.sleep(0.5)

        deleted_items = driver.find_elements(By.CSS_SELECTOR, '.deleted-item')
        print(f"    Recycle Bin contains {len(deleted_items)} deleted items.")
        found_in_bin = False
        for item in deleted_items:
            name = item.find_element(By.CSS_SELECTOR, '.deleted-item-name').text.strip()
            print(f"      - {name}")
            if place_name in name:
                found_in_bin = True

        print(f"    Place '{place_name}' found in Recycle Bin: {found_in_bin}")

        # Now test Restore
        if found_in_bin:
            print(f"\n[4] Testing Restore for '{place_name}'...")
            restore_form = driver.find_element(By.CSS_SELECTOR, f'form[action*="/admin/restore/"]')
            restore_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(0.8)
            print(f"    Restored! Current URL: {driver.current_url}")

finally:
    driver.quit()
