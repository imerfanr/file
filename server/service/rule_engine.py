def evaluate(miner):
    score = 0
    if "3333" in miner["open_ports"]: score += 2
    if miner.get("country") not in ["IR", "IRN"]: score += 1
    if miner.get("city") in ["ایلام", "تهران"]: score += 1
    return "high" if score > 2 else "medium" if score == 2 else "low"