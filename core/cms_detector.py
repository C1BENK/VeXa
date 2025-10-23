# core/cms_detector.py
import requests
import urllib3
from rich.console import Console

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def detect_cms(url):
    base = url.rstrip("/")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # WordPress
    wp_paths = ["/wp-login.php", "/wp-admin/", "/readme.html"]
    for path in wp_paths:
        try:
            r = requests.get(f"{base}{path}", timeout=5, headers=headers, verify=False)
            if r.status_code == 200 and ("wordpress" in r.text.lower() or "wp-login" in r.url):
                return "WordPress"
        except:
            continue

    # Joomla
    try:
        r = requests.get(f"{base}/administrator/", timeout=5, headers=headers, verify=False)
        if r.status_code == 200 and "joomla" in r.text.lower():
            return "Joomla"
    except:
        pass

    # Laravel
    try:
        r = requests.get(base, timeout=10, headers=headers, verify=False)
        if "laravel" in r.headers.get("X-Powered-By", "").lower() or "laravel_session" in str(r.cookies):
            return "Laravel"
    except:
        pass

    return "Tidak terdeteksi"
