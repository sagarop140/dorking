import requests
from bs4 import BeautifulSoup
import urllib.parse

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# List of Google dorks to apply
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

# Function to perform a Bing search and filter results by domain
def bing_search(query, domain):
    url = f"https://www.bing.com/search?q={urllib.parse.quote_plus(query)}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        for h2 in soup.find_all('h2'):
            a = h2.find('a')
            if a and a.get('href') and domain in a['href']:
                links.append(a['href'])

        return links
    except Exception as e:
        return [f"[!] Request failed: {str(e)}"]

# Main function to perform all dorks
def perform_dorking(site):
    logs = []
    for dork in DORKS:
        query = dork.format(site=site)
        logs.append(f"[+] Dorking: {query}")
        results = bing_search(query, site)

        if not results:
            logs.append("[!] No valid links from target domain found.")
        else:
            for idx, link in enumerate(results, start=1):
                logs.append(f"[{idx}] {link}")
        logs.append("-" * 60)
    return logs
