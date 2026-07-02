from pyats import aetest
from pyats.topology import loader

# Load testbed globally
testbed = loader.load("testbed.yaml")

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_to_devices(self):
        self.parent.parameters["device"] = testbed.devices["cat8000v"]
        self.parent.parameters["device"].connect()
        print("Connected to device")

class CheckInterfaces(aetest.Testcase):

    @aetest.setup
    def setup(self):
        device = self.parent.parameters["device"]
        self.parsed = device.parse("show ip interface brief")

    @aetest.test
    def test_gigabit1_is_up(self):
        status = self.parsed["interface"]["GigabitEthernet1"]["status"]
        protocol = self.parsed["interface"]["GigabitEthernet1"]["protocol"]
        assert status == "up", f"GigabitEthernet1 status is {status}, expected up"
        assert protocol == "up", f"GigabitEthernet1 protocol is {protocol}, expected up"
        print(f"[PASS] GigabitEthernet1 is up/up")

    @aetest.test
    def test_loopback0_has_ip(self):
        ip = self.parsed["interface"]["Loopback0"]["ip_address"]
        assert ip != "unassigned", f"Loopback0 has no IP assigned"
        print(f"[PASS] Loopback0 has IP: {ip}")

    @aetest.test
    def test_no_down_interfaces(self):
        down_intfs = []
        for intf, data in self.parsed["interface"].items():
            if data["status"] == "down" and data["protocol"] == "down":
                down_intfs.append(intf)
        assert len(down_intfs) == 0, f"Down interfaces found: {down_intfs}"
        print("[PASS] No down interfaces")

    @aetest.test
    def test_gigabit2_is_up(self):
        status = self.parsed["interface"]["GigabitEthernet2"]["status"]
        assert status == "up", f"GigabitEthernet2 status is {status}, expected up"
        print(f"[PASS] GigabitEthernet2 is up")

class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self):
        self.parent.parameters["device"].disconnect()
        print("Disconnected from device")

if __name__ == "__main__":
    aetest.main()