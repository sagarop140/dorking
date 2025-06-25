from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import time
import urllib.parse
import argparse

# Initialize colorama
init(autoreset=True)

# ASCII Art and Branding
def print_banner():
    print(f"{Fore.LIGHTRED_EX}"
          "  ____  ___   ___   ____ _     _____   ____   ___  ____  _  __\n"
          " / ___|/ _ \\ / _ \\ / ___| |   | ____| |  _ \\ / _ \\|  _ \\| |/ /\n"
          "| |  _| | | | | | | |  _| |   |  _|   | | | | | | | |_) | ' / \n"
          "| |_| | |_| | |_| | |_| | |___| |___  | |_| | |_| |  _ <| . \\ \n"
          " \\____|\\___/ \\___/ \\____|_____|_____| |____/ \\___/|_| \\_\\_|\\_\\\n"
          f"{Style.RESET_ALL}=======================================\n"
          f"{Fore.WHITE}TOOL BY - thexm0g{Style.RESET_ALL}")

# Dork list
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

# Initialize headless Firefox browser
def init_browser():
    options = FirefoxOptions()
    options.add_argument("--headless")
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver

# Perform DuckDuckGo search
def duckduckgo_search(driver, query):
    search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
    driver.get(search_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
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
    return results

# Save results to file
def save_results(results, filename):
    with open(filename, 'w') as file:
        for result in results:
            file.write(result + '\n')

# Main dorking function
def perform_dorking(site):
    print_banner()
    driver = init_browser()
    all_results = []

    for dork in DORKS:
        query = dork.format(site=site)
        print(f"{Fore.CYAN}Performing Dork: {Fore.YELLOW}{query}{Style.RESET_ALL}")
        results = duckduckgo_search(driver, query)
        all_results.extend(results)
        for result in results:
            print(f"{Fore.LIGHTBLUE_EX}{result}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-' * 80}{Style.RESET_ALL}")

    driver.quit()

    # Prompt to save
    save_option = input(f"{Fore.YELLOW}Save results to file? (y/n): {Style.RESET_ALL}").strip().lower()
    if save_option == 'y':
        filename = input(f"{Fore.YELLOW}Enter filename (e.g., results.txt): {Style.RESET_ALL}").strip()
        save_results(all_results, filename)
        print(f"{Fore.GREEN}Results saved to {filename}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Results not saved.{Style.RESET_ALL}")

# Entry point
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DuckDuckGo Dorking Tool")
    parser.add_argument('site', help="Target site domain (e.g., example.com)")
    args = parser.parse_args()
    perform_dorking(args.site)
    
driver.quit()
return all_results
