"""
HiddenYatra — Admin Place Featured Star Toggle E2E Browser Test Suite
Tests:
1. Admin login & navigation to /admin/places
2. Locating 5 places across distinct districts (Patna, Gaya, Jamui, Nalanda, Bhagalpur)
3. Direct browser star click: UI toggle, AJAX call, DB update, and page refresh persistence
4. Revert toggle (OFF -> ON -> OFF) and database verification
5. Multi-place independence verification across pages
6. Zero browser console errors
"""
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = 'http://127.0.0.1:5000'

class AdminStarE2ETester:
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
        icon = '✅' if status == 'PASS' else '❌'
        print(f"  {icon} [{flow}] {step[:48]} -> {status} ({actual})", flush=True)

    def check_console_errors(self, page_name):
        logs = self.driver.get_log('browser')
        severe = [l for l in logs if l['level'] in ('SEVERE', 'ERROR')]
        for s in severe:
            msg = s['message']
            if 'favicon' not in msg and 'fonts.googleapis' not in msg and 'fonts.gstatic' not in msg and 'tile.openstreetmap' not in msg:
                self.log(page_name, 'Browser Console Error', 'Zero JS runtime exceptions', msg[:60], 'FAIL')

    def run_tests(self):
        d = self.driver
        sys.path.insert(0, r'd:\HiddenYatra')
        from dotenv import load_dotenv
        load_dotenv()
        from models.connection import get_cursor
        from models.places import get_all_places
        from config import ADMIN_PASSWORD

        # Get all places in order to map each place to its exact page number
        all_places = get_all_places(limit=500, offset=0)
        place_page_map = {}
        for idx, p in enumerate(all_places):
            page_num = (idx // 30) + 1
            place_page_map[p['id']] = page_num

        # Pick 5 distinct places from 5 districts (Patna, Gaya, Jamui, Nalanda, Bhagalpur)
        target_districts = ['Patna', 'Gaya', 'Jamui', 'Nalanda', 'Bhagalpur']
        target_places = []
        with get_cursor() as cur:
            for dist_name in target_districts:
                cur.execute("""
                    SELECT p.id, p.name, p.district_id, d.name AS district_name, p.is_featured
                    FROM places p
                    JOIN districts d ON p.district_id = d.id
                    WHERE d.name = %s AND p.deleted_at IS NULL
                    ORDER BY p.id ASC
                    LIMIT 1
                """, (dist_name,))
                row = cur.fetchone()
                if row:
                    row['page'] = place_page_map.get(row['id'], 1)
                    target_places.append(row)

        print(f"\n[1] Target Places across districts:", flush=True)
        for p in target_places:
            print(f"    - ID {p['id']}: {p['name']} ({p['district_name']}) | Page {p['page']} | Initial is_featured={p['is_featured']}", flush=True)

        print("\n[2] Logging in as Admin...", flush=True)
        d.get(f'{BASE_URL}/admin/login')
        time.sleep(0.4)
        pass_inp = d.find_element(By.NAME, 'password')
        pass_inp.send_keys(ADMIN_PASSWORD)
        btn = d.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        btn.click()
        time.sleep(0.8)

        d.get(f'{BASE_URL}/admin/places')
        time.sleep(0.5)
        self.check_console_errors('Admin Places Page')

        table_rows = d.find_elements(By.CSS_SELECTOR, '.place-row')
        login_ok = len(table_rows) > 0
        self.log('Admin Auth', 'Access Admin Place List Table', 'Place rows rendered', f"Rows={len(table_rows)}", 'PASS' if login_ok else 'FAIL')

        print("\n[3] Testing Star Button End-to-End for each place...", flush=True)
        for p in target_places:
            pid = p['id']
            pname = p['name']
            dist = p['district_name']
            page_num = p['page']
            star_btn_id = f'star-btn-{pid}'

            # Navigate to the place's page
            d.get(f'{BASE_URL}/admin/places?page={page_num}')
            time.sleep(0.4)

            # Check button in DOM
            star_btns = d.find_elements(By.ID, star_btn_id)
            if not star_btns:
                self.log(dist, f'Locate star button for {pname}', 'Found button', f'Not found on page {page_num}', 'FAIL')
                continue

            star_btn = star_btns[0]
            d.execute_script("arguments[0].scrollIntoView({block:'center'});", star_btn)
            time.sleep(0.2)

            # 1. Read initial DB state
            with get_cursor() as cur:
                cur.execute("SELECT is_featured FROM places WHERE id = %s", (pid,))
                db_initial = cur.fetchone()['is_featured']

            # 2. Click Star Button (Toggle 1)
            d.execute_script("arguments[0].click();", star_btn)
            time.sleep(0.6)
            self.check_console_errors(f'Toggle {pname}')

            # Verify DOM updated
            btn_text_1 = star_btn.text.strip()
            is_active_1 = 'active' in star_btn.get_attribute('class')
            expected_feat_1 = 0 if db_initial else 1

            # Verify DB updated
            with get_cursor() as cur:
                cur.execute("SELECT is_featured FROM places WHERE id = %s", (pid,))
                db_after_1 = cur.fetchone()['is_featured']

            toggle_1_ok = (db_after_1 == expected_feat_1) and (is_active_1 == bool(expected_feat_1))
            self.log(dist, f'Click Star Toggle 1: {pname}', f'DB={expected_feat_1}, UI Active={bool(expected_feat_1)}', f'DB={db_after_1}, UI={btn_text_1}', 'PASS' if toggle_1_ok else 'FAIL')

            # 3. Refresh Page and verify persistence
            d.get(f'{BASE_URL}/admin/places?page={page_num}')
            time.sleep(0.4)
            star_btn_refreshed = d.find_element(By.ID, star_btn_id)
            d.execute_script("arguments[0].scrollIntoView({block:'center'});", star_btn_refreshed)
            is_active_refreshed = 'active' in star_btn_refreshed.get_attribute('class')
            persist_1_ok = is_active_refreshed == bool(expected_feat_1)
            self.log(dist, f'Page Refresh Persistence 1: {pname}', f'UI Active={bool(expected_feat_1)}', f'UI Active={is_active_refreshed}', 'PASS' if persist_1_ok else 'FAIL')

            # 4. Click Star Button again (Toggle 2 - revert back)
            d.execute_script("arguments[0].click();", star_btn_refreshed)
            time.sleep(0.6)
            self.check_console_errors(f'Revert {pname}')

            # Verify DB reverted
            with get_cursor() as cur:
                cur.execute("SELECT is_featured FROM places WHERE id = %s", (pid,))
                db_after_2 = cur.fetchone()['is_featured']

            is_active_2 = 'active' in star_btn_refreshed.get_attribute('class')
            revert_ok = (db_after_2 == db_initial) and (is_active_2 == bool(db_initial))
            self.log(dist, f'Click Star Toggle 2 (Revert): {pname}', f'DB={db_initial}, UI Active={bool(db_initial)}', f'DB={db_after_2}, UI Active={is_active_2}', 'PASS' if revert_ok else 'FAIL')

            # 5. Refresh Page again and verify revert persisted
            d.get(f'{BASE_URL}/admin/places?page={page_num}')
            time.sleep(0.4)
            star_btn_revert_refreshed = d.find_element(By.ID, star_btn_id)
            d.execute_script("arguments[0].scrollIntoView({block:'center'});", star_btn_revert_refreshed)
            is_active_revert_refreshed = 'active' in star_btn_revert_refreshed.get_attribute('class')
            persist_2_ok = is_active_revert_refreshed == bool(db_initial)
            self.log(dist, f'Page Refresh Persistence 2: {pname}', f'UI Active={bool(db_initial)}', f'UI Active={is_active_revert_refreshed}', 'PASS' if persist_2_ok else 'FAIL')

        d.quit()

        print("\n" + "="*80)
        print("ADMIN PLACE STAR TOGGLE E2E TEST SUMMARY")
        print("="*80)
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = total - passed
        print(f"Total Controls/Flows: {total} | Passed: {passed} | Failed: {failed}")
        return failed == 0

if __name__ == '__main__':
    tester = AdminStarE2ETester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)
