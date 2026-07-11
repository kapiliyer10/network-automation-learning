import pytest
import requests

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://IP address/restconf/data"
AUTH = ("", "")
HEADERS = {
    "Accept":       "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Fixture — runs once, shared across all tests
@pytest.fixture(scope="module")
def interfaces():
    response = requests.get(
        f"{BASE_URL}/ietf-interfaces:interfaces",
        auth=AUTH,
        headers=HEADERS,
        verify=False
    )
    assert response.status_code == 200
    return response.json()["ietf-interfaces:interfaces"]["interface"]

# Tests use the fixture by name
def test_interface_count(interfaces):
    assert len(interfaces) >= 3
    print(f"\nFound {len(interfaces)} interfaces")

def test_gigabit1_enabled(interfaces):
    gi1 = next(i for i in interfaces if i["name"] == "GigabitEthernet1")
    assert gi1["enabled"] == True

def test_loopback0_has_ip(interfaces):
    lo0 = next(i for i in interfaces if i["name"] == "Loopback0")
    assert lo0.get("ietf-ip:ipv4", {}).get("address")
    ip = lo0["ietf-ip:ipv4"]["address"][0]["ip"]
    assert ip != ""
    print(f"\nLoopback0 IP: {ip}")

def test_management_interface_description(interfaces):
    gi1 = next(i for i in interfaces if i["name"] == "GigabitEthernet1")
    assert "description" in gi1
    print(f"\nDescription: {gi1['description']}")