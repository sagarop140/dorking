import requests
from bs4 import BeautifulSoup
import urllib.parse

# User-Agent header to avoid bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Common dorks for testing vulnerabilities and sensitive data exposure
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

# Function to perform Bing search with BeautifulSoup
def bing_search(query, domain):
    url = f"https://www.bing.com/search?q={urllib.parse.quote_plus(query)}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        # Extract links from Bing results
        for h2 in soup.find_all('h2'):
            a = h2.find('a')
            if a and a.get('href'):
                href = a['href']
                if domain in href:
                    links.append(href)

        # Fallback if nothing found
        if not links:
            for li in soup.find_all('li', class_='b_algo'):
                a = li.find('a')
                if a and a.get('href'):
                    href = a['href']
                    if domain in href:
                        links.append(href)

        return links
    except Exception as e:
        return [f"[!] Request failed: {str(e)}"]

# Main function to run all dorks on the given site
def perform_dorking(site):
    all_results = []
    counter = 1

    for dork in DORKS:
        query = dork.format(site=site)
        print(f"[+] Dorking: {query}")
        results = bing_search(query, site)

        if results and not all("[!]" in r for r in results):
            for res in results:
                print(f"[{counter}] {res}")
                counter += 1
                all_results.append(res)
        else:
            print(f"[!] No valid links from target domain found.")

        print("-" * 60)

    return all_results
