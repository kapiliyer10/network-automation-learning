from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

print("--- Running hostname command ---")
result = nr.run(
    task=netmiko_send_command,
    command_string="hostname"
)
print_result(result)

print("--- Running ip addr show ---")
result = nr.run(
    task=netmiko_send_command,
    command_string="ip addr show eth1"
)
print_result(result)