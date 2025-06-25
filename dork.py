import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote_plus

DORKS = [
    "site:nasa.gov inurl:admin",
    "site:nasa.gov inurl:login",
    "site:nasa.gov inurl:wp-admin",
    'site:github.com nasa.gov "DB_PASSWORD="',
    'site:github.com nasa.gov "heroku_api_key"',
    "site:nasa.gov inurl:view_items.php?id=",
    "site:nasa.gov inurl:home.php?cat=",
    "site:nasa.gov inurl:item_book.php?CAT=",
    "site:nasa.gov inurl:prev_results.php?prodID=",
    "site:nasa.gov inurl:storemanager/contents/item.php?page_code="
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

BING_SEARCH_URL = "https://www.bing.com/search?q="

def bing_search(query):
    try:
        url = BING_SEARCH_URL + quote_plus(query)
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for item in soup.find_all('li', class_='b_algo'):
            h2 = item.find('h2')
            if h2 and h2.a:
                link = h2.a['href']
                results.append(link)
        return results
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return []

def filter_urls(urls, base_domain):
    filtered = []
    base_domain = base_domain.lower()
    for url in urls:
        parsed = urlparse(url)
        hostname = parsed.netloc.lower()
        if hostname == base_domain or hostname.endswith('.' + base_domain):
            filtered.append(url)
    return filtered

def get_subdomain(url):
    parsed = urlparse(url)
    return parsed.netloc.lower()

def perform_dorking(base_domain):
    print(f"Starting dorking for domain: {base_domain}\n")
    for dork in DORKS:
        print(f"[+] Dorking: {dork}")
        urls = bing_search(dork)
        filtered = filter_urls(urls, base_domain)
        if not filtered:
            print("[!] No valid links found for this dork.")
        else:
            for i, link in enumerate(filtered, 1):
                subdomain = get_subdomain(link)
                print(f"[{i}] ({subdomain}) {link}")
        print("-" * 60)

if __name__ == "__main__":
    target_domain = "nasa.gov"
    perform_dorking(target_domain)
