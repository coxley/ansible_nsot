from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.readlines()[3]

setup(
    name='ansible_nsot',
    version='0.1.0',

    description='Ansible NSoT Dynamic Inventory',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/coxley/ansible_nsot',

    # Author details
    author='Codey Oxley',
    author_email='codey.a.oxley+os@gmail.com',

    license='WTFPL',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development',
        'Topic :: System :: Systems Administration',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    ],

    keywords='ansible automation network ipam inventory',
    packages=find_packages(exclude=['tests*']),

    install_requires=[
        'pynsot',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [
            'pytest',
            'pytest-flake8',
            'bumpversion',
            'ipython',
        ],
    },

    entry_points={
        'console_scripts': [
            'ansible_nsot = ansible_nsot.inventory:main',
        ],
    },
)
