import nmap
import requests
import sqlite3

PORTS = "3333,4444,5555,7777,8888,18081,18082,18083,4028,4233,8233"
DB = "miners.db"

def scan(targets):
    nm = nmap.PortScanner()
    nm.scan(hosts=targets, ports=PORTS, arguments="-sT -Pn --open")
    conn = sqlite3.connect(DB)
    for host in nm.all_hosts():
        open_ports = []
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                open_ports.append(port)
        if open_ports:
            geo = requests.get(f"http://ip-api.com/json/{host}").json()
            conn.execute(
                "INSERT OR IGNORE INTO miners (ip, open_ports, lat, lon, city, country) VALUES (?, ?, ?, ?, ?, ?)",
                (host, ",".join(map(str, open_ports)), geo.get("lat"), geo.get("lon"), geo.get("city"), geo.get("countryCode")),
            )
    conn.commit()
    conn.close()