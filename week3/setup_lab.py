import subprocess
import time
import yaml

LAB_FILE = "/home/owner/practice/week3/bgp-lab.yaml"
LAB_DIR  = "/home/owner/practice/week3"
INVENTORY_FILE = "/home/owner/practice/week3/inventory.yaml"

def setup_ssh(containers):
    print("Setting up SSH on containers...")
    for container in containers:
        subprocess.run(["sudo", "docker", "exec", container, "bash", "-c",
            "apk add openssh && mkdir -p /run/sshd && echo 'root:ansible' | chpasswd && "
            "ssh-keygen -A && echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config && "
            "echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && "
            "/usr/sbin/sshd"], capture_output=True)
        print(f"[OK] SSH setup on {container}")

def deploy_lab():
    print("Deploying lab...")
    subprocess.run(["sudo", "containerlab", "deploy", "-t", LAB_FILE], 
                   check=True
                   )
    print("Lab deployed successfully")

def get_containers(lab_name):
    result = subprocess.run(["docker", "ps", 
                            "--filter", f"label=containerlab={lab_name}",
                            "--format", "{{.Names}}"],
    capture_output=True,
    check=True,
    text=True)
    return result.stdout.strip().splitlines()

def configure_router(container, cfg):
    subprocess.run(["docker", "exec", container, "bash", 
                    "-c","sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons && "
                    "/usr/lib/frr/bgpd -d -F traditional -A 127.0.0.1"],
                        check=True
                       )
    time.sleep(3)

    subprocess.run(["docker", "exec", container, "bash","-c",
                        f"ip addr add {cfg['eth1_ip']} dev eth1 && ip addr add {cfg['loopback_ip']} dev lo"],
                        check=True
                       )   
                       
    time.sleep(1)

    subprocess.run(["docker", "exec", container, "vtysh",
                    "-c", "conf t",
                    "-c", "route-map ALLOW permit 10",
                    "-c", f"router bgp {cfg['asn']}",
                    "-c", f"bgp router-id {cfg['router_id']}",
                    "-c", f"neighbor {cfg['neighbor_ip']} remote-as {cfg['neighbor_asn']}",
                    "-c", "address-family ipv4 unicast",
                    "-c", f"network {cfg['network']}",
                    "-c", f"neighbor {cfg['neighbor_ip']} route-map ALLOW in",
                    "-c", f"neighbor {cfg['neighbor_ip']} route-map ALLOW out",
                    "-c", "exit-address-family",
                    "-c", "end"],
                       check=True
                       )
    print(f"[OK] {container} configured")

def verify_bgp(container):
    result = subprocess.run(["docker", "exec", container, "vtysh",
                            "-c", "show bgp summary"],
                            check=True,
                            capture_output=True,
                            text=True
                            )
    print(f"--- BGP Summary: {container} ---")
    print(result.stdout)

def main():
    with open(LAB_FILE) as f:
        topology = yaml.safe_load(f)
    with open(INVENTORY_FILE) as f:
        inventory = yaml.safe_load(f)

    deploy_lab()
    time.sleep(3)
    containers = get_containers(topology['name'])
    for container in containers:
        node_name = container.split("-")[-1]
        cfg = inventory[node_name]
        configure_router(container, cfg)
    setup_ssh(containers)   
    time.sleep(5)
    for container in containers:
        verify_bgp(container)

if __name__ == "__main__":
    main()

