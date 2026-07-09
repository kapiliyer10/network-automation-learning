import requests
import json

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://ip address of your RESTCONF server/restconf/data"
AUTH = ("user", "password")
HEADERS = {
    "Accept":       "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# PATCH — update description only
print("=== PATCH — updating description ===")
patch_payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback200",
        "description": "Updated by Python RESTCONF"
    }
}

response = requests.patch(
    f"{BASE_URL}/ietf-interfaces:interfaces/interface=Loopback200",
    auth=AUTH,
    headers=HEADERS,
    verify=False,
    json=patch_payload
)
print(f"Status code: {response.status_code}")
if response.status_code in [200, 201, 204]:
    print("[SUCCESS] Description updated")
else:
    print(f"[FAILED] {response.text}")

# Verify PATCH
response = requests.get(
    f"{BASE_URL}/ietf-interfaces:interfaces/interface=Loopback200",
    auth=AUTH,
    headers=HEADERS,
    verify=False
)
data = response.json()["ietf-interfaces:interface"][0]
print(f"New description: {data['description']}")

# DELETE — remove Loopback200
print("\n=== DELETE — removing Loopback200 ===")
response = requests.delete(
    f"{BASE_URL}/ietf-interfaces:interfaces/interface=Loopback200",
    auth=AUTH,
    headers=HEADERS,
    verify=False
)
print(f"Status code: {response.status_code}")
if response.status_code in [200, 201, 204]:
    print("[SUCCESS] Loopback200 deleted")
else:
    print(f"[FAILED] {response.text}")

# Verify DELETE
response = requests.get(
    f"{BASE_URL}/ietf-interfaces:interfaces/interface=Loopback200",
    auth=AUTH,
    headers=HEADERS,
    verify=False
)
print(f"Verification status: {response.status_code}")
if response.status_code == 404:
    print("[CONFIRMED] Loopback200 no longer exists")