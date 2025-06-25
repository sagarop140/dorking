import requests
from urllib.parse import urlparse, quote_plus
from bs4 import BeautifulSoup

# List of dorks to use
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

MOJEEK_SEARCH_URL = "https://www.mojeek.com/search?q="

def scrape_mojeek(query):
    """Send search query to Mojeek and return a list of URLs."""
    try:
        url = MOJEEK_SEARCH_URL + quote_plus(query)
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Mojeek search results URLs are in <a class="result__url" href="...">
        anchors = soup.find_all("a", class_="result__url")
        urls = []
        for a in anchors:
            href = a.get('href')
            if href:
                urls.append(href.strip())
        return urls
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return []

def filter_urls(urls, domain):
    """Filter URLs to keep those with domain or subdomains matching the target."""
    filtered = []
    for url in urls:
        parsed = urlparse(url)
        if domain in parsed.netloc.lower():
            filtered.append(url)
    return filtered

def perform_dorking(domain):
    print(f"Starting dorking for domain: {domain}\n")
    results_all = {}
    for dork in DORKS:
        print(f"[+] Dorking: {dork}")
        urls = scrape_mojeek(dork)
        filtered_urls = filter_urls(urls, domain)
        
        if not filtered_urls:
            print("[!] No valid links found for this dork.")
        else:
            for i, url in enumerate(filtered_urls, start=1):
                print(f"[{i}] {url}")
        
        print("-" * 60)
        results_all[dork] = filtered_urls
    return results_all

if __name__ == "__main__":
    target_domain = "nasa.gov"
    perform_dorking(target_domain)
