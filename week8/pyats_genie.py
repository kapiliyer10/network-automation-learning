from pyats.topology import loader
import json

testbed = loader.load("testbed.yaml")    # load the file, not "NetGuard"

router = testbed.devices["cat8000v"]     # match device name in testbed
router.connect()

# Raw output:
raw = router.execute("show ip interface brief")
print("=== Raw output ===")
print(raw)
print()

# Genie parsed output:
parsed = router.parse("show ip interface brief")
print("=== Parsed output ===")
print(json.dumps(parsed, indent=2))

router.disconnect()