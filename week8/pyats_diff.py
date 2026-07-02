from pyats.topology import loader
from genie.utils.diff import Diff

testbed = loader.load("testbed.yaml")
device = testbed.devices["cat8000v"]
device.connect()

# Learn BEFORE
print("Learning state BEFORE...")
before = device.learn("interface")

# Make change
print("Making config change...")
device.configure("""
interface Loopback99
 description Added by pyATS test
 ip address 99.99.99.99 255.255.255.255
""")

# Learn AFTER
print("Learning state AFTER...")
after = device.learn("interface")

# Diff with exclusions
print("\n=== Diff (excluding counters) ===")
diff = Diff(before.info, after.info,
            exclude=["counters", "accounting", "rate",
                     "in_rate", "out_rate", "in_pkts",
                     "out_pkts", "in_octets", "out_octets"])
diff.findDiff()
print(diff)

# Verify
if "Loopback99" in after.info:
    print("\n[PASS] Loopback99 created successfully")
else:
    print("\n[FAIL] Loopback99 not found")

# Cleanup — remove Loopback99
print("\nCleaning up...")
device.configure("no interface Loopback99")
print("[OK] Loopback99 removed")

device.disconnect()