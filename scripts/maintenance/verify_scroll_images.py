"""
Scroll down and verify all lazy-loaded cards on /state/bihar/jamui.
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,3000')

driver = webdriver.Chrome(options=options)
try:
    driver.get('https://hiddenyatra.onrender.com/state/bihar/jamui')
    time.sleep(3)
    # Scroll down to bottom to trigger all lazy images
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    cards = driver.execute_script("""
        const res = [];
        document.querySelectorAll('.place-directory-item').forEach(c => {
            const name = c.querySelector('h3')?.innerText?.trim() || '';
            const img = c.querySelector('img.place-card-img');
            res.push({
                name: name,
                src: img ? img.src : '',
                naturalWidth: img ? img.naturalWidth : 0,
                naturalHeight: img ? img.naturalHeight : 0,
                complete: img ? img.complete : false
            });
        });
        return res;
    """)

    print(f"Total cards evaluated: {len(cards)}")
    custom_loaded = 0
    for c in cards:
        is_custom = '/static/uploads/places/' in c['src'] and c['naturalWidth'] > 0
        if is_custom:
            custom_loaded += 1
        print(f"  - [{c['naturalWidth']}x{c['naturalHeight']}] {c['name']:32s} -> {c['src']}")

    print(f"\nFinal count of custom loaded images: {custom_loaded} of 11 local Jamui places!")
    driver.save_screenshot('scratch/jamui_all_cards_scrolled.png')

finally:
    driver.quit()
