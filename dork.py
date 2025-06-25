import requests
from bs4 import BeautifulSoup

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
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

def mojeek_search(query, target_domain):
    url = f"https://www.mojeek.com/search?q={requests.utils.quote(query)}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for link in soup.select("a.result-title"):
            href = link.get("href")
            if href and target_domain in href:
                results.append(href)

        return results

    except requests.RequestException as e:
        print(f"[!] Request failed: {e}")
        return []

def perform_dorking(site):
    all_results = {}
    for dork in DORKS:
        query = dork.format(site=site)
        print(f"[+] Dorking: {query}")
        results = mojeek_search(query, site)
        if results:
            for idx, link in enumerate(results, 1):
                print(f"[{idx}] {link}")
        else:
            print("[!] No valid links from target domain found.")
        print("-" * 60)
        all_results[query] = results
    return all_results
