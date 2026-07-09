import requests
import json

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://ip address of your DNA Center"
AUTH = ("user", "password")
HEADERS = {"Content-Type": "application/json"}

def get_token():
    response = requests.post(
        f"{BASE_URL}/dna/system/api/v1/auth/token",
        auth=AUTH,
        headers=HEADERS,
        verify=False
    )
    return response.json()["Token"]

def get_devices(token):
    headers = {"Content-Type": "application/json", "x-auth-token": token}
    response = requests.get(
        f"{BASE_URL}/dna/intent/api/v1/network-device",
        headers=headers,
        verify=False
    )
    return response.json()["response"]

def get_device_interfaces(token, device_id):
    headers = {"Content-Type": "application/json", "x-auth-token": token}
    response = requests.get(
        f"{BASE_URL}/dna/intent/api/v1/interface/network-device/{device_id}",
        headers=headers,
        verify=False
    )
    return response.json()["response"]

# Main
token = get_token()
devices = get_devices(token)

# Get details for first device
device = devices[0]
print(f"=== Device: {device['hostname']} ===")
print(f"IP:       {device['managementIpAddress']}")
print(f"Type:     {device['type']}")
print(f"Software: {device['softwareVersion']}")
print(f"Serial:   {device['serialNumber']}")
print(f"Status:   {device['reachabilityStatus']}")

# Get interfaces
print(f"\n=== Interfaces on {device['hostname']} ===")
interfaces = get_device_interfaces(token, device["id"])
print(f"{'Interface':<30} {'Status':<10} {'IP Address'}")
print(f"{'---------':<30} {'------':<10} {'----------'}")
for intf in interfaces:
    name = intf.get("portName", "N/A")
    status = intf.get("status", "N/A")
    ip = intf.get("ipv4Address", "N/A") or "N/A"
    print(f"{name:<30} {status:<10} {ip}")