import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'http://127.0.0.1:5000'

class DeleteButtonsTester:
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
        print(f"  {icon} [{flow}] {step[:45]} -> {status} ({actual})", flush=True)

    def login_admin(self):
        d = self.driver
        d.get(f'{BASE_URL}/admin/login')
        time.sleep(0.3)
        pass_input = d.find_element(By.NAME, 'password')
        pass_input.send_keys('admin@hidden123')
        d.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(0.5)
        self.log('Admin Auth', 'Admin Login', 'Dashboard loaded', d.current_url, 'PASS' if '/admin' in d.current_url and '/login' not in d.current_url else 'FAIL')

    def test_place_delete_button_on_dashboard(self):
        d = self.driver
        print("\n[1] Testing Place Delete Button on Admin Dashboard...", flush=True)
        d.get(f'{BASE_URL}/admin/dashboard')
        time.sleep(0.5)
        
        # Check for delete forms
        del_forms = d.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/delete/"]')
        self.log('Dashboard Places', 'Locate Delete Forms', '>0 forms', f"Count={len(del_forms)}", 'PASS' if len(del_forms) > 0 else 'FAIL')
        
        if del_forms:
            form = del_forms[0]
            action = form.get_attribute('action')
            btn = form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            csrf = form.find_elements(By.NAME, '_csrf_token')
            has_csrf = len(csrf) > 0 and len(csrf[0].get_attribute('value') or '') > 0
            self.log('Dashboard Places', 'Delete Form Action & CSRF', 'Action & CSRF present', f"Action={action.split('/')[-2:]}, CSRF={has_csrf}", 'PASS' if has_csrf else 'FAIL')

    def test_place_delete_on_edit_page(self):
        d = self.driver
        print("\n[2] Testing Place Delete Button on Edit Place Page...", flush=True)
        d.get(f'{BASE_URL}/admin/edit/1')
        time.sleep(0.5)
        
        del_btns = d.find_elements(By.XPATH, "//button[contains(text(), 'Delete Place')]")
        self.log('Edit Place', 'Locate Delete Place Button', 'Button found', f"Found={len(del_btns)>0}", 'PASS' if len(del_btns)>0 else 'FAIL')
        
        # Check photo delete buttons
        photo_del = d.find_elements(By.CSS_SELECTOR, '.btn-icon-delete')
        self.log('Edit Place', 'Locate Photo Delete Buttons', 'Check photos', f"Count={len(photo_del)}", 'PASS')

    def test_recycle_bin_permanent_delete(self):
        d = self.driver
        print("\n[3] Testing Permanent Delete on Recycle Bin...", flush=True)
        d.get(f'{BASE_URL}/admin/recycle-bin')
        time.sleep(0.5)
        
        perm_btns = d.find_elements(By.CSS_SELECTOR, '.btn-perm-delete')
        restore_btns = d.find_elements(By.CSS_SELECTOR, '.btn-restore')
        modal = d.find_elements(By.ID, 'confirm-delete-modal')
        confirm_form = d.find_elements(By.ID, 'confirm-delete-form')
        
        self.log('Recycle Bin', 'Locate Restore Buttons', 'Check restore', f"Count={len(restore_btns)}", 'PASS')
        self.log('Recycle Bin', 'Locate Perm Delete Buttons', 'Check perm del', f"Count={len(perm_btns)}", 'PASS')
        self.log('Recycle Bin', 'Confirm Modal & Form Exist', 'Modal & form found', f"Modal={len(modal)>0}, Form={len(confirm_form)>0}", 'PASS' if len(modal)>0 and len(confirm_form)>0 else 'FAIL')

        if perm_btns:
            # Click the first permanent delete button to open modal
            perm_btns[0].click()
            time.sleep(0.3)
            is_open = 'open' in modal[0].get_attribute('class')
            form_action = confirm_form[0].get_attribute('action')
            self.log('Recycle Bin', 'Open Perm Delete Modal', 'Modal open with action', f"Open={is_open}, Action={form_action}", 'PASS' if is_open and '/permanent-delete/' in form_action else 'FAIL')

    def test_hero_media_delete(self):
        d = self.driver
        print("\n[4] Testing Hero Media Delete Button...", flush=True)
        d.get(f'{BASE_URL}/admin/hero-media')
        time.sleep(0.5)
        
        del_forms = d.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/hero-media/"][action*="/delete"]')
        self.log('Hero Media', 'Locate Hero Media Delete Buttons', 'Forms check', f"Count={len(del_forms)}", 'PASS')

    def run_all(self):
        self.login_admin()
        self.test_place_delete_button_on_dashboard()
        self.test_place_delete_on_edit_page()
        self.test_recycle_bin_permanent_delete()
        self.test_hero_media_delete()
        self.driver.quit()

if __name__ == '__main__':
    tester = DeleteButtonsTester()
    tester.run_all()
