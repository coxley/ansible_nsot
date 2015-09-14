import sys
import pytest
from ansible_nsot import inventory


class TestArgs:
    def test_withold_command(self):
        sys.argv = ['inventory.py']
        with pytest.raises(SystemExit):
            inventory.parse_args()

    def test_with_list(self):
        sys.argv = ['inventory.py', '--list']
        assert inventory.parse_args().mode == 'list'

    def test_with_bad_option(self):
        sys.argv = ['inventory.py', '--list', '--foo']
        with pytest.raises(SystemExit):
            inventory.parse_args()
