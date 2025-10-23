# core/plugin_detector.py
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def detect_plugins(url, cms):
    if cms != "WordPress":
        return []
    
    base = url.rstrip("/")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    plugins = []
    
    common_plugins = {
        "contact-form-7": "contact-form-7",
        "elementor": "elementor",
        "woocommerce": "woocommerce"
    }
    
    for name, path in common_plugins.items():
        try:
            r = requests.get(f"{base}/wp-content/plugins/{path}/readme.txt", timeout=5, headers=headers, verify=False)
            if r.status_code == 200:
                # Ambil versi
                for line in r.text.split("\n"):
                    if line.startswith("Stable tag:"):
                        version = line.split(":")[1].strip()
                        # Cek rentan (contoh sederhana)
                        if name == "contact-form-7" and version < "5.3":
                            plugins.append(f"{name} v{version} (⚠️ Rentan)")
                        else:
                            plugins.append(f"{name} v{version}")
                        break
        except:
            continue
    
    return plugins
