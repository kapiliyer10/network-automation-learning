from ncclient import manager
import xmltodict
from payload import build_loopback_payload

conn = manager.connect(
    host="",
    port="",
    username="",
    password="",
    hostkey_verify=False
)

config_payload = build_loopback_payload("Loopback50", "50.50.50.50","Created via NETCONF")

conn.edit_config(target="candidate", config=config_payload)
conn.commit()

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

for intf in interfaces:
    if intf["interface-name"] == "Loopback50":
        print(f"[SUCCESS] Loopback50 created with IP {intf['ipv4-network']['addresses']['primary']['address']}")
        break
else:
    print("[FAILED]")