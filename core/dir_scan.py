# core/dir_scan.py
import requests
import urllib3
from rich.console import Console

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scan_directories(base_url):
    console = Console()
    found = []
    with open("wordlists/dirs.txt") as f:
        paths = [line.strip() for line in f if line.strip()]

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for path in paths:
        url = f"{base_url.rstrip('/')}/{path}"
        try:
            r = requests.get(url, timeout=5, headers=headers, verify=False)
            if r.status_code in [200, 301, 302, 403]:
                status = str(r.status_code)
                if path in [".env", ".git", "backup.zip", "database.sql"]:
                    found.append(f"⚠️ {path} ({status}) → File sensitif ADA!")
                else:
                    found.append(f"{path} ({status})")
        except:
            continue

    return found
