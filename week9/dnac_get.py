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
    headers = {
        "Content-Type": "application/json",
        "x-auth-token": token
    }
    response = requests.get(
        f"{BASE_URL}/dna/intent/api/v1/network-device",
        headers=headers,
        verify=False
    )
    return response.json()

# Get token first
token = get_token()
print(f"Token received: {token[:20]}...")

# Get all network devices
data = get_devices(token)
devices = data["response"]

print(f"\nFound {len(devices)} devices:\n")
print(f"{'Hostname':<25} {'Type':<20} {'IP Address':<15} {'Software'}")
print(f"{'---------':<25} {'----':<20} {'----------':<15} {'--------'}")
for device in devices:
    print(f"{device['hostname']:<25} {device['type']:<20} {device['managementIpAddress']:<15} {device['softwareVersion']}")