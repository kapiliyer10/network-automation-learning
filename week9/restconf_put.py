import requests
import json

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://ip address of your RESTCONF server/restconf/data"
AUTH = ("user", "password")
HEADERS = {
    "Accept":       "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Create Loopback200
payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback200",
        "description": "Created by Python RESTCONF",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "200.200.200.200",
                    "netmask": "255.255.255.255"
                }
            ]
        }
    }
}

# PUT to specific interface URL
response = requests.put(
    f"{BASE_URL}/ietf-interfaces:interfaces/interface=Loopback200",
    auth=AUTH,
    headers=HEADERS,
    verify=False,
    json=payload
)

print(f"Status code: {response.status_code}")
if response.status_code in [200, 201, 204]:
    print("[SUCCESS] Loopback200 created")
else:
    print(f"[FAILED] {response.text}")

# Verify by GET
response = requests.get(
    f"{BASE_URL}/ietf-interfaces:interfaces/interface=Loopback200",
    auth=AUTH,
    headers=HEADERS,
    verify=False
)
print(f"\nVerification status: {response.status_code}")
print(json.dumps(response.json(), indent=2))