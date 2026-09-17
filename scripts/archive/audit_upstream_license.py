"""
Inspect exact upstream license and commit details from datta07/INDIAN-SHAPEFILES.
"""

import urllib.request
import json

def audit_license():
    repo_url = "https://api.github.com/repos/datta07/INDIAN-SHAPEFILES"
    license_url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/LICENSE"
    readme_url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/README.md"
    commits_url = "https://api.github.com/repos/datta07/INDIAN-SHAPEFILES/commits?path=STATES/BIHAR/BIHAR_SUBDISTRICTS.geojson&page=1&per_page=1"

    req_headers = {'User-Agent': 'HiddenYatra-Audit/1.0'}

    print("1. Fetching LICENSE...")
    try:
        req = urllib.request.Request(license_url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            lic = r.read().decode('utf-8', errors='ignore')
            print("--- LICENSE CONTENT ---")
            print(lic.strip())
            print("-----------------------")
    except Exception as e:
        print("Error fetching LICENSE:", e)

    print("\n2. Fetching README metadata...")
    try:
        req = urllib.request.Request(readme_url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            readme = r.read().decode('utf-8', errors='ignore')
            print("--- README CONTENT ---")
            print(readme[:600].strip())
            print("----------------------")
    except Exception as e:
        print("Error fetching README:", e)

    print("\n3. Fetching latest commit for BIHAR_SUBDISTRICTS.geojson...")
    try:
        req = urllib.request.Request(commits_url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            commits = json.loads(r.read().decode('utf-8'))
            if commits:
                commit = commits[0]
                print(f"Latest Commit SHA: {commit.get('sha')}")
                print(f"Commit Date: {commit.get('commit', {}).get('committer', {}).get('date')}")
                print(f"Commit Message: {commit.get('commit', {}).get('message')}")
    except Exception as e:
        print("Error fetching commit:", e)

if __name__ == "__main__":
    audit_license()
