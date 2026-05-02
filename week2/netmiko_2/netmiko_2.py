from netmiko import ConnectHandler
import json
from dotenv import load_dotenv
import os

load_dotenv()  # reads the .env file

device = {
    "device_type": "cisco_xr",
    "host":        os.getenv("DEVICE_HOST"),
    "username":    os.getenv("DEVICE_USERNAME"),
    "password":    os.getenv("DEVICE_PASSWORD"),
    "port":        int(os.getenv("DEVICE_PORT")),
}


connection = ConnectHandler(**device)
output = connection.send_command("show ip interface brief")

def parse_interfaces(output):
    lst = []

    for line in output.splitlines():
        if not line.strip() or "Interface" in line:
            continue
        parts = line.split()
        if len(parts)==5 and "." in parts[1]:
            lst.append({
            "interface" : parts[0],
            "ip" : parts[1],
            "status" : parts[2],
            "protocol" : parts[3]})
    
   # for network in lst:
   #     if network['status'] =="Up" and network['protocol']=="Up":
   #         print(f"{network['interface']} | {network['ip']} | {network['status']} | {network['protocol']}")
    with open("interfaces.json","w") as f:
        json.dump(lst,f,indent = 4)
    return lst
parse_interfaces(output)
connection.disconnect()

    