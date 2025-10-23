# core/scanner.py
from rich.console import Console
from .cms_detector import detect_cms
from .plugin_detector import detect_plugins
from .dir_scan import scan_directories
from .header_scan import check_security_headers
from .tech_detector import detect_technologies
from .crawler import crawl_urls
from .xss_scan import scan_xss_all
from .sqli_scan import scan_sqli_all
from .reporter import generate_report

def run_full_scan(base_url):
    console = Console()
    results = {
        "cms": None,
        "plugins": [],
        "dirs": [],
        "headers": [],
        "tech": "",
        "sqli": [],
        "xss": [],
        "is_static": True
    }

    # === 1. CRAWL RINGAN (1 level) ===
    console.print("[2/8] Menjalankan crawler ringan...", style="bold blue")
    crawled = crawl_urls(base_url, max_depth=1)

    # === 2. AMBIL HALAMAN BERPARAMETER ===
    param_endpoints = [url for url in crawled if "?" in url]

    # === 3. JIKA TIDAK ADA, BUAT PARAMETER UJI OTOMATIS ===
    if not param_endpoints:
        console.print("[yellow]ℹ️ Tidak ada parameter ditemukan — uji path umum...[/yellow]")
        base = base_url.rstrip('/')
        param_endpoints = [
            f"{base}/?s=test",
            f"{base}/?q=test",
            f"{base}/?id=1",
            f"{base}/?page_id=1",
            f"{base}/search/?s=test"
        ]
        results["is_static"] = False  # karena kita paksa uji
    else:
        results["is_static"] = False

    console.print(f"[green]✓[/green] Siap uji {len(param_endpoints)} endpoint berparameter")

    # === 4. JALANKAN SEMUA MODUL ===
    console.print("[3/8] Mendeteksi CMS...", style="bold blue")
    results["cms"] = detect_cms(base_url)

    console.print("[4/8] Mendeteksi plugin (jika WordPress)...", style="bold blue")
    results["plugins"] = detect_plugins(base_url, results["cms"])

    console.print("[5/8] Memindai direktori sensitif...", style="bold blue")
    results["dirs"] = scan_directories(base_url)

    console.print("[6/8] Memindai header keamanan...", style="bold blue")
    results["headers"] = check_security_headers(base_url)

    console.print("[7/8] Mendeteksi teknologi...", style="bold blue")
    results["tech"] = detect_technologies(base_url)

    console.print("[8/8] Menguji SQLi & XSS...", style="bold blue")
    results["sqli"] = scan_sqli_all(param_endpoints)
    results["xss"] = scan_xss_all(param_endpoints)

    generate_report(results)
