import subprocess

def run_command(container,command):
    result = subprocess.run(
        ["docker", "exec", container,"vtysh", "-c", command],
        capture_output=True,
        text=True
    )
    if "%" in result.stdout:
        print(f"[WARNING] {result.stdout.strip()}")
    else:
        print(result.stdout)

containers = ["clab-bgp-lab-router1", "clab-bgp-lab-router2"]
commands = ["show bgp summary", "show ip route bgp", "show interface brief"]
for container in containers:
    for command in commands:
        print(f"===== {container} | {command} =====")
        run_command(container, command)