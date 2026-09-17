"""
Fetch and parse live district data from https://hiddenyatra.onrender.com/state/bihar/<slug>
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_live_district(district_slug):
    url = f"https://hiddenyatra.onrender.com/state/bihar/{district_slug}"
    print(f"Scraping live: {url}")
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,900')
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    
    data = {}
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(2)
        
        data = driver.execute_script("""
            const d = {
                url: window.location.href,
                title: document.title,
                heading: document.querySelector('.dist-hero-content h1')?.innerText?.trim() || '',
                subtitle: document.querySelector('.dist-hero-sub')?.innerText?.trim() || '',
                tags: Array.from(document.querySelectorAll('.dist-hero-tag')).map(el => el.innerText.trim()),
                cover_bg: document.querySelector('.dist-hero-bg')?.style?.background || '',
                stats: {},
                blocks: [],
                places_from_map_attr: [],
                places_from_cards: [],
                foods: [],
                related_districts: []
            };

            // Extract stats
            document.querySelectorAll('.dist-stat-pill').forEach(el => {
                const val = el.querySelector('.dist-stat-pill-val')?.innerText?.trim() || '';
                const lbl = el.querySelector('.dist-stat-pill-lbl')?.innerText?.trim() || '';
                if (lbl) d.stats[lbl] = val;
            });

            // Extract places JSON from #district-map data-places attribute
            const mapEl = document.getElementById('district-map');
            if (mapEl && mapEl.getAttribute('data-places')) {
                try {
                    d.places_from_map_attr = JSON.parse(mapEl.getAttribute('data-places'));
                } catch(e) {
                    d.places_from_map_attr_error = e.toString();
                }
            }

            // Extract places cards
            document.querySelectorAll('.place-directory-item, .dist-places-grid > div').forEach(el => {
                const name = el.querySelector('h3, .card-title, h4')?.innerText?.trim() || '';
                const cat = el.getAttribute('data-category') || el.querySelector('.badge, .category-badge')?.innerText?.trim() || '';
                const lat = el.getAttribute('data-lat') || '';
                const lng = el.getAttribute('data-lng') || '';
                const gem = el.querySelector('.gem-badge, .is-gem') ? true : false;
                const img = el.querySelector('img')?.getAttribute('src') || el.querySelector('.card-img, .place-card-img')?.style?.backgroundImage || '';
                
                if (name) {
                    d.places_from_cards.push({
                        name: name,
                        category: cat,
                        latitude: lat,
                        longitude: lng,
                        is_gem: gem,
                        img: img
                    });
                }
            });

            // Extract blocks
            document.querySelectorAll('.dist-block-card').forEach(el => {
                const name = el.querySelector('.dist-block-name')?.innerText?.trim() || '';
                const count = el.querySelector('.dist-block-count')?.innerText?.trim() || '';
                const href = el.getAttribute('href') || '';
                if (name) {
                    d.blocks.push({ name, count, href });
                }
            });

            // Extract foods
            document.querySelectorAll('.dist-food-card').forEach(el => {
                const name = el.querySelector('.dist-food-name')?.innerText?.trim() || '';
                const desc = el.querySelector('.dist-food-desc')?.innerText?.trim() || '';
                const emoji = el.querySelector('.dist-food-emoji')?.innerText?.trim() || '';
                const where = el.querySelector('.dist-food-where')?.innerText?.trim() || '';
                if (name) {
                    d.foods.push({ name, desc, emoji, where });
                }
            });

            // Extract related districts
            document.querySelectorAll('.dist-related-card').forEach(el => {
                const name = el.querySelector('.dist-related-name')?.innerText?.trim() || '';
                const count = el.querySelector('.dist-related-meta')?.innerText?.trim() || '';
                const href = el.getAttribute('href') || '';
                if (name) {
                    d.related_districts.push({ name, count, href });
                }
            });

            return d;
        """)
        print(f"Scraped {district_slug}: {len(data.get('places_from_map_attr', []))} map places, {len(data.get('places_from_cards', []))} cards, {len(data.get('blocks', []))} blocks, {len(data.get('foods', []))} foods")
    except Exception as e:
        print(f"Error scraping {district_slug}: {e}")
    finally:
        driver.quit()
        
    return data

if __name__ == '__main__':
    jamui_live = scrape_live_district('jamui')
    gaya_live = scrape_live_district('gaya-ji')
    patna_live = scrape_live_district('patna')
    
    with open('scratch/live_district_data.json', 'w', encoding='utf-8') as f:
        json.dump({'jamui': jamui_live, 'gaya_ji': gaya_live, 'patna': patna_live}, f, indent=2)
    print("Live district data saved to scratch/live_district_data.json")
