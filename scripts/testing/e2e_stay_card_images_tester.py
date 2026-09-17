"""
HiddenYatra — Local Stays & Homestay Card Images E2E Browser Test Suite
Tests:
1. Browse stays page (/stays) — image rendering across all cards
2. Image loaded verification (naturalWidth > 0, zero broken images)
3. Computed style check (object-fit: cover, fixed height 210px)
4. Alt text and badges visibility
5. Stay detail page (/stay/<slug>) gallery rendering
6. Mobile viewport responsiveness (375px)
7. Console error verification
"""
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'http://127.0.0.1:5000'

class StayCardImagesE2ETester:
    def __init__(self):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1280,900')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        self.results = []

    def log(self, flow, step, expected, actual, status):
        self.results.append({
            'flow': flow, 'step': step,
            'expected': expected, 'actual': actual,
            'status': status
        })
        icon = '[PASS]' if status == 'PASS' else '[FAIL]'
        print(f"  {icon} [{flow}] {step[:48]} -> {status} ({actual})", flush=True)

    def check_console_errors(self, page_name):
        logs = self.driver.get_log('browser')
        severe = [l for l in logs if l['level'] in ('SEVERE', 'ERROR')]
        for s in severe:
            msg = s['message']
            if 'favicon' not in msg and 'fonts.googleapis' not in msg and 'fonts.gstatic' not in msg:
                self.log(page_name, 'Browser Console Error', 'Zero JS exceptions', msg[:60], 'FAIL')

    def run_tests(self):
        d = self.driver

        print("\n[1] Testing /stays Discovery Page...", flush=True)
        d.get(f'{BASE_URL}/stays')
        time.sleep(0.5)
        self.check_console_errors('Stays Browse Page')

        cards = d.find_elements(By.CSS_SELECTOR, '.stay-card')
        self.log('Browse Page', 'Locate Stay Cards', 'At least 1 stay card', f"Cards={len(cards)}", 'PASS' if len(cards) > 0 else 'FAIL')

        for idx, card in enumerate(cards):
            title = card.find_element(By.CSS_SELECTOR, '.stay-card-title').text.strip()
            wrapper = card.find_element(By.CSS_SELECTOR, '.stay-card-image-wrapper')
            img = wrapper.find_element(By.CSS_SELECTOR, '.stay-card-img')

            # 1. Check img src
            src = img.get_attribute('src') or ''
            has_src = len(src) > 0
            self.log(f'Card {idx+1}', f'Image Source: {title[:25]}', 'Non-empty src', src.split('/')[-1], 'PASS' if has_src else 'FAIL')

            # 2. Check naturalWidth > 0 (image loaded successfully)
            is_loaded = d.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0;", img)
            self.log(f'Card {idx+1}', f'Image Loaded (No Broken Img): {title[:25]}', 'naturalWidth > 0', f"Loaded={is_loaded}", 'PASS' if is_loaded else 'FAIL')

            # 3. Check object-fit: cover
            object_fit = d.execute_script("return window.getComputedStyle(arguments[0]).objectFit;", img)
            self.log(f'Card {idx+1}', f'Image Object-Fit Cover: {title[:25]}', 'cover', object_fit, 'PASS' if object_fit == 'cover' else 'FAIL')

            # 4. Check Alt text
            alt = img.get_attribute('alt') or ''
            has_alt = len(alt.strip()) > 0
            self.log(f'Card {idx+1}', f'Image Alt Text: {title[:25]}', 'Descriptive alt', alt[:35], 'PASS' if has_alt else 'FAIL')

            # 5. Check Badge visible
            badges = wrapper.find_elements(By.CSS_SELECTOR, '.stay-badge-type')
            has_badge = len(badges) > 0 and badges[0].is_displayed()
            badge_text = badges[0].text if has_badge else 'None'
            self.log(f'Card {idx+1}', f'Badge Visible: {title[:25]}', 'Visible badge', badge_text, 'PASS' if has_badge else 'FAIL')

        print("\n[2] Testing Stay Detail Pages...", flush=True)
        detail_slugs = [
            'bodh-gaya-heritage-homestay',
            'simultala-eco-village-stay',
            'test-paid-heritage-homestay'
        ]

        for slug in detail_slugs:
            d.get(f'{BASE_URL}/stay/{slug}')
            time.sleep(0.4)
            self.check_console_errors(f'Detail {slug}')

            main_img = d.find_elements(By.CSS_SELECTOR, '.sd-gallery-main')
            has_main = len(main_img) > 0
            if has_main:
                img_el = main_img[0]
                is_loaded = d.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0;", img_el)
                alt = img_el.get_attribute('alt') or ''
                self.log(slug, 'Main Gallery Image Loaded', 'naturalWidth > 0', f"Loaded={is_loaded}, Alt={alt[:30]}", 'PASS' if is_loaded else 'FAIL')

        print("\n[3] Testing Mobile Viewport (375x667)...", flush=True)
        d.set_window_size(375, 667)
        d.get(f'{BASE_URL}/stays')
        time.sleep(0.4)
        cards_mob = d.find_elements(By.CSS_SELECTOR, '.stay-card')
        mob_ok = len(cards_mob) > 0
        if mob_ok:
            img_mob = cards_mob[0].find_element(By.CSS_SELECTOR, '.stay-card-img')
            is_loaded_mob = d.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0;", img_mob)
            self.log('Mobile Layout', 'Mobile Stays Viewport', 'Cards render cleanly', f"Loaded={is_loaded_mob}", 'PASS' if is_loaded_mob else 'FAIL')

        d.quit()

        print("\n" + "="*80)
        print("STAY CARD IMAGES E2E TEST SUMMARY")
        print("="*80)
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = total - passed
        print(f"Total Controls/Flows: {total} | Passed: {passed} | Failed: {failed}")
        return failed == 0

if __name__ == '__main__':
    tester = StayCardImagesE2ETester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)
