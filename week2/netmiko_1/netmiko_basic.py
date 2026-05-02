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
full_op = ""
commands = ["show version", "show ip interface brief", "show running-config"]
for cmd in commands:
    output = connection.send_command(cmd)
    print(f"===== {cmd} =====")
    print(f"{output} \n")
    full_op+=f"===== {cmd} =====\n {output}\n\n"
connection.disconnect()
with open("device_output.txt","w") as f:
    f.write(full_op)
    