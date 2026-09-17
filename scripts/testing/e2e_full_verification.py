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
    print("\n[1] Testing /stays Discovery Page...")
    driver.get(f'{BASE_URL}/stays')
    time.sleep(0.5)

    cards = driver.find_elements(By.CSS_SELECTOR, '.stay-card')
    print(f"    Total stay cards displayed: {len(cards)}")
    for idx, c in enumerate(cards):
        title = c.find_element(By.CSS_SELECTOR, '.stay-card-title').text.strip()
        img = c.find_element(By.CSS_SELECTOR, '.stay-card-img')
        src = img.get_attribute('src') or ''
        loaded = driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0;", img)
        print(f"    Card {idx+1}: '{title}' -> src={src.split('/')[-1]}, loaded={loaded}")

    print("\n[2] Testing Stay Detail Pages...")
    for slug in ['bodh-gaya-heritage-homestay', 'simultala-eco-village-stay']:
        driver.get(f'{BASE_URL}/stay/{slug}')
        time.sleep(0.4)
        main_img = driver.find_element(By.CSS_SELECTOR, '.sd-gallery-main')
        src = main_img.get_attribute('src') or ''
        loaded = driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0;", main_img)
        print(f"    Detail '{slug}': src={src.split('/')[-1]}, loaded={loaded}")

    print("\n[3] Testing Admin Recycle Bin...")
    driver.get(f'{BASE_URL}/admin/login')
    time.sleep(0.3)
    pass_input = driver.find_element(By.NAME, 'password')
    pass_input.send_keys('admin@hidden123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(0.5)

    driver.get(f'{BASE_URL}/admin/recycle-bin')
    time.sleep(0.5)

    deleted_items = driver.find_elements(By.CSS_SELECTOR, '.deleted-item')
    print(f"    Recycle Bin contains {len(deleted_items)} deleted places:")
    for item in deleted_items:
        name = item.find_element(By.CSS_SELECTOR, '.deleted-item-name').text.strip()
        print(f"      - {name}")

finally:
    driver.quit()
