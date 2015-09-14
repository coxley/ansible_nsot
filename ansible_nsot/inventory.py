#!/bin/env python2.7

'''
inventory.py
============

Take params as defined by the Ansible Project and return hosts from NSoT

'''

import sys
import os
import pkg_resources
import argparse
import yaml
from pynsot.client import get_api_client

# Version source of truth is in setup.py
__version__ = pkg_resources.require('ansible_nsot')[0].version


class NSoTInventory(object):
    '''NSoT Client object for gather inventory'''

    def __init__(self):
        self.config = {}
        config_env = os.environ.get('NSOT_INVENTORY_CONFIG')
        if config_env:
            try:
                config_file = os.path.abspath(config_env)
            except Exception as e:
                sys.exit('%s\n' % e)

            with open(config_file) as f:
                try:
                    self.config.update(yaml.safe_load(f))
                except Exception as e:
                    sys.exit('%s\n' % e)
        self.groups = self.config.keys()
        self.client = get_api_client()

    def get_inventory(self):
        pass

    def get_host(self, host):
        pass


def parse_args():
    desc = __doc__.splitlines()[4]  # Just to avoid being redundant

    # Establish parser with options and error out if no action provided
    parser = argparse.ArgumentParser(
        description=desc,
        version=__version__,
        conflict_handler='resolve',
    )

    # Arguments
    #
    # Currently accepting (--list | -l) and (--host | -h)
    # These must not be allowed together
    parser.add_argument(
        '--list', '-l',
        help='Print JSON object containing hosts to STDOUT',
        action='store_true',
        dest='list_',  # Avoiding syntax highlighting for list
    )

    parser.add_argument(
        '--host', '-h',
        help='Print JSON object containing hostvars for <host>',
        action='store',
    )
    args = parser.parse_args()

    if not args.list_ and not args.host:  # Require at least one option
        parser.exit(status=1, message='No action requested')

    if args.list_ and args.host:  # Do not allow multiple options
        parser.exit(status=1, message='Too many actions requested')

    return args


def main():
    '''Set up argument handling and callback routing'''
    args = parse_args()
    client = NSoTInventory()

    # Callback condition
    if args.list_:
        client.get_inventory()
    elif args.host:
        client.get_host(args.host)

if __name__ == '__main__':
    main()
