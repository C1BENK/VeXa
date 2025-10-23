# core/header_scan.py
import requests
import urllib3
from rich.console import Console

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_security_headers(url):
    console = Console()
    missing = []
    headers_req = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        r = requests.get(url, timeout=10, headers=headers_req, verify=False)
        h = r.headers

        if "Content-Security-Policy" not in h:
            missing.append("CSP")
        if "X-Frame-Options" not in h:
            missing.append("X-Frame-Options")
        if url.startswith("https") and "Strict-Transport-Security" not in h:
            missing.append("HSTS")
        if "X-Content-Type-Options" not in h:
            missing.append("X-Content-Type-Options")

        status = "Aman" if not missing else ", ".join(missing)
        console.print(f"[green]✓[/green] Header: {status}")
        return missing
    except Exception as e:
        console.print("[yellow]⚠ Gagal scan header[/yellow]")
        return ["Gagal"]
