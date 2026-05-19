from ncclient import manager
import xmltodict
import json
import ipaddress

conn = manager.connect(
    host="",
    port="",
    username="",
    password="",
    hostkey_verify=False
)

# Try Cisco native interface model
filter = """
<filter>
  <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
  <interface-configuration>
    <active>act</active>
  </interface-configuration>
  </interface-configurations>
</filter>
"""

response = conn.get_config(source="running", filter=filter)
data = xmltodict.parse(response.xml)
interfaces = data["rpc-reply"]["data"]["interface-configurations"]["interface-configuration"]

print(f"{'Interface':<30} {'IP Address':<20} {'Description'}")
print(f"{'---------':<30} {'----------':<20} {'-----------'}")
for intf in interfaces:
    name = intf.get('interface-name','N/A')
    desc = intf.get('description', 'N/A')
    ip_data = intf.get('ipv4-network',{})
    address = ip_data.get('addresses', {}).get('primary', {}).get('address', None)
    if address:
      netmask = ip_data.get('addresses', {}).get('primary', {}).get('netmask', None)
      prefix = ipaddress.IPv4Network(f"0.0.0.0/{netmask}").prefixlen
      print(f"{name:<30} {address+'/'+str(prefix):<20} {desc}")
    else:
       continue


with open("output.json", "w") as f:
    json.dump(data, f, indent=2)



#print(json.dumps(data, indent=2))

conn.close_session()