import requests
from bs4 import BeautifulSoup
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

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

def duckduckgo_search(query, domain):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = []

        for a in soup.select("a.result__url"):
            href = a.get("href")
            if href and domain in href:
                links.append(href)

        return links or [f"[!] No results found for: {query}"]
    except Exception as e:
        return [f"[!] Error during search: {str(e)}"]

def perform_dorking(site):
    results = []
    count = 1
    for dork in DORKS:
        query = dork.format(site=site)
        print(f"[+] Dorking: {query}")
        links = duckduckgo_search(query, site)
        for link in links:
            print(f"[{count}] {link}")
            results.append(link)
            count += 1
        print("-" * 50)
    return results
