import sys
import pytest
from ansible_nsot import inventory


class TestParams:
    def test_withold_command(self):
        with pytest.raises(SystemExit):
            inventory.parse_args()

    def test_with_list(self):
        sys.argv = '--list'.split()
        assert inventory.parse_args().list_

    def test_with_host(self):
        sys.argv = '--host rtr.example.com'.split()
        assert inventory.parse_args().host

        # Do not allow left out hostname if --host
        with pytest.raises(SystemExit):
            sys.argv = '--host'.split()
            inventory.parse_args()

    def test_with_both(self):
        with pytest.raises(SystemExit):
            sys.argv = '--list --host rtr.example.com'.split()
            inventory.parse_args()

    def test_with_bad_option(self):
        with pytest.raises(SystemExit):
            sys.argv = '--list --foo'.split()
            inventory.parse_args()
