from netmiko_2 import parse_interfaces
from netmiko import ConnectHandler
import yaml
import json
from dotenv import load_dotenv
import os

load_dotenv()

with open("devices.yaml","r") as f:
    data = yaml.safe_load(f)

devices = data["devices"]
report = []

for device in devices:
    hostname = device["hostname"]  
    netmiko_device = {
        "device_type": device["device_type"],
        "host":        device["host"],
        "username":    device["username"],
        "password":    device["password"],
        "port":        device["port"],
    }

    try:
        connection = ConnectHandler(**netmiko_device)
        output = connection.send_command("show ip interface brief")
        interfaces = parse_interfaces(output)
        connection.disconnect()
        
        print(f"--- {hostname} ---")
        for intf in interfaces:
            if intf["status"] == "Up" and intf["protocol"] == "Up":
                print(f"{intf['interface']} | {intf['ip']} | {intf['status']} | {intf['protocol']}")

        
        report.append({
            "hostname":   hostname,
            "interfaces": interfaces
        })
    except Exception as e:
        print(f"[ERROR] Failed to connect to {hostname}: {e}")
        report.append({
            "hostname":   hostname,
            "interfaces": [],
            "error":      str(e)
        })
with open("network_report.json", "w") as f:
    json.dump(report, f, indent=4)

print("\nReport written to network_report.json")

