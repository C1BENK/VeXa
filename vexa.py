# vexa.py
from utils.banner import print_banner
from utils.input_handler import get_valid_url
from core.scanner import run_full_scan

def main():
    print_banner()
    print("dev:   Wh04miXx")
    print("github: https://github.com/C1BENK/VeXa")
    print("tele:  t.me/Wh04am")
    print("info:  VeXa tools are tools that allow users to find out vulnerabilities on a website with just one click.\n")
    
    url = get_valid_url()
    print(f"\n[+] Target: {url}")
    print("[*] Memulai pemindaian otomatis...\n")
    
    run_full_scan(url)

if __name__ == "__main__":
    main()
