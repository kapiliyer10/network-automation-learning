from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result

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
print_result(result)