import requests
from bs4 import BeautifulSoup
import urllib.parse

# Search headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Common dork payloads
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

def bing_search(query):
    """Scrape Bing search results for the given query"""
    search_url = f"https://www.bing.com/search?q={urllib.parse.quote_plus(query)}"
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        for h2 in soup.find_all('h2'):
            a = h2.find('a')
            if a and a.get('href'):
                links.append(a['href'])

        return links
    except Exception as e:
        return [f"[!] Request failed: {str(e)}"]

def perform_dorking(site):
    """Run all dorks against the provided site and collect logs"""
    logs = []
    for dork in DORKS:
        query = dork.format(site=site)
        logs.append(f"[+] Dorking: {query}")
        results = bing_search(query)

        if not results:
            logs.append("[!] No results found.")
        else:
            for i, result in enumerate(results, start=1):
                logs.append(f"[{i}] {result}")
        logs.append("-" * 60)
    return logs
