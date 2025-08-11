import os
import json
import ipaddress
import sqlite3
import socket
import requests
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich import box

# ---------- کلیدهای واقعی API ----------
ABUSEIPDB_KEY = "کلید واقعی abuseipdb"
PROXYCHECK_KEY = "کلید واقعی proxycheck"
SHODAN_KEY = "کلید واقعی shodan"
IPINFO_KEY = "کلید واقعی ipinfo"

# ---------- ثابت‌ها ----------
IP_PORTS = [22, 3333, 3389, 4444, 5555, 7777, 8888, 9999, 18081, 18082, 18083, 3000, 4000, 5000]
DB_NAME = "kashif_cli.db"
console = Console()

# ---------- دیتابیس ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS scan_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        province TEXT,
        city TEXT,
        proxycheck TEXT,
        abuseipdb TEXT,
        shodan TEXT,
        ipinfo TEXT,
        open_ports TEXT,
        created TEXT
    )
    ''')
    conn.commit()
    conn.close()

def save_scan(ip, province, city, proxycheck, abuseipdb, shodan, ipinfo, open_ports):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    INSERT INTO scan_results (ip, province, city, proxycheck, abuseipdb, shodan, ipinfo, open_ports, created)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (ip, province, city, str(proxycheck), str(abuseipdb), str(shodan), str(ipinfo), ','.join(map(str, open_ports)), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_reports():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM scan_results ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

# ---------- استان و شهر ----------
def select_location():
    with open("iran_states_cities.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    provinces = list(data.keys())
    while True:
        console.print("\n[bold blue]📍 انتخاب استان:[/bold blue]")
        for idx, province in enumerate(provinces, 1):
            console.print(f"[cyan]{idx}[/cyan]. {province}")
        pidx = IntPrompt.ask("شماره استان", choices=[str(i) for i in range(1, len(provinces) + 1)])
        province = provinces[pidx - 1]
        cities = data[province]
        console.print(f"\n[bold green]🏙️ انتخاب شهر در استان {province}:[/bold green]")
        for idx, city in enumerate(cities, 1):
            console.print(f"[green]{idx}[/green]. {city}")
        cidx = IntPrompt.ask("شماره شهر", choices=[str(i) for i in range(1, len(cities) + 1)])
        city = cities[cidx - 1]
        return province, city

# ---------- دریافت رنج IP ----------
def get_ip_range(province, city):
    # در نسخه واقعی باید از دیتابیس‌های RIPE، APNIC یا دیتابیس ISP استفاده شود
    # به طور نمونه:
    if os.path.exists("target_location.json"):
        with open("target_location.json", encoding="utf-8") as f:
            db = json.load(f)
            if db["province"] == province and db["city"] == city:
                return db["ip_range"]
    # نمونه تستی برای ادامه کار:
    ip_range = "192.168.100.0/29" # بجای این، رنج واقعی را قرار دهید
    with open("target_location.json", "w", encoding="utf-8") as f:
        json.dump({"province": province, "city": city, "ip_range": ip_range}, f, ensure_ascii=False, indent=2)
    return ip_range

# ---------- اسکن پورت‌ها ----------
def scan_ports(ip):
    open_ports = []
    for port in IP_PORTS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
        except:
            pass
    return open_ports

# ---------- APIهای تحلیل ----------
def call_proxycheck(ip):
    url = f"https://proxycheck.io/v2/{ip}?key={PROXYCHECK_KEY}&vpn=1&asn=1"
    try:
        res = requests.get(url, timeout=5).json()
        return res
    except:
        return None

def call_abuseipdb(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": "90"}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=5).json()
        return res
    except:
        return None

def call_shodan(ip):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_KEY}"
    try:
        res = requests.get(url, timeout=5).json()
        return res
    except:
        return None

def call_ipinfo(ip):
    url = f"https://ipinfo.io/{ip}?token={IPINFO_KEY}"
    try:
        res = requests.get(url, timeout=5).json()
        return res
    except:
        return None

def is_suspect(ip, proxycheck_res, abuseipdb_res):
    if not proxycheck_res or not abuseipdb_res:
        return False
    proxy = proxycheck_res.get(ip, {}).get("proxy", "no") if ip in proxycheck_res else "no"
    abuse_score = abuseipdb_res.get("data", {}).get("abuseConfidenceScore", 0)
    return proxy == "yes" or abuse_score > 50

# ---------- اسکن رنج IP ----------
def scan_ip_range(ip_range, province, city):
    net = ipaddress.IPv4Network(ip_range, strict=False)
    for ip in net.hosts():
        ip = str(ip)
        console.print(f"\n[bold yellow]🔎 در حال بررسی {ip}...[/bold yellow]")
        proxycheck_res = call_proxycheck(ip)
        abuseipdb_res = call_abuseipdb(ip)
        shodan_res = call_shodan(ip)
        ipinfo_res = call_ipinfo(ip)
        open_ports = []
        if is_suspect(ip, proxycheck_res, abuseipdb_res):
            console.print(f"[red]⚠️ {ip} مشکوک به ماینینگ، بررسی پورت‌ها...[/red]")
            open_ports = scan_ports(ip)
            if open_ports:
                console.print(f"[green]پورت‌های باز:[/green] {open_ports}")
            else:
                console.print("[cyan]هیچ پورت ماینری باز نیست[/cyan]")
        else:
            console.print("[grey]IP مشکوک نیست.[/grey]")
        save_scan(ip, province, city, proxycheck_res, abuseipdb_res, shodan_res, ipinfo_res, open_ports)
        time.sleep(1)

# ---------- نمایش گزارش ----------
def show_reports():
    reports = get_reports()
    table = Table(show_header=True, header_style="bold magenta", box=box.SQUARE)
    table.add_column("ID", style="dim", width=4)
    table.add_column("IP", style="bold green")
    table.add_column("استان")
    table.add_column("شهر")
    table.add_column("پورت‌های باز")
    table.add_column("تاریخ")

    for row in reports[:20]: # فقط ۲۰ تا آخر
        table.add_row(str(row[0]), row[1], row[2], row[3], row[8], row[9][:19])
    console.print(table)

# ---------- منوی اصلی ----------
def main_menu():
    while True:
        console.print(Panel.fit("[bold blue]سیستم کاشف شبح حبشی[/bold blue]\n[cyan]1.[/] انتخاب استان و شهر\n[cyan]2.[/] اسکن رنج IP\n[cyan]3.[/] نمایش گزارش‌ها\n[cyan]0.[/] خروج", title="منو", subtitle="کلید را وارد کنید"))
        choice = Prompt.ask("انتخاب", choices=["1", "2", "3", "0"])
        if choice == "1":
            province, city = select_location()
            ip_range = get_ip_range(province, city)
            console.print(f"[green]استان:[/green] {province}  [yellow]شهر:[/yellow] {city}  [magenta]رنج IP:[/magenta] {ip_range}")
        elif choice == "2":
            if not os.path.exists("target_location.json"):
                console.print("[red]لطفا ابتدا استان و شهر را انتخاب کنید![/red]")
                continue
            with open("target_location.json", encoding="utf-8") as f:
                db = json.load(f)
                province, city, ip_range = db["province"], db["city"], db["ip_range"]
            scan_ip_range(ip_range, province, city)
        elif choice == "3":
            show_reports()
        elif choice == "0":
            console.print("[cyan]خروج از برنامه.[/cyan]")
            break

if __name__ == "__main__":
    init_db()
    main_menu()