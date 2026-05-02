from netmiko import ConnectHandler
from dotenv import load_dotenv
import os

load_dotenv()

device = {
    "device_type": "cisco_xr",
    "host":        os.getenv("DEVICE_HOST"),
    "username":    os.getenv("DEVICE_USERNAME"),
    "password":    os.getenv("DEVICE_PASSWORD"),
    "port":        int(os.getenv("DEVICE_PORT")),
}

connection = ConnectHandler(**device)

#config_commands = ["interface Loopback99",
#    "description Test by Python",
#    "ipv4 address 99.99.99.99 255.255.255.255",]

output = connection.send_config_set([
    "interface Loopback99",
    "description Test by Python",
    "ipv4 address 99.99.99.99 255.255.255.255",
    "commit",
], exit_config_mode=False)
connection.exit_config_mode()


output1 = connection.send_command("show ip interface brief")
print(output1)

if "Loopback99" in output1:
    print("[SUCCESS] Loopback99 created")
else:
    print("[FAILED] Loopback99 not found")

remove_commands = ["no interface Loopback99","commit",]

connection.send_config_set(remove_commands)

output = connection.send_command("show ip interface brief")
if "Loopback99" not in output:
    print("[SUCCESS] Loopback99 removed")   
else:
    print("[FAILED] Loopback99 still present")

connection.disconnect()