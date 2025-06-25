import requests
from bs4 import BeautifulSoup

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
    'site:{site} inurl:storemanager/contents/item.php?page_code='
]

def mojeek_search(query, domain):
    url = f"https://www.mojeek.com/search?q={requests.utils.quote(query)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = []

        # Only look at result-title anchors which contain actual results
        for a in soup.select('a.result-title'):
            href = a.get('href')
            if href and href.startswith('http') and domain in href:
                links.append(href)

        return links

    except requests.exceptions.RequestException as e:
        print(f"[!] Mojeek request failed: {e}")
        return []

def perform_dorking(site):
    logs = []
    for dork in DORKS:
        query = dork.format(site=site)
        logs.append(f"[+] Dorking: {query}")
        results = mojeek_search(query, site)

        if results:
            for i, link in enumerate(results, 1):
                logs.append(f"[{i}] {link}")
        else:
            logs.append("[!] No valid links from target domain found.")
        logs.append("-" * 60)
    return logs
