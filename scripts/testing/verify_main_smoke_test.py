import sys
import os
import requests
import re

BASE_URL = 'http://127.0.0.1:5000'

results = []

def test_get(url_path, expected_status=200, title_or_keyword=None, name=None):
    test_name = name or url_path
    url = f"{BASE_URL}{url_path}"
    try:
        r = requests.get(url, allow_redirects=True, timeout=5)
        status_ok = (r.status_code == expected_status)
        content_ok = True
        if title_or_keyword:
            content_ok = (title_or_keyword.lower() in r.text.lower())
        
        if status_ok and content_ok:
            results.append((test_name, 'PASS', f'HTTP {r.status_code}, Found: "{title_or_keyword}"' if title_or_keyword else f'HTTP {r.status_code}'))
            return True, r
        else:
            reason = f'HTTP {r.status_code} (expected {expected_status})' if not status_ok else f'Keyword "{title_or_keyword}" not found'
            results.append((test_name, 'FAIL', reason))
            return False, r
    except Exception as e:
        results.append((test_name, 'FAIL', str(e)))
        return False, None

print("="*70)
print("RUNNING POST-MERGE COMPREHENSIVE SMOKE TEST ON MAIN")
print("="*70)

# 1. Homepage
test_get('/', 200, 'HiddenYatra', '1. Homepage (/)')

# 2. Search API
test_get('/api/search/instant?q=Rajgir', 200, 'Rajgir', '2a. Search Instant API (Rajgir)')
test_get('/api/search/instant?q=temple', 200, 'results', '2b. Search Instant API (temple)')

# 3. Districts / Browse
test_get('/browse', 200, 'Bihar', '3a. Browse States (/browse)')
test_get('/state/bihar', 200, 'Districts', '3b. Bihar Districts (/state/bihar)')

# 4. Jamui District
test_get('/state/bihar/jamui', 200, 'Jamui', '4. Jamui District Page (/state/bihar/jamui)')

# 5. Nalanda District
test_get('/state/bihar/nalanda', 200, 'Nalanda', '5. Nalanda District Page (/state/bihar/nalanda)')

# 6. AI Trip Planner / Itinerary
test_get('/itinerary', 200, 'Trip', '6. AI Trip Planner / Itinerary (/itinerary)')

# 7. Local Stays Discovery
test_get('/stays', 200, 'Homestays', '7. Local Stays (/stays)')

# 8. Stay Detail
test_get('/stay/bodh-gaya-heritage-homestay', 200, 'Request', '8. Stay Detail (/stay/bodh-gaya-heritage-homestay)')

# 9. Authentication
test_get('/login', 200, 'Login', '9a. Auth Login (/login)')
test_get('/signup', 200, 'Create Account', '9b. Auth Signup (/signup)')

# 10. Wishlist
test_get('/wishlist', 200, 'Wishlist', '10. Wishlist (/wishlist)')

# 11. Host & Traveller Protected Dashboards (with user session)
s_user = requests.Session()
r_u_login = s_user.get(f'{BASE_URL}/login')
csrf_match_u = re.search(r'name="_csrf_token"\s+value="([^"]+)"', r_u_login.text)
csrf_token_u = csrf_match_u.group(1) if csrf_match_u else ''
r_u_post = s_user.post(f'{BASE_URL}/login', data={
    'email': 'test_traveller_1@hiddenyatra.in',
    'password': 'Traveller@123',
    '_csrf_token': csrf_token_u
})

r_my_stays = s_user.get(f'{BASE_URL}/my-stays')
if r_my_stays.status_code == 200 and 'My Stays' in r_my_stays.text:
    results.append(('11a. Traveller My Stays (/my-stays)', 'PASS', 'HTTP 200, Authenticated Dashboard Loaded'))
else:
    results.append(('11a. Traveller My Stays (/my-stays)', 'FAIL', f'HTTP {r_my_stays.status_code}'))

