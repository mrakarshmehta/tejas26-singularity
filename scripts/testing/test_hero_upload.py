from app import create_app
from config import ADMIN_PASSWORD
import io
import re
from PIL import Image

app = create_app()
client = app.test_client()

g = client.get('/admin/login')
html = g.data.decode('utf-8')
m = re.search(r'name="_csrf_token" value="([^"]+)"', html)
csrf_token = m.group(1) if m else ''

login_res = client.post('/admin/login', data={'password': ADMIN_PASSWORD, '_csrf_token': csrf_token})
print('Login status code:', login_res.status_code)
print('Login location:', login_res.headers.get('Location'))

img = Image.new('RGB', (100, 100), color = 'red')
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='JPEG')
img_byte_arr.seek(0)

data = {
    'media': (img_byte_arr, 'test_hero_bg.jpg'),
    'title': 'Test Hero Upload',
    '_csrf_token': csrf_token
}

response = client.post('/admin/hero-media/upload', data=data, content_type='multipart/form-data')
print('Upload status code:', response.status_code)
print('Location header:', response.headers.get('Location'))
