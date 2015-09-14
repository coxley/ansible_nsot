import os
from ansible_nsot.inventory import NSoTInventory

here = os.path.abspath(os.path.dirname(__file__))


class Inventory:
    def __init__(self):
        config_path = '%s/example.yaml' % here
        os.environ['NSOT_INVENTORY_CONFIG'] = config_path
        self.client = NSoTInventory()
        self.should_be = {
            'routers': {
                'query': 'deviceType=ROUTER',
                'vars': {'a': 'b'}
            }
        }

    def test_groups(self):
        assert self.client.groups == self.should_be.keys()

    def test_config(self):
        assert self.client.config == self.should_be

    def test_test(self):
        assert 1 == 2
