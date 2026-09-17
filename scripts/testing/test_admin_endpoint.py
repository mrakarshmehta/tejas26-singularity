import sys
import os
sys.path.insert(0, r'd:\HiddenYatra')
import requests
from app import create_app

app = create_app()
found = False
for rule in app.url_map.iter_rules():
    if 'stay-requests' in rule.rule:
        print('Registered Rule:', rule.rule, 'Endpoint:', rule.endpoint)
        found = True

if not found:
    print('Rule NOT registered in app!')

s = requests.Session()
r1 = s.get('http://127.0.0.1:5000/admin/login')
import re
m = re.search(r'name="_csrf_token"\s+value="([^"]+)"', r1.text)
token = m.group(1) if m else ''

r2 = s.post('http://127.0.0.1:5000/admin/login', data={'password': 'admin@hidden123', '_csrf_token': token})
print('Login Status:', r2.status_code, 'Final URL:', r2.url)

# Test stay-requests
r3 = s.get('http://127.0.0.1:5000/admin/stay-requests')
print('GET /admin/stay-requests ->', r3.status_code)
if r3.status_code != 200:
    # Try with test_client
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['admin_logged_in'] = True
        tc_res = c.get('/admin/stay-requests')
        print('Flask test_client GET /admin/stay-requests ->', tc_res.status_code)
