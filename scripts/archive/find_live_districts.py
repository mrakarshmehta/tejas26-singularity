import urllib.request
import re

def find_live_districts():
    url = 'https://hiddenyatra.onrender.com/'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        
    links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html)
    dist_links = set(l for l in links if '/state/' in l or '/district' in l)
            
    print(f"District links on LIVE Homepage ({len(dist_links)}):")
    for l in sorted(dist_links):
        print(f"  - {l}")

    # Also check /state/bihar
    try:
        url_bihar = 'https://hiddenyatra.onrender.com/state/bihar'
        req_b = urllib.request.Request(url_bihar, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_b) as resp:
            html_b = resp.read().decode('utf-8')
        links_b = set(l for l in re.findall(r'href=[\'"]([^\'"]+)[\'"]', html_b) if '/state/bihar/' in l)
        print(f"\nDistrict links on LIVE /state/bihar ({len(links_b)}):")
        for l in sorted(links_b):
            print(f"  - {l}")
    except Exception as e:
        print("Error on /state/bihar:", e)

if __name__ == '__main__':
    find_live_districts()
