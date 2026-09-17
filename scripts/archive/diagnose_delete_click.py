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
    driver.get(f'{BASE_URL}/admin/login')
    time.sleep(0.3)
    pass_input = driver.find_element(By.NAME, 'password')
    pass_input.send_keys('admin@hidden123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(0.5)

    driver.get(f'{BASE_URL}/admin/places')
    time.sleep(0.5)

    del_buttons = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/delete/"] button[type="submit"]')
    print(f"Found {len(del_buttons)} delete buttons.")

    if del_buttons:
        btn = del_buttons[0]
        # Check if button is in viewport
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.3)
        
        # Check element from point
        loc = btn.location
        size = btn.size
        cx = loc['x'] + size['width'] / 2
        cy = loc['y'] + size['height'] / 2
        
        covering = driver.execute_script("""
            var el = arguments[0];
            var rect = el.getBoundingClientRect();
            var cx = rect.left + rect.width / 2;
            var cy = rect.top + rect.height / 2;
            var topEl = document.elementFromPoint(cx, cy);
            return {
                topTag: topEl ? topEl.tagName : 'none',
                topClass: topEl ? topEl.className : '',
                topId: topEl ? topEl.id : '',
                isSame: topEl === el || el.contains(topEl)
            };
        """, btn)
        print(f"Element from point check: {covering}")

        # Try clicking after scroll
        driver.execute_script("window.confirm = function() { return true; };")
        btn.click()
        time.sleep(0.8)
        print(f"Post-click URL: {driver.current_url}")

        # Check flash messages
        flashes = driver.find_elements(By.CSS_SELECTOR, '.flash-message, .alert')
        for f in flashes:
            print(f"Flash: {f.text.strip()}")

finally:
    driver.quit()
