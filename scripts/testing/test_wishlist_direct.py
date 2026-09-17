import urllib.request
import json
import re

BASE = 'http://127.0.0.1:5000'
req = urllib.request.Request(f'{BASE}/place/kakolat-waterfall', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    cookies = resp.headers.get_all('Set-Cookie') or []
    html = resp.read().decode('utf-8')

cookie_header = '; '.join(c.split(';')[0] for c in cookies)
m = re.search(r'window\.HY_CSRF_TOKEN = "([^"]+)"', html)
csrf = m.group(1) if m else ''
print(f'CSRF: {csrf[:15]}..., Cookies: {cookie_header}')

# Test Add Wishlist
req_add = urllib.request.Request(f'{BASE}/wishlist/add/16', data=b'{}', headers={
    'User-Agent': 'Mozilla/5.0',
    'Cookie': cookie_header,
    'Content-Type': 'application/json',
    'X-CSRF-Token': csrf
}, method='POST')
try:
    with urllib.request.urlopen(req_add) as resp_add:
        print('Add response:', resp_add.status, resp_add.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('Add failed:', e.code, e.read().decode('utf-8'))

# Test Status
req_st = urllib.request.Request(f'{BASE}/wishlist/status/16', headers={
    'User-Agent': 'Mozilla/5.0',
    'Cookie': cookie_header,
})
with urllib.request.urlopen(req_st) as resp_st:
    print('Status response:', resp_st.status, resp_st.read().decode('utf-8'))

# Test Remove Wishlist
req_rem = urllib.request.Request(f'{BASE}/wishlist/remove/16', data=b'{}', headers={
    'User-Agent': 'Mozilla/5.0',
    'Cookie': cookie_header,
    'Content-Type': 'application/json',
    'X-CSRF-Token': csrf
}, method='POST')
with urllib.request.urlopen(req_rem) as resp_rem:
    print('Remove response:', resp_rem.status, resp_rem.read().decode('utf-8'))
