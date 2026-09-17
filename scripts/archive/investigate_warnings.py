"""Investigate '???' and 'placeholder' false positives."""
import sys, io, re, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://127.0.0.1:5000"
s = requests.Session()

# Check if 'placeholder' is just HTML attributes
print("=== PLACEHOLDER INVESTIGATION ===")
r = s.get(f"{BASE}/", timeout=10)
text = r.text
# Find 'placeholder' outside of HTML attrs
attr_matches = len(re.findall(r'placeholder\s*=\s*["\']', text))
visible_matches = len(re.findall(r'(?<![\w="\'])placeholder(?![\w="\'])', text, re.IGNORECASE))
print(f"Homepage: {attr_matches} HTML placeholder attrs, {visible_matches} possible visible 'placeholder' text")

# Check food culture ??? specifically
print("\n=== FOOD & CULTURE '???' INVESTIGATION ===")
r = s.get(f"{BASE}/food-culture", timeout=10)
text = r.text
lines = text.split('\n')
for i, line in enumerate(lines):
    if '???' in line:
        # Get context
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean:
            print(f"  Line {i+1}: {clean[:120]}")

# Check homepage ???
print("\n=== HOMEPAGE '???' INVESTIGATION ===")
r = s.get(f"{BASE}/", timeout=10)
text = r.text
lines = text.split('\n')
for i, line in enumerate(lines):
    if '???' in line:
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean:
            print(f"  Line {i+1}: {clean[:120]}")

# Check place detail ??? (Golghar)
print("\n=== GOLGHAR '???' INVESTIGATION ===")
r = s.get(f"{BASE}/place/golghar", timeout=10)
text = r.text
lines = text.split('\n')
for i, line in enumerate(lines):
    if '???' in line:
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean:
            print(f"  Line {i+1}: {clean[:120]}")

# Check empty img src
print("\n=== EMPTY IMG SRC INVESTIGATION ===")
r = s.get(f"{BASE}/place/golghar", timeout=10)
empty_imgs = re.findall(r'<img[^>]*src\s*=\s*["\'][\s]*["\'][^>]*>', r.text)
for img in empty_imgs[:5]:
    print(f"  {img[:150]}")
# Also check if these are just onerror fallback patterns
onerror_imgs = re.findall(r'<img[^>]*src\s*=\s*["\'][^"\']+["\'][^>]*onerror[^>]*>', r.text)
print(f"  Images with onerror fallback: {len(onerror_imgs)}")

# Check state/bihar ???
print("\n=== STATE BIHAR '???' INVESTIGATION ===")
r = s.get(f"{BASE}/state/bihar", timeout=10)
text = r.text
lines = text.split('\n')
for i, line in enumerate(lines):
    if '???' in line:
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean:
            print(f"  Line {i+1}: {clean[:120]}")

# Verify actual place count from explore
print("\n=== ACTUAL PLACE COUNT ===")
r = s.get(f"{BASE}/explore", timeout=10)
# Try different patterns
patterns = [
    r'var\s+placesData\s*=\s*\[',
    r'const\s+placesData\s*=\s*\[',
    r'let\s+placesData\s*=\s*\[',
    r'placesData\s*=\s*\[',
]
for pat in patterns:
    m = re.search(pat, r.text)
    if m:
        # Count objects in array
        start = m.end() - 1  # Include the [
        depth = 0
        count = 0
        for c in r.text[start:start+500000]:
            if c == '{':
                if depth == 1:
                    count += 1
                depth += 1
            elif c == '}':
                depth -= 1
            elif c == '[' and depth == 0:
                depth = 1
            elif c == ']' and depth == 1:
                break
        print(f"  Pattern '{pat[:30]}...' found, ~{count} place objects")
        break
else:
    # Try to find the places data differently
    # Search for how places are loaded
    place_loads = re.findall(r'(?:places|markers|locations)\s*(?:Data|Array)?\s*=\s*\[', r.text)
    print(f"  Place data patterns found: {len(place_loads)}")
    # Check template-injected data
    jinja_data = re.findall(r'\{\{.*places.*\}\}', r.text)
    print(f"  Jinja place injections: {len(jinja_data)}")
