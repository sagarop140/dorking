from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.utils import set_env_var
from bs4 import BeautifulSoup
import time
import urllib.parse
import os

# Optional: Use GitHub token to avoid API rate limits on Render
set_env_var("GH_TOKEN", os.environ.get("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"))

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

def init_browser():
    options = FirefoxOptions()
    options.add_argument("--headless")
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def duckduckgo_search(driver, query):
    search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
    driver.get(search_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []

    for a_tag in soup.find_all('a', class_='result__a'):
        href = a_tag.get('href')
        if href and 'uddg=' in href:
            parsed = urllib.parse.urlparse(href)
            query_params = urllib.parse.parse_qs(parsed.query)
            real_url = query_params.get('uddg', [None])[0]
            if real_url:
                results.append(urllib.parse.unquote(real_url))
        elif href:
            results.append(href)
    return results

def perform_dorking(site):
    driver = init_browser()
    all_results = []
    for dork in DORKS:
        query = dork.format(site=site)
        results = duckduckgo_search(driver, query)
        all_results.extend(results)
    driver.quit()
    return all_results
