import subprocess

def get_containers(lab_name):
    result = subprocess.run(
        ["docker", "ps", "--filter", f"label=containerlab={lab_name}",
         "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().splitlines()

def run_command(container, command):
    result = subprocess.run(
        ["docker", "exec", container, "vtysh", "-c", command],
        capture_output=True,
        text=True
    )
    if "%" in result.stdout:
        print(f"[WARNING] {result.stdout.strip()}")
    else:
        print(result.stdout)

containers = get_containers("bgp-lab")
commands = ["show bgp summary", "show ip route bgp", "show interface brief"]

for container in containers:
    for command in commands:
        print(f"===== {container} | {command} =====")
        run_command(container, command)