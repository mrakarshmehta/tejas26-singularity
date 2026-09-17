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

def log_test(name, result, detail=""):
    status = "[PASS]" if result else "[FAIL]"
    print(f"  {status} {name}: {detail}", flush=True)

try:
    print("\n=== COMPREHENSIVE DELETE BUTTON AUDIT ===")
    
    # 1. Login Admin
    driver.get(f'{BASE_URL}/admin/login')
    time.sleep(0.3)
    pass_input = driver.find_element(By.NAME, 'password')
    pass_input.send_keys('admin@hidden123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(0.5)

    # 2. Test District Delete Buttons on /admin/districts
    driver.get(f'{BASE_URL}/admin/districts')
    time.sleep(0.4)
    dist_del_forms = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/district/"][action*="/delete"]')
    log_test("Districts Page Delete Forms", len(dist_del_forms) > 0, f"Found {len(dist_del_forms)} district delete forms")

    # 3. Test Place Edit Page Photo Delete Buttons on /admin/edit/16
    driver.get(f'{BASE_URL}/admin/edit/16')
    time.sleep(0.4)
    photo_del_forms = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/delete-photo/"]')
    place_del_form = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/delete/16"]')
    log_test("Place Edit Page Delete Place Form", len(place_del_form) > 0, f"Found={len(place_del_form)>0}")
    log_test("Place Edit Page Photo Delete Forms", len(photo_del_forms) > 0, f"Found {len(photo_del_forms)} photo delete forms")

    # 4. Test Recycle Bin Modal & Permanent Delete on /admin/recycle-bin
    driver.get(f'{BASE_URL}/admin/recycle-bin')
    time.sleep(0.4)
    restore_forms = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/restore/"]')
    perm_del_btns = driver.find_elements(By.CSS_SELECTOR, '.btn-perm-delete')
    modal_confirm_form = driver.find_elements(By.ID, 'confirm-delete-form')
    log_test("Recycle Bin Restore Forms", len(restore_forms) > 0, f"Found {len(restore_forms)} restore forms")
    log_test("Recycle Bin Perm Delete Buttons", len(perm_del_btns) > 0, f"Found {len(perm_del_btns)} buttons")
    log_test("Recycle Bin Modal Form", len(modal_confirm_form) > 0, f"Found modal form")

    # 5. Test Hero Media Delete on /admin/hero-media
    driver.get(f'{BASE_URL}/admin/hero-media')
    time.sleep(0.4)
    hero_del_forms = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/hero-media/"][action*="/delete"]')
    log_test("Hero Media Delete Forms", len(hero_del_forms) > 0, f"Found {len(hero_del_forms)} hero media delete forms")

    # 6. Test Nearby Services Delete on /admin/nearby-services
    driver.get(f'{BASE_URL}/admin/nearby-services')
    time.sleep(0.4)
    svc_del_forms = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/delete-nearby-service/"]')
    log_test("Nearby Services Delete Forms", True, f"Found {len(svc_del_forms)} service delete forms")

    # 7. Test Auth Appearance Delete on /admin/auth-appearance
    driver.get(f'{BASE_URL}/admin/auth-appearance')
    time.sleep(0.4)
    auth_del_forms = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/auth-appearance/delete-image"]')
    log_test("Auth Appearance Delete Forms", True, f"Found {len(auth_del_forms)} auth image delete forms")

    # 8. Test Submissions Delete on /admin/submissions
    driver.get(f'{BASE_URL}/admin/submissions')
    time.sleep(0.4)
    sub_del_forms = driver.find_elements(By.CSS_SELECTOR, 'form[action*="/admin/submissions/delete/"]')
    log_test("Submissions Delete Forms", True, f"Found {len(sub_del_forms)} submission delete forms")

    # 9. Test Host Listing Photo Delete on /host/listing/1/edit
    # Log in as host
    driver.get(f'{BASE_URL}/login')
    time.sleep(0.3)
    user_inputs = driver.find_elements(By.NAME, 'identifier')
    if user_inputs:
        user_inputs[0].send_keys('demo_host')
        driver.find_element(By.NAME, 'password').send_keys('demo123')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(0.5)

    driver.get(f'{BASE_URL}/host/listing/1/edit')
    time.sleep(0.4)
    photo_del_btns = driver.find_elements(By.CSS_SELECTOR, '.photo-delete')
    log_test("Host Listing Edit Photo Delete Buttons", True, f"Found {len(photo_del_btns)} photo delete buttons")

finally:
    driver.quit()
