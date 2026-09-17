import urllib.request
import urllib.parse
import http.cookiejar
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

try:
    resp = opener.open('https://hiddenyatra.onrender.com/admin/login')
    html = resp.read().decode('utf-8')
    print('GET /admin/login Status:', resp.status)
    
    m = re.search(r'name=["\']_csrf_token["\']\s+value=["\']([^"\']+)["\']', html)
    if not m:
        m = re.search(r'value=["\']([^"\']+)["\']\s+name=["\']_csrf_token["\']', html)
    csrf = m.group(1) if m else ''
    print('CSRF Token found:', csrf[:10] if csrf else 'NONE')
    
    # Try with admin@hidden123
    data = urllib.parse.urlencode({'_csrf_token': csrf, 'password': 'admin@hidden123'}).encode('utf-8')
    req = urllib.request.Request('https://hiddenyatra.onrender.com/admin/login', data=data)
    post_resp = opener.open(req)
    final_url = post_resp.geturl()
    print('POST Final URL:', final_url)
    post_html = post_resp.read().decode('utf-8')
    if 'Invalid password' in post_html:
        print('Result: Invalid password on Render')
    elif 'admin' in final_url or 'dashboard' in final_url or 'places' in final_url:
        print('Result: SUCCESS! Logged into Admin on Render')
    else:
        print('Result: URL =', final_url)
except Exception as e:
    print('Error testing live login:', e)
