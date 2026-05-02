import yaml

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

with open ("devices.yaml","r") as f:
    data = yaml.safe_load(f)

devices = data["devices"]
groups = {d["location"]: [] for d in devices}

for device in devices:    
    if validate_ip(device["ip"]) and device["status"]=="up":
            groups[device["location"]].append(device["hostname"])

for location,hostnames in groups.items():
    print(f"{location}: {hostnames}")

with open("groups.yaml","w") as f:
    yaml.dump(groups,f,default_flow_style = False)

