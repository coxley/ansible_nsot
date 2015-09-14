import os
from ansible_nsot.inventory import NSoTInventory

here = os.path.abspath(os.path.dirname(__file__))
config_path = '%s/example.yaml' % here
os.environ['NSOT_INVENTORY_CONFIG'] = config_path
client = NSoTInventory()
should_be = {
    'routers': {
        'query': 'deviceType=ROUTER',
        'vars': {'a': 'b'}
    }
}


class TestInventory:
    def test_groups(self):
        assert client.groups == should_be.keys()

    def test_config(self):
        assert client.config == should_be
