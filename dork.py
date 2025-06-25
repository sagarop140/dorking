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
    'site:{site} inurl:storemanager/contents/item.php?page_code=',
]

def bing_search(query):
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for li in soup.select('li.b_algo h2 a'):
            link = li.get('href')
            if link and link.startswith("http"):
                results.append(link)
        return results
    except Exception as e:
        return [f"[!] Request failed: {e}"]

def perform_dorking(site):
    output_lines = []

    for dork in DORKS:
        query = dork.format(site=site)
        output_lines.append(f"[+] Dorking: {query}")
        links = bing_search(query)

        # Filter only valid links containing site
        filtered_links = [l for l in links if site in l]

        if not filtered_links:
            output_lines.append("[!] No valid links from target domain found.")
        else:
            for i, link in enumerate(filtered_links, start=1):
                output_lines.append(f"[{i}] {link}")
        output_lines.append("-" * 60)

    return output_lines
