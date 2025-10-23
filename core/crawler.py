# core/crawler.py
import requests
import urllib3
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
from rich.console import Console


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def crawl_urls(base_url, max_depth=2):
    console = Console()
    visited = set()
    to_visit = [(base_url, 0)]
    endpoints = set()

    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    while to_visit:
        url, depth = to_visit.pop(0)
        if depth > max_depth or url in visited:
            continue
        visited.add(url)

        try:
            resp = requests.get(
                url,
                timeout=10,
                headers=headers,
                allow_redirects=True,
                verify=False  
            )
            endpoints.add(url)

            if depth < max_depth:
                soup = BeautifulSoup(resp.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(url, link['href'])
                    parsed = urlparse(full_url)
                    base_netloc = urlparse(base_url).netloc
                    if parsed.netloc == base_netloc and full_url not in visited:
                        to_visit.append((full_url, depth + 1))
        except:
            continue

    console.print(f"[green]✓[/green] Ditemukan {len(endpoints)} endpoint")
    return list(endpoints)
