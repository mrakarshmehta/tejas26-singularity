"""
Comprehensive Audit of Jamui Place Images
"""
import os, sys
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import urllib.request
import subprocess
from models.connection import get_cursor

def audit_images():
    print("=" * 80)
    print("AUDIT: JAMUI PLACE IMAGES (LOCAL DB vs LOCAL DISK vs GIT vs LIVE RENDER)")
    print("=" * 80)
    
    # 1. Fetch Jamui places from local DB
    with get_cursor() as cur:
        cur.execute("SELECT id, name, slug, category, cover_image, is_featured, is_hidden_gem FROM places WHERE district_id = (SELECT id FROM districts WHERE slug='jamui' LIMIT 1) ORDER BY id")
        places = cur.fetchall()
        
    print(f"Total Jamui places in local DB: {len(places)}\n")
    
    audit_results = []
    
    for p in places:
        c_img = p.get('cover_image') or ''
        local_path = os.path.join('static', 'uploads', 'places', c_img) if c_img else None
        local_exists = os.path.exists(local_path) if local_path else False
        local_size = os.path.getsize(local_path) if local_exists else 0
        
        # Check Git status for this file
        git_tracked = False
        if local_exists:
            res = subprocess.run(['git', 'ls-files', local_path], capture_output=True, text=True)
            git_tracked = bool(res.stdout.strip())
            
        # Check Live URL
        live_url = f"https://hiddenyatra.onrender.com/static/uploads/places/{c_img}" if c_img else None
        live_status = None
        if live_url:
            try:
                req = urllib.request.Request(live_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    live_status = resp.getcode()
            except urllib.error.HTTPError as e:
                live_status = e.code
            except Exception as e:
                live_status = str(e)
                
        audit_results.append({
            'id': p['id'],
            'name': p['name'],
            'slug': p['slug'],
            'category': p['category'],
            'cover_image': c_img,
            'local_path': local_path,
            'local_exists': local_exists,
            'local_size_kb': round(local_size / 1024, 1) if local_size else 0,
            'git_tracked': git_tracked,
            'live_url': live_url,
            'live_status': live_status
        })
        
        print(f"Place [{p['id']}] {p['name']} ({p['slug']}):")
        print(f"  - DB cover_image: '{c_img}'")
        print(f"  - Local File: {local_path} (Exists: {local_exists}, Size: {round(local_size/1024, 1)} KB)")
        print(f"  - Git Tracked: {git_tracked}")
        print(f"  - Live URL: {live_url} -> Status: {live_status}")
        print("-" * 60)
        
    with open('scratch/jamui_images_audit.json', 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=2)
        
    # Check all files in static/uploads/places/
    all_place_files = os.listdir('static/uploads/places')
    print(f"\nAll files in static/uploads/places/ ({len(all_place_files)} files):")
    for f in sorted(all_place_files):
        fpath = os.path.join('static', 'uploads', 'places', f)
        sz = os.path.getsize(fpath)
        res = subprocess.run(['git', 'ls-files', fpath], capture_output=True, text=True)
        tracked = bool(res.stdout.strip())
        print(f"  - {f:25s} ({round(sz/1024, 1):7.1f} KB) Tracked: {tracked}")

if __name__ == '__main__':
    audit_images()
