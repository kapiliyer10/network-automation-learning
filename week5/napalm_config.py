from napalm import get_network_driver

driver = get_network_driver("iosxr_netconf")

device = driver(
    hostname="",
    username="",
    password="",
    optional_args={
        "port": 830,
    }
)

device.open()
device.load_merge_candidate(config="""
interface Loopback77
 description Added by Napalm
 ipv4 address 77.77.77.77 255.255.255.255
""")


diff = device.compare_config()
print("=====Config Diff=====")
if diff:
    device.commit_config()
    print(f"[COMMITTED] \n{diff}")
else:
    device.discard_config()
    print("[NOTHING TO CHANGE]")


intf_ips = device.get_interfaces_ip()

if "Loopback77" in intf_ips:
    print("\n=====Loopback77 IP Address=====")
    for intf, data in intf_ips["Loopback77"].items():
        for ip, details in data.items():
            print(f"Interface: Loopback77, IP Address: {ip}, Prefix Length: {details['prefix_length']}")
else:
    print("\nLoopback77 not found in interface IPs.")