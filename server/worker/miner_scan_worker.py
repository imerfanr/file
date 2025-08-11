import nmap
import requests
import sqlite3

PORTS = "4028,3333,4444,5555,4233,8233"
DB = "miners.db"

def scan(targets):
    nm = nmap.PortScanner()
    print(f"Start Nmap scan: {targets}")
    nm.scan(hosts=targets, ports=PORTS, arguments="-sT -Pn --open")
    conn = sqlite3.connect(DB)
    for host in nm.all_hosts():
        open_ports = []
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                open_ports.append(port)
        if open_ports:
            # GeoIP واقعی
            geo = requests.get(f"http://ip-api.com/json/{host}").json()
            conn.execute(
                "INSERT OR IGNORE INTO miners (ip, open_ports, lat, lon, city, country) VALUES (?, ?, ?, ?, ?, ?)",
                (host, ",".join(map(str, open_ports)), geo.get("lat"), geo.get("lon"), geo.get("city"), geo.get("countryCode")),
            )
    conn.commit()
    conn.close()
if __name__ == "__main__":
    scan("192.168.100.0/24")