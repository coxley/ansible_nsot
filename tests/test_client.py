import os
import requests
import requests_mock
from ansible_nsot.inventory import NSoTInventory

client = None
here = os.path.abspath(os.path.dirname(__file__))
config_path = '%s/example.yaml' % here
os.environ['NSOT_INVENTORY_CONFIG'] = config_path
base_url = 'http://localhost:8990/api'
YAML_SHOULD_BE = {
    'routers': {
        'query': 'deviceType=ROUTER',
        'vars': {'a': 'b'}
    }
}

AUTH_RESPONSE = {
    'status': 'ok',
    'data': {'auth_token': 'bogus_token'}
}


@requests_mock.Mocker()
class Server(object):
    def __init__(self):
        self.base_url = base_url

    def test_authenticate(self, m):
        uri = self.base_url + '/authenticate/'
        m.register_uri('POST', uri, json=AUTH_RESPONSE)
        return requests.post(uri).text


def mock_auth():
    with requests_mock.Mocker() as mock:
        headers = {'Content-Type': 'application/json'}
        auth_url = base_url + '/authenticate/'
        mock.post(auth_url, json=AUTH_RESPONSE, headers=headers)
        global client
        client = NSoTInventory()


mock_auth()


class TestInventory:
    def test_groups(self):
        assert client.groups == YAML_SHOULD_BE.keys()

    def test_config(self):
        assert client.config == YAML_SHOULD_BE
