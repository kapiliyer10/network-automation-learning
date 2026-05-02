import json
def validate_ip(ip):
    try:
            dev = ip.split(".")
            if len(dev)!=4:
                return False
            for val in dev:
                if int(val)>255 or int(val)<0:
                    return False
            return True
    except ValueError:
        return False
with open("devices.json","r") as f:
    data = json.load(f)
    
up_count = 0
down_count = 0
valid_count = 0
report =  []

for line in data:
    is_valid = validate_ip(line["ip"])
    if is_valid:
        valid_count+=1
    if line["status"]=="up":
        up_count+=1   
    else:
        down_count+=1
    report.append({
        "hostname":line["hostname"],
        "ip":line["ip"],
        "status":line["status"],
        "ip_valid":is_valid
        })

with open ("report.json","w") as f:
    json.dump(report,f, indent = 4)

print(f"Total devices: {len(data)}")
print(f"Valid IPs: {valid_count}")
print(f"Online (up): {up_count}")
print(f"Online (down): {down_count}")
