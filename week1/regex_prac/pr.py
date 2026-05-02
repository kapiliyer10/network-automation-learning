import re
import json

devices = []

with open("syslog.txt", "r") as f:
    for line in f:
        link = line.strip()

        timestamp = re.search(r"[A-Za-z]+ \d+ \d+:\d+:\d+", link)
        device    = link.split()[3]
        inf       = re.search(r"[A-Za-z]+\d+/\d+", link)
        state     = re.search(r"changed state to (\w+)", link)

        dev_dict = {
            "timestamp": timestamp.group() if timestamp else None,
            "device":    device,
            "interface": inf.group() if inf else None,
            "state":     state.group(1) if state else None
        }
        devices.append(dev_dict)

# Print only "down" state changes
print("--- State changed to DOWN ---")
for d in devices:
    if d["state"] == "down":
        print(f"{d['timestamp']} | {d['device']} | {d['interface']} | {d['state']}")

# Write all results to JSON
with open("parsed_syslog.json", "w") as f:
    json.dump(devices, f, indent=4)

print("\nResults written to parsed_syslog.json")
