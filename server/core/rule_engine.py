def evaluate_risk(miner):
    # Rule sample: اگر پورت 3333 باز، امتیاز شادان بالا و geoip مشکوک → ریسک بالا
    score = 0
    if 3333 in miner["open_ports"]: score += 3
    if miner.get("abuseipdb_score", 0) > 50: score += 2
    if miner.get("country") not in ("IR", "IRN"): score += 1
    return score