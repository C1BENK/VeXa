# utils/input_handler.py
from urllib.parse import urlparse
from rich.console import Console

def get_valid_url():
    console = Console()
    while True:
        url = console.input("[bold yellow][+][/bold yellow] Masukan url: ").strip()
        if not url:
            console.print("[red]❌ URL tidak boleh kosong![/red]")
            continue
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        try:
            result = urlparse(url)
            if result.scheme and result.netloc:
                return url
            else:
                console.print("[red]❌ Format URL tidak valid![/red]")
        except:
            console.print("[red]❌ URL tidak valid![/red]")
