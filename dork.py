from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import time

DORKS = [
    'site:{site} inurl:admin',
    'site:{site} inurl:login',
    'site:{site} inurl:wp-admin',
    'site:github.com {site} "DB_PASSWORD="',
    'site:github.com {site} "heroku_api_key"',
    'site:{site} inurl:view_items.php?id=',
    'site:{site} inurl:home.php?cat=',
    'site:{site} inurl:item_book.php?CAT=',
    'site:{site} inurl:prev_results.php?prodID=',
    'site:{site} inurl:storemanager/contents/item.php?page_code=',
]

def bing_search(query, domain):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    search_url = f"https://www.bing.com/search?q={urllib.parse.quote_plus(query)}"
    driver.get(search_url)
    time.sleep(2)

    links = []
    results = driver.find_elements(By.CSS_SELECTOR, "li.b_algo h2 a")

    for r in results:
        href = r.get_attribute("href")
        if domain in href:
            links.append(href)

    driver.quit()
    return links if links else [f"[!] No results found for: {query}"]

def perform_dorking(site):
    results = []
    count = 1
    for dork in DORKS:
        query = dork.format(site=site)
        print(f"[+] Dorking: {query}")
        links = bing_search(query, site)
        for link in links:
            print(f"[{count}] {link}")
            results.append(link)
            count += 1
        print("-" * 60)
    return results
