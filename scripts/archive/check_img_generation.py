"""
Inspect image files and which district ID was generated for which district name.
"""
import sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')

# Search for any seed or image generation scripts in the repo
img_scripts = glob.glob(r"D:\HiddenYatra\scripts\**\*.py", recursive=True)
for s in img_scripts:
    if 'image' in s.lower() or 'cover' in s.lower():
        print(f"Image script: {s}")

with open(r"D:\HiddenYatra\scratch\audit_dump.json", "r", encoding="utf-8") as f:
    import json
    data = json.load(f)

print("\nOriginal Districts dump with cover_image (from backup):")
for d in data['districts']:
    print(f"ID {d['id']:2d} | Original Name: {d['name']:25s} | Original Slug: {d['slug']:22s} | CoverImg: {d['cover_image']}")
