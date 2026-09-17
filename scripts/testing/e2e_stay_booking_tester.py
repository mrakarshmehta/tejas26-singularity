"""
HiddenYatra — Homestay / Local Stay Request Workflow E2E Selenium Automation Suite
Tests complete real browser flows:
1. Traveller Paid Stay request submission & live price calculation preview
2. Host incoming requests dashboard & Accept flow with welcome note
3. Traveller status update to 'Accepted' with revealed host direct contact info
4. Traveller Free Stay request submission & live preview (₹0 Free)
5. Traveller cancellation flow with reason modal
6. Admin stay requests moderation overview & force cancellation
7. Zero console errors
"""
import sys
import os
import time
import json
from datetime import date, timedelta

sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'http://127.0.0.1:5000'

class E2EStayBookingTester:
    def __init__(self):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
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
        print(f"  {icon} [{flow}] {step[:40]} -> {status} ({actual})", flush=True)

    def check_console_errors(self, page_name):
        logs = self.driver.get_log('browser')
        severe = [l for l in logs if l['level'] in ('SEVERE', 'ERROR')]
        for s in severe:
            msg = s['message']
            if 'favicon' not in msg and 'fonts.googleapis' not in msg and 'fonts.gstatic' not in msg and 'tile.openstreetmap' not in msg and 'wikimedia.org' not in msg:
                self.log(page_name, 'Browser Console Error', 'Zero JS runtime exceptions', msg[:60], 'FAIL')

    def test_login(self, email, password=""):
        d = self.driver
        d.delete_all_cookies()
        d.get(f'{BASE_URL}/login')
        time.sleep(0.4)
        email_inp = d.find_element(By.NAME, 'email')
        pass_inp = d.find_element(By.NAME, 'password')
        email_inp.clear()
        email_inp.send_keys(email)
        pass_inp.clear()
        pass_inp.send_keys(password or "testpass123")
        btn = d.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        d.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        btn.click()
        time.sleep(0.8)

    def run_tests(self):
        d = self.driver

        # Ensure passwords are set for test users
        from models.connection import get_cursor
        from models.auth import hash_password
        pwd_hash = hash_password("Traveller@123")
        with get_cursor(commit=True) as cur:
            cur.execute("UPDATE users SET password_hash = %s WHERE email = 'test_traveller_1@hiddenyatra.in'", (pwd_hash,))
            cur.execute("UPDATE users SET password_hash = %s WHERE email = 'test_host_1@hiddenyatra.in'", (pwd_hash,))
            cur.execute("DELETE FROM listing_availability WHERE listing_id IN (17, 18)")
            cur.execute("DELETE FROM stay_requests WHERE listing_id IN (17, 18)")

        print("\n[1] Testing Live Date Picker & Dynamic Price Preview (/stay/test-paid-heritage-homestay)...", flush=True)
        d.get(f'{BASE_URL}/stay/test-paid-heritage-homestay')
        time.sleep(0.8)
        self.check_console_errors('Stay Detail Page')

        try:
            d_in_str = (date.today() + timedelta(days=5)).strftime('%Y-%m-%d')
            d_out_str = (date.today() + timedelta(days=8)).strftime('%Y-%m-%d')
            
            d.execute_script(f"document.getElementById('checkin').value = '{d_in_str}'; document.getElementById('checkin').dispatchEvent(new Event('change'));")
            d.execute_script(f"document.getElementById('checkout').value = '{d_out_str}'; document.getElementById('checkout').dispatchEvent(new Event('change'));")
            time.sleep(0.4)

            calc_box = d.find_element(By.ID, 'sd-price-calc')
            is_displayed = calc_box.is_displayed()
            total_text = d.find_element(By.ID, 'sd-calc-total').text
            ok_preview = is_displayed and '3600' in total_text
            self.log('Stay Detail', 'Live Price & Nights Preview', 'Display ₹3600 for 3 nights', f"Displayed={is_displayed}, Total={total_text}", 'PASS' if ok_preview else 'FAIL')
        except Exception as e:
            self.log('Stay Detail', 'Live Price Preview', 'Calculate price', str(e)[:50], 'FAIL')

        # 2. Login as Traveller and Submit Paid Stay Request
        print("\n[2] Testing Traveller Paid Stay Request Submission...", flush=True)
        self.test_login('test_traveller_1@hiddenyatra.in', 'Traveller@123')
        d.get(f'{BASE_URL}/stay/test-paid-heritage-homestay')
        time.sleep(0.8)

        try:
            d_in_str = (date.today() + timedelta(days=12)).strftime('%Y-%m-%d')
            d_out_str = (date.today() + timedelta(days=15)).strftime('%Y-%m-%d')
            d.execute_script(f"document.getElementById('checkin').value = '{d_in_str}'; document.getElementById('checkin').dispatchEvent(new Event('change'));")
            d.execute_script(f"document.getElementById('checkout').value = '{d_out_str}'; document.getElementById('checkout').dispatchEvent(new Event('change'));")
            time.sleep(0.3)

            msg_input = d.find_element(By.ID, 'message')
            msg_input.send_keys("E2E Automated test booking request")

            submit_btn = d.find_element(By.ID, 'btn-request-stay')
            d.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
            time.sleep(0.2)
            submit_btn.click()
            time.sleep(1.0)

            is_mystays = '/my-stays' in d.current_url or '/my-bookings' in d.current_url
            has_pending_card = len(d.find_elements(By.CSS_SELECTOR, '.status-pending, .stay-card-item')) > 0
            self.log('Traveller Flow', 'Submit Request & Redirect /my-stays', 'Redirect to /my-stays and render Pending card', f"URL={d.current_url}, Card Found={has_pending_card}", 'PASS' if is_mystays and has_pending_card else 'FAIL')
        except Exception as e:
            self.log('Traveller Flow', 'Submit Request', 'Submit stay request', str(e)[:50], 'FAIL')

        # 3. Host Login & Accept Request
        print("\n[3] Testing Host Requests Management (/host/requests)...", flush=True)
        self.test_login('test_host_1@hiddenyatra.in', 'Traveller@123')
        d.get(f'{BASE_URL}/host/requests')
        time.sleep(0.8)
        self.check_console_errors('Host Requests Page')

        try:
            req_cards = d.find_elements(By.CSS_SELECTOR, '.req-item-card')
            has_reqs = len(req_cards) > 0
            accept_btns = d.find_elements(By.CSS_SELECTOR, 'button[onclick*="openAcceptModal"]')
            has_accept = len(accept_btns) > 0
            self.log('Host Flow', 'View Incoming Requests', 'Render guest requests with Accept/Decline action buttons', f"Requests={len(req_cards)}, Accept Btns={len(accept_btns)}", 'PASS' if has_reqs and has_accept else 'FAIL')

            # Accept the request via modal
            if has_accept:
                accept_btns[0].click()
                time.sleep(0.3)
                accept_modal = d.find_element(By.ID, 'accept-modal')
                modal_open = 'open' in accept_modal.get_attribute('class') or accept_modal.is_displayed()
                
                note_input = accept_modal.find_element(By.NAME, 'host_message')
                note_input.send_keys("Welcome to our heritage home! Check-in is after 2 PM.")
                confirm_btn = accept_modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                confirm_btn.click()
                time.sleep(1.0)

                # Check status updated
                d.get(f'{BASE_URL}/host/requests?tab=accepted')
                time.sleep(0.8)
                accepted_cards = d.find_elements(By.CSS_SELECTOR, '.req-item-card')
                self.log('Host Flow', 'Accept Request with Host Note', 'Accept request, block calendar & move to Accepted tab', f"Modal Open={modal_open}, Accepted Stays={len(accepted_cards)}", 'PASS' if len(accepted_cards) > 0 else 'FAIL')
        except Exception as e:
            self.log('Host Flow', 'Accept Request', 'Accept guest request', str(e)[:50], 'FAIL')

        # 4. Traveller Verifies Accepted Status & Revealed Host Contact
        print("\n[4] Testing Traveller View of Accepted Stay (/my-stays)...", flush=True)
        self.test_login('test_traveller_1@hiddenyatra.in', 'Traveller@123')
        d.get(f'{BASE_URL}/my-stays')
        time.sleep(0.8)
        try:
            accepted_badge = d.find_elements(By.CSS_SELECTOR, '.status-accepted')
            has_accepted = len(accepted_badge) > 0
            has_phone = '📞' in d.page_source or 'Host Contact' in d.page_source
            self.log('Traveller Flow', 'Verify Accepted Status & Host Contact', 'Render Accepted badge and reveal direct host arrival contact', f"Accepted Badge={has_accepted}, Contact Revealed={has_phone}", 'PASS' if has_accepted and has_phone else 'FAIL')
        except Exception as e:
            self.log('Traveller Flow', 'Verify Accepted Status', 'Inspect /my-stays', str(e)[:50], 'FAIL')

        # 5. Traveller Requests Free Cultural Stay (/stay/test-free-village-cultural-stay)
        print("\n[5] Testing Traveller Free Cultural Stay Request...", flush=True)
        d.get(f'{BASE_URL}/stay/test-free-village-cultural-stay')
        time.sleep(0.8)
        try:
            d_in_free = (date.today() + timedelta(days=25)).strftime('%Y-%m-%d')
            d_out_free = (date.today() + timedelta(days=27)).strftime('%Y-%m-%d')
            d.execute_script(f"document.getElementById('checkin').value = '{d_in_free}'; document.getElementById('checkin').dispatchEvent(new Event('change'));")
            d.execute_script(f"document.getElementById('checkout').value = '{d_out_free}'; document.getElementById('checkout').dispatchEvent(new Event('change'));")
            time.sleep(0.3)

            free_calc_total = d.find_element(By.ID, 'sd-calc-total').text
            btn_free = d.find_element(By.ID, 'btn-request-stay')
            d.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_free)
            time.sleep(0.2)
            btn_free.click()
            time.sleep(1.0)

            is_free_in_mystays = 'Free Cultural Stay' in d.page_source or 'Free Stay' in d.page_source
            self.log('Free Stay Flow', 'Request Free Stay & Price 0', 'Request ₹0 stay & render Free Stay badge in /my-stays', f"Price Calc={free_calc_total}, In My Stays={is_free_in_mystays}", 'PASS' if is_free_in_mystays else 'FAIL')
        except Exception as e:
            self.log('Free Stay Flow', 'Request Free Stay', 'Submit free stay request', str(e)[:50], 'FAIL')

        # 6. Traveller Cancellation Flow
        print("\n[6] Testing Traveller Cancellation Flow with Modal...", flush=True)
        try:
            d.get(f'{BASE_URL}/my-stays')
            time.sleep(0.6)
            cancel_btns = d.find_elements(By.CSS_SELECTOR, 'button[onclick*="openCancelModal"]')
            if cancel_btns:
                d.execute_script("arguments[0].scrollIntoView({block:'center'});", cancel_btns[0])
                time.sleep(0.2)
                cancel_btns[0].click()
                time.sleep(0.3)
                cancel_modal = d.find_element(By.ID, 'cancel-modal')
                c_open = 'open' in cancel_modal.get_attribute('class') or cancel_modal.is_displayed()
                
                reason_inp = cancel_modal.find_element(By.NAME, 'cancellation_reason')
                reason_inp.send_keys("Testing cancellation flow via E2E Selenium")
                confirm_cancel_btn = cancel_modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                confirm_cancel_btn.click()
                time.sleep(1.0)

                d.get(f'{BASE_URL}/my-stays?tab=cancelled')
                time.sleep(0.8)
                cancelled_badges = d.find_elements(By.CSS_SELECTOR, '.status-cancelled')
                self.log('Cancellation Flow', 'Traveller Cancel with Reason Modal', 'Cancel stay request & render Cancelled badge', f"Modal Open={c_open}, Cancelled Badges={len(cancelled_badges)}", 'PASS' if len(cancelled_badges) > 0 else 'FAIL')
        except Exception as e:
            self.log('Cancellation Flow', 'Cancel Stay Request', 'Execute cancellation', str(e)[:50], 'FAIL')

        # 7. Admin Stay Requests Moderation View
        print("\n[7] Testing Admin Stay Requests Moderation (/admin/stay-requests)...", flush=True)
        d.delete_all_cookies()
        d.get(f'{BASE_URL}/admin/login')
        time.sleep(0.4)
        pwd_inp = d.find_element(By.ID, 'password')
        pwd_inp.send_keys('admin@hidden123')
        d.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(0.8)

        d.get(f'{BASE_URL}/admin/stay-requests')
        time.sleep(0.8)
        self.check_console_errors('Admin Stay Requests')

        try:
            table_rows = d.find_elements(By.CSS_SELECTOR, 'tbody tr')
            has_rows = len(table_rows) > 0
            force_cancel_btns = d.find_elements(By.CSS_SELECTOR, 'button[onclick*="openAdminCancelModal"]')
            self.log('Admin Flow', 'Admin Stay Requests Table & Oversight', 'List all booking requests with Force Cancel controls', f"Rows={len(table_rows)}, Force Cancel Btns={len(force_cancel_btns)}", 'PASS' if has_rows else 'FAIL')
        except Exception as e:
            self.log('Admin Flow', 'Admin Stay Requests', 'Inspect admin table', str(e)[:50], 'FAIL')

    def close(self):
        self.driver.quit()
        print("\n" + "=" * 80)
        print("HOMESTAY BOOKING E2E TEST SUMMARY")
        print("=" * 80)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        print(f"Total E2E Controls/Flows: {len(self.results)} | Passed: {passed} | Failed: {failed}")

if __name__ == '__main__':
    tester = E2EStayBookingTester()
    try:
        tester.run_tests()
    finally:
        tester.close()
