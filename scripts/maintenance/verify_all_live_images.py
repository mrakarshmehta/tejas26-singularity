"""
Verify all Jamui place images on LIVE Render.
Checks HTTP 200 for all image assets, opens /state/bihar/jamui in Selenium,
verifies rendered card images, and captures screenshot.
"""
import os
import sys
import json
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verify():
    print("=" * 80)
    print("LIVE PRODUCTION JAMUI IMAGE VERIFICATION")
    print("=" * 80)

    jamui_images = [
        ("57_3edc98f203.png", "Giddheswar Temple"),
        ("58_f17d37897e.png", "Patneshwar Mandir"),
        ("59_e5277e5586.png", "Simultala Hill Station"),
        ("60_1bc07dc67a.png", "Kali Mandir, Malaypur"),
        ("61_bb548899fb.png", "Minto Tower, Gidhaur"),
        ("62_29ce760efe.png", "Maa Netula Temple"),
        ("63_ac8fa5aa1f.png", "Lachhuar Jain Temple"),
        ("66_79d4860cda.png", "Kshatriya Kund"),
        ("67_f23ef36559.png", "Nakti Dam Bird Sanctuary"),
        ("68_2ab6b2f782.png", "Gidhaur Raj Palace"),
        ("69_c29553d1cf.png", "Garhi Reservoir & Dam"),
    ]

    # 1. HTTP Status check for all 11 Jamui images
    print("\n[1/3] Testing HTTP status for all Jamui image URLs...")
    http_results = {}
    for filename, place_name in jamui_images:
        url = f"https://hiddenyatra.onrender.com/static/uploads/places/{filename}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                sz = len(resp.read())
                print(f"  [OK] {filename:20s} ({place_name:28s}) -> HTTP {status} ({round(sz/1024, 1)} KB)")
                http_results[filename] = {'status': status, 'size_kb': round(sz/1024, 1), 'url': url}
        except Exception as e:
            print(f"  [FAIL] {filename:20s} ({place_name:28s}) -> Error: {e}")
            http_results[filename] = {'status': str(e), 'url': url}

    # 2. Browser Verification of /state/bihar/jamui
    print("\n[2/3] Opening https://hiddenyatra.onrender.com/state/bihar/jamui in headless Chrome...")
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,1200')

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)

    try:
        driver.get('https://hiddenyatra.onrender.com/state/bihar/jamui')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.place-directory-item, .dist-places-grid')))
        time.sleep(3)

        # Evaluate cards and image elements
        card_results = driver.execute_script("""
            const results = [];
            document.querySelectorAll('.place-directory-item, .dist-places-grid > div').forEach(card => {
                const name = card.querySelector('h3, .card-title, h4')?.innerText?.trim() || '';
                const img = card.querySelector('img.place-card-img, .place-card-img-wrap img');
                if (img) {
                    results.push({
                        name: name,
                        src: img.getAttribute('src') || img.src,
                        currentSrc: img.currentSrc,
                        complete: img.complete,
                        naturalWidth: img.naturalWidth,
                        naturalHeight: img.naturalHeight,
                        is_placeholder: (img.src || '').includes('placeholder')
                    });
                }
            });
            return results;
        """)

        print(f"\nScanned {len(card_results)} place cards on live Jamui page:")
        custom_rendered_count = 0
        for cr in card_results:
            is_custom = not cr['is_placeholder'] and cr['naturalWidth'] > 0
            if is_custom:
                custom_rendered_count += 1
            status_tag = "CUSTOM IMAGE LOADED" if is_custom else "SVG PLACEHOLDER"
            print(f"  - [{status_tag}] {cr['name']:32s} -> {cr['src']} (dims: {cr['naturalWidth']}x{cr['naturalHeight']})")

        print(f"\nSummary: {custom_rendered_count} of {len(card_results)} cards have custom loaded images rendered!")

        # 3. Capture screenshot of Jamui District Page
        screenshot_path = 'scratch/jamui_live_verified.png'
        driver.save_screenshot(screenshot_path)
        print(f"\n[3/3] Screenshot saved to {screenshot_path}")

        report = {
            'http_results': http_results,
            'card_results': card_results,
            'custom_rendered_count': custom_rendered_count,
            'total_cards': len(card_results)
        }
        with open('scratch/live_images_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

    finally:
        driver.quit()

if __name__ == '__main__':
    verify()
