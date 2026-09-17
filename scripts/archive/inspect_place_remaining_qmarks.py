import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
import requests, re

BASE = "http://127.0.0.1:5000"
r = requests.get(f"{BASE}/place/golghar")

for line_no, line in enumerate(r.text.splitlines(), 1):
    if '???' in line:
        print(f"Line {line_no}: {line.strip()[:140]}")
