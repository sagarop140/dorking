import requests
from bs4 import BeautifulSoup
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

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def duckduckgo_search(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
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

    time.sleep(1)  # Be polite to DuckDuckGo
    return results

def perform_dorking(site):
    all_results = []
    for dork in DORKS:
        query = dork.format(site=site)
        results = duckduckgo_search(query)
        all_results.extend(results)
    return all_results
