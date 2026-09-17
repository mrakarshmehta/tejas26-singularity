import sys
import os
sys.path.insert(0, r'D:\HiddenYatra')

import re
from app import create_app

app = create_app()
client = app.test_client()

resp = client.get('/admin/login')
print('GET /admin/login status:', resp.status_code)
html = resp.get_data(as_text=True)

csrf_match = re.search(r'name=["\']_csrf_token["\']\s+value=["\']([^"\']+)["\']', html)
if not csrf_match:
    csrf_match = re.search(r'value=["\']([^"\']+)["\']\s+name=["\']_csrf_token["\']', html)

csrf_token = csrf_match.group(1) if csrf_match else ''
print('CSRF token:', csrf_token[:8] + '...' if csrf_token else 'NOT FOUND')

# Attempt with admin@hidden123
res = client.post('/admin/login', data={'_csrf_token': csrf_token, 'password': 'admin@hidden123'})
print('POST status:', res.status_code)
print('Redirect target:', res.headers.get('Location'))

dash = client.get('/admin/dashboard')
print('Accessing /admin/dashboard status:', dash.status_code)
print('Success - Logged into Dashboard:', 'Admin Dashboard' in dash.get_data(as_text=True) or 'Dashboard' in dash.get_data(as_text=True) or 'Moderation' in dash.get_data(as_text=True))
