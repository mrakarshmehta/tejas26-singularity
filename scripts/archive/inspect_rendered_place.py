import sys
sys.path.insert(0, '.')
from app import create_app
app = create_app()
with app.test_request_context('/place/golghar'):
    with app.test_client() as client:
        r = client.get('/place/golghar')
        html = r.get_data(as_text=True)
        print("HTML length:", len(html))
        print("Contains 'maps.googleapis.com':", "maps.googleapis.com" in html)
        # Find where extra_js is rendered
        idx = html.find('/static/js/map.js')
        if idx != -1:
            print("Around map.js:\n", html[idx-300:idx+200])
        else:
            print("map.js not found in rendered HTML!")