# Host session
s_host = requests.Session()
r_h_login = s_host.get(f'{BASE_URL}/login')
csrf_match_h = re.search(r'name="_csrf_token"\s+value="([^"]+)"', r_h_login.text)
csrf_token_h = csrf_match_h.group(1) if csrf_match_h else ''
r_h_post = s_host.post(f'{BASE_URL}/login', data={
    'email': 'test_host_1@hiddenyatra.in',
    'password': 'Traveller@123',
    '_csrf_token': csrf_token_h
})

r_host_req = s_host.get(f'{BASE_URL}/host/requests')
if r_host_req.status_code == 200 and 'Stay Requests' in r_host_req.text:
    results.append(('11b. Host Stay Requests (/host/requests)', 'PASS', 'HTTP 200, Host Requests Loaded'))
else:
    results.append(('11b. Host Stay Requests (/host/requests)', 'FAIL', f'HTTP {r_host_req.status_code}'))

# 12. Admin Stay Requests via Admin Session
s_admin = requests.Session()
r_login_page = s_admin.get(f'{BASE_URL}/admin/login')
csrf_match = re.search(r'name="_csrf_token"\s+value="([^"]+)"', r_login_page.text)
csrf_token = csrf_match.group(1) if csrf_match else ''
r_post = s_admin.post(f'{BASE_URL}/admin/login', data={'password': 'admin@hidden123', '_csrf_token': csrf_token})
if r_post.status_code in (200, 302):
    r_admin_stays = s_admin.get(f'{BASE_URL}/admin/stay-requests')
    if r_admin_stays.status_code == 200 and 'Stay Requests' in r_admin_stays.text:
        results.append(('12. Admin Stay Requests (/admin/stay-requests)', 'PASS', 'HTTP 200, Authenticated Table Loaded'))
    else:
        results.append(('12. Admin Stay Requests (/admin/stay-requests)', 'FAIL', f'HTTP {r_admin_stays.status_code}'))
else:
    results.append(('12. Admin Stay Requests (/admin/stay-requests)', 'FAIL', f'Admin login failed: {r_post.status_code}'))

# Database count integrity check
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_db
import pymysql.cursors
conn = get_db()
cursor = conn.cursor(pymysql.cursors.DictCursor)

cursor.execute("SELECT COUNT(*) as cnt FROM districts")
dist_cnt = cursor.fetchone()['cnt']

cursor.execute("SELECT COUNT(*) as cnt FROM places")
places_cnt = cursor.fetchone()['cnt']

cursor.execute("SELECT COUNT(*) as cnt FROM users")
users_cnt = cursor.fetchone()['cnt']

cursor.execute("SELECT COUNT(*) as cnt FROM host_listings")
listings_cnt = cursor.fetchone()['cnt']

cursor.execute("SELECT COUNT(*) as cnt FROM stay_requests")
requests_cnt = cursor.fetchone()['cnt']

cursor.execute("SELECT COUNT(*) as cnt FROM notifications")
notif_cnt = cursor.fetchone()['cnt']

conn.close()

print("\n" + "="*70)
print("SMOKE TEST RESULTS SUMMARY")
print("="*70)
all_pass = True
for name, status, detail in results:
    icon = "PASS" if status == "PASS" else "FAIL"
    if status != "PASS":
        all_pass = False
    print(f"[{icon}] {name:<50} -> {status:<6} [{detail}]")

print("\n" + "="*70)
print(f"DATABASE INTEGRITY VERIFICATION")
print("="*70)
print(f"  Districts:     {dist_cnt} (Expected: 38)")
print(f"  Places:        {places_cnt}")
print(f"  Users:         {users_cnt}")
print(f"  Host Listings: {listings_cnt}")
print(f"  Stay Requests: {requests_cnt}")
print(f"  Notifications: {notif_cnt}")

if dist_cnt == 38 and all_pass:
    print("\n>>> ALL SMOKE TESTS & DATABASE INTEGRITY CHECKS: PASS <<<")
else:
    print("\n>>> SOME CHECKS FAILED <<<")
