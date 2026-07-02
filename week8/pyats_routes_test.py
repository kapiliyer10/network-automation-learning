from pyats import aetest
from pyats.topology import loader
#import json
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
    def test_gigbit1_is_up(self):
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
    def test_3_inf_exist(self):
        interfaces = self.parsed["interface"].keys()
        assert len(interfaces) >= 3, f"Less than 3 interfaces found: {interfaces}"
        print(f"[PASS] Found {len(interfaces)} interfaces: {interfaces}")
    
class CheckRoutes(aetest.Testcase):
    @aetest.setup
    def setup(self):
        device = self.parent.parameters["device"]
        self.parsed = device.parse("show ip route summary")

        #print(json.dumps(self.parsed, indent=2))
    @aetest.test
    def test_total_routes(self):
        routes = self.parsed["vrf"]["default"]["total_route_source"]["subnets"]
        assert routes > 0, "No routes found in the routing table"
        print(f"[PASS] Found {routes} routes in the routing table")
    
    @aetest.test
    def test_connected_routes_exist(self):
        connected_routes = self.parsed["vrf"]["default"]["route_source"]["connected"]["subnets"]
        assert connected_routes > 0, "No connected routes found in the routing table"
        print(f"[PASS] Found {connected_routes} connected routes: {connected_routes}")
    

class CheckVersion(aetest.Testcase):
    @aetest.setup
    def setup(self):
        device = self.parent.parameters["device"]
        self.parsed = device.parse("show version")

    @aetest.test
    def test_os_is_iosxe(self):
        os = self.parsed["version"]["os"]
        assert os == "IOS-XE", f"OS is {os}, expected IOS-XE"
        print(f"[PASS] OS is {os}")
    
    @aetest.test
    def test_version_is_17_12_2(self):
        version = self.parsed["version"]["version"]
        assert version == "17.12.2", f"Version is {version}, expected 17.12.2"
        print(f"[PASS] Version is {version}")

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self):
        self.parent.parameters["device"].disconnect()
        print("Disconnected from device")

if __name__ == "__main__":
    aetest.main()