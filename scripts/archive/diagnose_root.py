import urllib.request
import urllib.error

url = "https://hiddenyatra.onrender.com"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        print("Status:", resp.status)
        print("Headers:", resp.headers)
        body = resp.read()
        print("Body length:", len(body))
        print("Body preview:\n", body[:500].decode('utf-8', errors='ignore'))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.reason)
    print("Body:", e.read().decode('utf-8', errors='ignore'))
except Exception as e:
    print("Error:", type(e), e)
