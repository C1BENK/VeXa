# utils/banner.py
from rich.console import Console
from rich.text import Text

def print_banner():
    console = Console()
    banner_text = """

██╗░░░██╗███████╗██╗░░██╗░█████╗░
██║░░░██║██╔════╝╚██╗██╔╝██╔══██╗
╚██╗░██╔╝█████╗░░░╚███╔╝░███████║
░╚████╔╝░██╔══╝░░░██╔██╗░██╔══██║
░░╚██╔╝░░███████╗██╔╝╚██╗██║░░██║
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝"""
    text = Text(banner_text, style="bold green")
    console.print(text, justify="center")
    console.print("[bold cyan]All-in-One Web Vulnerability Explorer[/bold cyan]\n", justify="center")
