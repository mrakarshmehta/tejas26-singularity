import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()
from app import create_app

app = create_app()
print("=== REGISTERED FLASK ROUTES ===")
for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    if '/api/' in rule.rule:
        print(f"{rule.rule:45} -> methods: {rule.methods}")
