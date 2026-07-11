import pytest
import requests

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://IP address/restconf/data"
AUTH = ("", "")
HEADERS = {
    "Accept":       "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

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

@pytest.mark.parametrize("interface,expected_status", [
    ("GigabitEthernet1", True),
    ("GigabitEthernet2", False),
    ("Loopback0",        True),
])
def test_interface_enabled(interfaces, interface, expected_status):
    intf = next(i for i in interfaces if i["name"] == interface)
    assert intf["enabled"] == expected_status

@pytest.mark.skip(reason="sandbox not available")
def test_something():
    assert True  # never runs

@pytest.mark.xfail(reason="GigabitEthernet2 is admin down, not up")
def test_gigabit2_should_be_up(interfaces):
    intf = next(i for i in interfaces if i["name"] == "GigabitEthernet2")
    assert intf["enabled"] == True  # will fail → XFAIL
    