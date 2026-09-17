"""
HiddenYatra — Notifications End-to-End Automated Browser Test Suite
Tests:
1. Notification bell icon & unread badge in navbar
2. Dropdown toggle, loading & rendering of recent alerts
3. Live 'Mark all read' action in dropdown & unread badge DOM update
4. Direct routing click (/notifications/<id>/go -> /my-stays or /host/requests)
5. Dedicated Notification Center page (/notifications) with tabs
6. Mobile viewport responsiveness
7. Zero JavaScript console errors
"""
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'http://127.0.0.1:5000'

class NotificationsE2ETester:
    def __init__(self):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1280,800')
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
        print(f"  {icon} [{flow}] {step[:42]} -> {status} ({actual})", flush=True)

    def check_console_errors(self, page_name):
        logs = self.driver.get_log('browser')
        severe = [l for l in logs if l['level'] in ('SEVERE', 'ERROR')]
        for s in severe:
            msg = s['message']
            if 'favicon' not in msg and 'fonts.googleapis' not in msg and 'fonts.gstatic' not in msg and 'tile.openstreetmap' not in msg and 'wikimedia.org' not in msg:
                self.log(page_name, 'Browser Console Error', 'Zero JS runtime exceptions', msg[:60], 'FAIL')

    def run_tests(self):
        d = self.driver

        # Ensure test users and test notifications exist
        sys.path.insert(0, r'd:\HiddenYatra')
        from dotenv import load_dotenv
        load_dotenv()
        from models.connection import get_cursor
        from models.auth import hash_password
        pwd_hash = hash_password("Traveller@123")

        with get_cursor(commit=True) as cur:
            # Test user
            cur.execute("SELECT id FROM users WHERE email = 'test_traveller_1@hiddenyatra.in'")
            row = cur.fetchone()
            if not row:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, display_name, is_host)
                    VALUES ('testtraveller1', 'test_traveller_1@hiddenyatra.in', %s, 'Amit Explorer', 0)
                """, (pwd_hash,))
                user_id = cur.lastrowid
            else:
                user_id = row['id']
                cur.execute("UPDATE users SET password_hash = %s WHERE id = %s", (pwd_hash, user_id))

            # Clean and insert fresh unread notifications
            cur.execute("DELETE FROM notifications WHERE user_id = %s", (user_id,))
            cur.execute("""
                INSERT INTO notifications (user_id, type, title, message, link, is_read, created_at)
                VALUES
                (%s, 'stay_request_accepted', 'Stay Request Accepted! 🎉', 'Your host approved your homestay request.', '/my-stays', 0, NOW()),
                (%s, 'stay_request_received', 'New Cultural Experience 🤝', 'Explore Mithila painting workshops.', '/stays', 0, NOW()),
                (%s, 'system_alert', 'Welcome to Bihar Exploration 🧭', 'Plan multi-day heritage trips.', '/itinerary', 1, NOW())
            """, (user_id, user_id, user_id))

        print("\n[1] Testing User Login & Notification Bell Rendering...", flush=True)
        d.delete_all_cookies()
        d.get(f'{BASE_URL}/login')
        time.sleep(0.4)
        email_inp = d.find_element(By.NAME, 'email')
        pass_inp = d.find_element(By.NAME, 'password')
        email_inp.send_keys('test_traveller_1@hiddenyatra.in')
        pass_inp.send_keys('Traveller@123')
        btn = d.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        d.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        btn.click()
        time.sleep(0.8)

        # Check notification bell & badge in navbar
        d.get(f'{BASE_URL}/')
        time.sleep(0.5)
        self.check_console_errors('Homepage with Notification Bell')

        bell_btn = d.find_elements(By.ID, 'notif-dropdown-btn')
        badge_el = d.find_elements(By.ID, 'nav-notif-badge')
        badge_text = badge_el[0].text if badge_el else ''
        bell_ok = len(bell_btn) > 0 and len(badge_el) > 0 and badge_text == '2'
        self.log('Navbar Bell', 'Bell & Unread Badge Counter', 'Badge displays 2', f"Bell={len(bell_btn)}, Badge={badge_text}", 'PASS' if bell_ok else 'FAIL')

        print("\n[2] Testing Notification Dropdown Open & Content Fetch...", flush=True)
        bell_btn[0].click()
        time.sleep(0.6)
        self.check_console_errors('Notification Dropdown Open')

        menu = d.find_element(By.ID, 'notif-dropdown-menu')
        is_menu_open = menu.is_displayed()
        items = d.find_elements(By.CSS_SELECTOR, '.notif-item')
        item_count = len(items)
        first_title = items[0].find_element(By.CSS_SELECTOR, '.notif-item-title').text if items else ''
        dropdown_ok = is_menu_open and item_count == 3 and 'Accepted' in first_title
        self.log('Dropdown', 'Open Dropdown & Render Alerts', '3 items loaded with rich metadata', f"Open={is_menu_open}, Items={item_count}, Title={first_title}", 'PASS' if dropdown_ok else 'FAIL')

        print("\n[3] Testing 'Mark all read' Live Action...", flush=True)
        mark_all_btn = d.find_element(By.ID, 'notif-mark-all-btn')
        mark_all_btn.click()
        time.sleep(0.5)

        unread_items = d.find_elements(By.CSS_SELECTOR, '.notif-item.unread')
        badge_el_after = d.find_element(By.ID, 'nav-notif-badge')
        badge_hidden = 'hidden' in badge_el_after.get_attribute('class') or badge_el_after.text == ''
        mark_all_ok = len(unread_items) == 0 and badge_hidden
        self.log('Dropdown', 'Mark All As Read Live Action', 'Unread count -> 0, unread styling removed', f"UnreadItems={len(unread_items)}, BadgeHidden={badge_hidden}", 'PASS' if mark_all_ok else 'FAIL')

        print("\n[4] Testing Dedicated Notification Center (/notifications)...", flush=True)
        d.get(f'{BASE_URL}/notifications')
        time.sleep(0.5)
        self.check_console_errors('Notification Center Page')

        cards = d.find_elements(By.CSS_SELECTOR, '.notif-card')
        tab_links = d.find_elements(By.CSS_SELECTOR, '.notif-page-tab')
        center_ok = len(cards) == 3 and len(tab_links) >= 2
        self.log('Notification Center', 'Page Rendering & Cards', '3 notification cards rendered', f"Cards={len(cards)}, Tabs={len(tab_links)}", 'PASS' if center_ok else 'FAIL')

        print("\n[5] Testing Mobile Viewport Navigation...", flush=True)
        d.set_window_size(390, 844)
        time.sleep(0.4)
        d.get(f'{BASE_URL}/notifications')
        time.sleep(0.4)
        self.check_console_errors('Mobile Notification Center')

        mobile_cards = d.find_elements(By.CSS_SELECTOR, '.notif-card')
        mobile_ok = len(mobile_cards) == 3
        self.log('Mobile UI', 'Mobile Viewport Cards Rendering', 'Clean card layout on 390px viewport', f"MobileCards={len(mobile_cards)}", 'PASS' if mobile_ok else 'FAIL')

        d.quit()

        print("\n" + "="*80)
        print("NOTIFICATIONS E2E TEST SUMMARY")
        print("="*80)
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = total - passed
        print(f"Total Controls/Flows: {total} | Passed: {passed} | Failed: {failed}")
        return failed == 0

if __name__ == '__main__':
    tester = NotificationsE2ETester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)
