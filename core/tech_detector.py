# core/tech_detector.py
import requests
import urllib3
from rich.console import Console

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def detect_technologies(url):
    console = Console()
    headers_req = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        r = requests.get(url, timeout=10, headers=headers_req, verify=False)
        server = r.headers.get("Server", "Unknown")
        powered = r.headers.get("X-Powered-By", "Unknown")
        return f"{server} | {powered}"
    except:
        return "Gagal"
