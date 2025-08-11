import json

with open("iran_isp_ip_ranges.json", "r", encoding="utf-8") as f:
    data = json.load(f)

province = input("انتخاب استان: ")
city = input("انتخاب شهر: ")

isps = list(data[province][city].keys())
for idx, isp in enumerate(isps, 1):
    print(f"{idx}. {isp}")

chosen_isp = isps[int(input("ISP شماره: ")) - 1]
ip_ranges = data[province][city][chosen_isp]
for idx, rng in enumerate(ip_ranges, 1):
    print(f"{idx}. {rng}")

chosen_range = ip_ranges[int(input("IP Range شماره: ")) - 1]
print(f"رنج انتخاب شده: {chosen_range}")