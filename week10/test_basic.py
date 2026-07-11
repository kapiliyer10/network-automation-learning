# Simple network data tests — no device connection needed

interfaces = {
    "GigabitEthernet1": {"status": "up", "protocol": "up", "ip": "10.10.20.48"},
    "GigabitEthernet2": {"status": "down", "protocol": "down", "ip": None},
    "Loopback0":        {"status": "up", "protocol": "up", "ip": "10.0.0.1"},
}

def test_gigabit1_is_up():
    assert interfaces["GigabitEthernet1"]["status"] == "up"

def test_loopback0_has_ip():
    assert interfaces["Loopback0"]["ip"] is not None

def test_at_least_one_up_interface():
    up_interfaces = [
        name for name, data in interfaces.items()
        if data["status"] == "up"
    ]
    assert len(up_interfaces) >= 1

def test_gigabit2_is_down():
    assert interfaces["GigabitEthernet2"]["status"] == "down"