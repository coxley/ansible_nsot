ansible_nsot
============

.. image:: https://travis-ci.org/coxley/ansible_nsot.svg
    :target: https://travis-ci.org/coxley/ansible_nsot

.. image:: http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-2.png
   :target: http://www.wtfpl.net/
   :alt: Do what the fuck you want
   :height: 25px

Ansible Dynamic Inventory to pull hosts from `NSoT`_

.. _NSoT: https://github.com/dropbox/nsot

Features
--------

Refer to Ansible's dynamic inventory spec `here`_ for more details of what some
of these features mean.

.. _here: http://docs.ansible.com/ansible/developing_inventory.html

* Define host groups in form of NSoT device attribute criteria

* All parameters defined by the spec as of 2015-09-05 are supported.

  + ``--list``: Returns JSON hash of host groups -> hosts and top-level
    ``_meta`` -> ``hostvars`` which correspond to all device attributes.

    Group vars can be specified in the YAML configuration, noted below.

  + ``--host <hostname>``: Returns JSON hash where every item is a device
    attribute.

Installation
------------

To install, run pip against the archive you want to install from (branch or
release tag)::

    pip install https://github.com/coxley/ansible_nsot/archive/master.zip
    # or...
    pip install https://github.com/coxley/ansible_nsot/archive/0.1.0.zip

To use it from Ansible, either supply ``-i <path/to/script>`` or configure it
in ``ansible.cfg`` with ``inventory = <path/to/script>``

Confguration
------------

Since it'd be annoying and failure prone to guess where you're configuration
file is, use ``NSOT_INVENTORY_CONFIG`` to specify the path to it.

This file should adhere to the YAML spec. All top-level variable must be
desired Ansible group-name hashed with single 'query' item to define the NSoT
attribute query.

Queries follow the normal NSoT query syntax, `show here`_

.. _shown here: https://github.com/dropbox/pynsot#set-queries

.. code:: yaml

   routers:
     query: 'deviceType=ROUTER'
     vars:
       a: b
       c: d

   juniper_fw:
     query: 'deviceType=FIREWALL manufacturer=JUNIPER'

   not_f10:
     query: '-manufacturer=FORCE10'

The inventory will automatically use your ``.pynsotrc`` like normal pynsot from
cli would, so make sure that's configured appropriately.

Note that the attributes I'm showing above are influenced from ones that the
Trigger project likes. As is the spirit of NSoT, use whichever attributes work
best for your workflow.

If config file is blank, the following default groups will be created:

* ``routers``: deviceType=ROUTER
* ``switches``: deviceType=SWITCH
* ``firewalls``: deviceType=FIREWALL

These are likely not useful for everyone so please use the configuration. :)
