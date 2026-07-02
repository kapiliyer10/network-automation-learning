from pyats.topology import loader

testbed = loader.load("testbed.yaml")

router = testbed.devices["cat8000v"]
router.connect()

output = router.execute("show version")
print(output)

router.disconnect()