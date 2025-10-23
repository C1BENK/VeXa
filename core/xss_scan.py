# core/xss_scan.py
import requests
import urllib3
from urllib.parse import urlparse
from rich.console import Console

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scan_xss_all(endpoints):
    console = Console()
    vulns = []
    
    # Jika tidak ada endpoint berparameter, skip
    if not endpoints:
        console.print("  ℹ️ Tidak ada endpoint berparameter — lewati XSS scan")
        return vulns

    try:
        with open("wordlists/xss.txt") as f:
            payloads = [line.strip() for line in f if line.strip()][:2]
    except:
        payloads = ['<script>alert(1)</script>']

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for url in endpoints[:20]:  # batasi
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        test_url = f"{base}?vexa_xss=test" if not parsed.query else url + "&vexa_xss=test"

        for payload in payloads:
            test = test_url.replace("test", payload)
            try:
                r = requests.get(test, timeout=5, headers=headers, verify=False)
                if payload in r.text:
                    vulns.append(url)
                    break
            except:
                continue

    return vulns
