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
facts = device.get_facts()
intfs    = device.get_interfaces()
intf_ips = device.get_interfaces_ip()
bgp      = device.get_bgp_neighbors()

print("=====Facts=====")
print(f"{'Hostname':<30} : {facts['hostname']}")
print(f"{'Vendor':<30} : {facts['vendor']}")
print(f"{'UpTime':<30} : {facts['uptime']} seconds \n")

print("=====Interfaces=====")
print(f"{'Interface':<30} {'Status':<10} {'Speed':<12} {'MAC Address':<20}")
val_list = list(intfs.values())
intf = list(intfs.keys())

for i,j in intfs.items():
    status = "Up" if j.get('is_up') else "Down"
    speed = int(j.get('speed', 'N/A'))
    mac = j.get('mac_address') or "N/A"
    if mac == "":
        mac = "N/A"
    print(f"{i:<30} {status:<10} {speed:<12} {mac:<20}")

print("\n=====Interface IPs=====")
print(f"{'Interface':<30} {'IP Address':<20} {'Prefix Length'}")
for i,j in intf_ips.items():
    for k,v in j.items():
        for l,m in v.items():
            print(f"{i:<30} {l:<20} /{m['prefix_length']}")

print("\n=====BGP Neighbors=====")
print(f"{'Neighbor':<30} {'Local AS':<10} {'Remote AS':<10} {'State':<10} {'Uptime'}")
for peer,data in bgp['global']['peers'].items():
    local_as = data.get('local_as', 'N/A')
    remote_as = data.get('remote_as', 'N/A')
    state = data.get('is_up', False)
    state_str = "Up" if state else "Down"
    uptime = data.get('uptime', 'N/A')
    print(f"{peer:<30} {local_as:<10} {remote_as:<10} {state_str:<10} {uptime}")

device.close()