from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.task import Task, Result
import re

def get_network_info(task: Task) -> Result:
    # Run multiple commands in one task
    hostname = task.run(
        task=netmiko_send_command,
        command_string="hostname"
    )
    interfaces = task.run(
        task=netmiko_send_command,
        command_string="ip addr show"
    )
    bgp = task.run(
        task=netmiko_send_command,
        command_string='vtysh -c "show bgp summary"'
    )
    return Result(
        host=task.host,
        result={
            "hostname":   hostname.result,
            "interfaces": interfaces.result,
            "bgp":        bgp.result
        }
    )

nr = InitNornir(config_file="config.yaml")
result = nr.run(task=get_network_info)

for host, host_result in result.items():
    data = host_result[0].result
    hostname = data["hostname"]
    bgp = data["bgp"]
    interfaces = data["interfaces"]
    print(f"====={hostname}=====")
    print(f"Hostname: {hostname}")
    # Check if any peer has a numeric PfxRcd (means Established):
    bgp_established = False
    for line in bgp.strip().splitlines():
        if re.search(r"\d+\.\d+\.\d+\.\d+\s+\d+\s+\d+\s+\d+\s+\d+", line):
            bgp_established = True
            count = re.search(r"Peers (\d)", bgp)
            peers = count.group(1) if count else "?"
            print(f"Established ({peers} peer/peers)")
            break
    else:
        print("BGP Down or no peers")
    name_list = []
    for line in interfaces.strip().splitlines():
        names = re.search(r"\d+: ([\w\d]+):", line) or re.search(r"\d+: ([\w\d]+)@", line)
        if names:
            name_list.append(names.group(1))
    print(f"Interfaces:{name_list}\n")
    