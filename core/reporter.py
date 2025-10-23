# core/reporter.py
from rich.console import Console
from rich.table import Table

def generate_report(results):
    console = Console()
    console.print("\n[bold green][✅] LAPORAN AKHIR:[/bold green]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Komponen", style="dim", width=15)
    table.add_column("Temuan", width=50)

    table.add_row("CMS", results["cms"])
    
    plugins = "Tidak ada" if not results["plugins"] else "\n".join(results["plugins"])
    table.add_row("Plugin", plugins)
    
    dirs = "Tidak ada" if not results["dirs"] else "\n".join(results["dirs"])
    table.add_row("Direktori", dirs)
    
    headers = "Aman" if not results["headers"] else ", ".join(results["headers"])
    table.add_row("Header", headers)
    
    table.add_row("Teknologi", results["tech"])
    
    sqli = "Tidak ada" if not results["sqli"] else "\n".join(results["sqli"])
    table.add_row("SQLi", sqli)
    
    xss = "Tidak ada" if not results["xss"] else "\n".join(results["xss"])
    table.add_row("XSS", xss)

    if results["is_static"]:
        console.print("[yellow]ℹ️ Situs statis — risiko SQLi/XSS sangat rendah.[/yellow]")

    console.print(table)
