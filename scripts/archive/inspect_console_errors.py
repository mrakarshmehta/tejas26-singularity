import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

try:
    driver.get('http://127.0.0.1:5000/stays')
    logs = driver.get_log('browser')
    print("=== /stays CONSOLE LOGS ===")
    for entry in logs:
        print(f"[{entry['level']}] {entry['message']}")

    driver.get('http://127.0.0.1:5000/stay/rajgir-green-valley-eco-homestay')
    logs2 = driver.get_log('browser')
    print("\n=== /stay/rajgir CONSOLE LOGS ===")
    for entry in logs2:
        print(f"[{entry['level']}] {entry['message']}")
finally:
    driver.quit()
