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


def return_inventory():
    pass


def parse_args():
    desc = __doc__.splitlines()[4]  # Just to avoid being redundant

    # Establish parser with options and error out if no action provided
    parser = argparse.ArgumentParser(
        description=desc,
        version=__version__,
        conflict_handler='resolve',
    )

    # Additional primary actions should also use the same ``action`` and
    # ``dest``, replacing ``const`` with what you want to use in the condition
    #
    # Would use positional args here (eg, list vs --list), but Ansible dictates
    # that optional arg be used
    parser.add_argument(
        '--list', '-l',
        help='Print JSON object containing hosts to STDOUT',
        action='store_const',
        const='list',
        dest='mode',
    )
    args = parser.parse_args()

    if not args.mode:  # Require at least on arg provided.
        parser.error('No action requested')

    return args


def main():
    '''Set up argument handling and callback routing'''
    args = parse_args()

    # Callback condition
    if args.mode == 'list':
        return_inventory()

if __name__ == '__main__':
    main()
