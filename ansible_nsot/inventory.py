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
import json
import yaml
from pynsot.client import get_api_client

# Version source of truth is in setup.py
__version__ = pkg_resources.require('ansible_nsot')[0].version


class NSoTInventory(object):
    '''NSoT Client object for gather inventory'''

    def __init__(self):
        self.config = dict()
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
        self._meta = {'hostvars': dict()}

    def do_list(self):
        '''Direct callback for when ``--list`` is provided

        Relies on the configuration generated from init to run
        _inventory_group()
        '''
        inventory = dict()
        for group, contents in self.config.iteritems():
            group_response = self._inventory_group(group, contents)
            inventory.update(group_response)
        inventory.update({'_meta': self._meta})
        return json.dumps(inventory)

    def do_host(self, host):
        return self._hostvars(host)

    def _hostvars(self, host):
        '''Return dictionary of all device attributes'''
        pass

    def _inventory_group(self, group, contents):
        '''Takes a group and returns inventory for it as dict

        :param group: Group name
        :type group: str
        :param contents: The contents of the group's YAML config
        :type contents: dict

        contents param should look like::

            {
              'query': 'xx',
              'vars':
                  'a': 'b'
            }

        Will return something like::

            { group: {
                hosts: [],
                vars: {},
            }
        '''
        query = contents.get('query')
        hostvars = contents.get('vars', dict())
        obj = {group: dict()}
        obj[group]['hosts'] = []
        obj[group]['vars'] = hostvars
        try:
            assert isinstance(query, basestring)
        except:
            sys.exit('ERR: Group queries must be a single string\n'
                     '  Group: %s\n'
                     '  Query: %s\n' % (group, query)
                     )
        devices = self.client.devices.query.get(query=query)
        # Would do a list comprehension here, but would like to save code/time
        # and also acquire attributes in this step
        for host in devices['data']['devices']:
            # Iterate through each device that matches query, assign hostname
            # to the group's hosts array and then use this single iteration as
            # a chance to update self._meta which will be used in the final
            # return
            hostname = host['hostname']
            obj[group]['hosts'].append(hostname)
            attributes = host['attributes']
            self._meta['hostvars'].update({hostname: attributes})

        return obj


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
        print client.do_list()
    elif args.host:
        client.do_host(args.host)

if __name__ == '__main__':
    main()
