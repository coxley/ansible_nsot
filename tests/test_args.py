import sys
import pytest
from ansible_nsot import inventory


class TestParams:
    def test_withold_command(self):
        with pytest.raises(SystemExit):
            inventory.parse_args()

    def test_with_list(self):
        sys.argv = 'ansible_nsot --list'.split()
        assert inventory.parse_args().list_

    def test_with_host(self):
        sys.argv = 'ansible_nsot --host rtr.example.com'.split()
        assert inventory.parse_args().host

        # Do not allow left out hostname if --host
        with pytest.raises(SystemExit):
            sys.argv = 'ansible_nsot --host'.split()
            inventory.parse_args()

    def test_with_both(self):
        with pytest.raises(SystemExit):
            sys.argv = 'ansible_nsot --list --host rtr.example.com'.split()
            inventory.parse_args()

    def test_with_bad_option(self):
        with pytest.raises(SystemExit):
            sys.argv = 'ansible_nsot --list --foo'.split()
            inventory.parse_args()
