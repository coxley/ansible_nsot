#!/bin/env python2.7

'''
inventory.py
============

Take params as defined by the Ansible Project and return hosts from NSoT

'''

import pkg_resources
import argparse

# Version source of truth is in setup.py
__version__ = pkg_resources.require('ansible_nsot')[0].version


# TODO: These two functions will likely be replaced with a class. Placeholders
# for writing tests/structure currently
def return_inventory():
    pass


def return_hostvars():
    pass


# TODO: Create setup function for importing configuration via
# NSOT_INVENTORY_CONFIG

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

    if not args.list_ or not args.host:  # Require at least one option
        parser.error('No action requested')

    if args.list_ and args.host:  # Do not allow multiple options
        parser.error('Too many actions requested')

    return args


def main():
    '''Set up argument handling and callback routing'''
    args = parse_args()

    # Callback condition
    if args.list_:
        return_inventory()
    elif args.host:
        return_hostvars(args.host)

if __name__ == '__main__':
    main()
