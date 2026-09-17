import sys
sys.path.insert(0, '.')
from app import create_app
app = create_app()
with app.test_request_context('/place/golghar'):
    with app.test_client() as client:
        r = client.get('/place/golghar')
        print("Status:", r.status_code)
        from config import MAP_ENGINE, GOOGLE_MAPS_API_KEY
        print("config.MAP_ENGINE:", MAP_ENGINE)
        print("config.GOOGLE_MAPS_API_KEY:", bool(GOOGLE_MAPS_API_KEY), len(GOOGLE_MAPS_API_KEY))
        # check template context
        from flask import render_template
        # check if context processor ran
        ctx = app.context_processor
        print("Context processors:", len(app.template_context_processors[None]))
        for cp in app.template_context_processors[None]:
            try:
                res = cp()
                print("CP returned keys:", list(res.keys()))
            except Exception as e:
                print("CP error:", e)
