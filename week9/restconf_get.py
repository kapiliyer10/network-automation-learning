import requests
import json

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://ip address of your RESTCONF server/restconf/data"
AUTH = ("user", "password")
HEADERS = {
    "Accept":       "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

def get_interfaces():
    response = requests.get(
        f"{BASE_URL}/ietf-interfaces:interfaces",
        auth=AUTH,
        headers=HEADERS,
        verify=False
    )
    print(f"Status code: {response.status_code}")
    return response.json()

data = get_interfaces()
interfaces = data["ietf-interfaces:interfaces"]["interface"]

print(f"\n{'Interface':<25} {'Enabled':<10} {'IP Address'}")
print(f"{'---------':<25} {'-------':<10} {'----------'}")
for intf in interfaces:
    name = intf["name"]
    enabled = intf["enabled"]
    ip = "N/A"
    if intf.get("ietf-ip:ipv4", {}).get("address"):
        ip = intf["ietf-ip:ipv4"]["address"][0]["ip"]
    print(f"{name:<25} {str(enabled):<10} {ip}")
