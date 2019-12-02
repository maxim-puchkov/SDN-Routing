#!/usr/bin/env python

"Setuptools params"

import sys
from os.path import join
from os.path import dirname
from setuptools import setup, find_packages


modname = distname = 'TestNet'
tnlib = 'Library/' + modname


sys.path.append( '.' )
sys.path.append('..' + dirname(__file__))
print(sys.path)


setup(
    name=distname,
    version='1.2',
    description='Process-based OpenFlow emulator',
    author='Maxim Puchkov, Xiyu Zhang',
    author_email='mpuchkov@sfu.ca',
    packages=[ 'TestNet', 'TestNet.Topology', 'TestNet.Logger', 'TestNet.Utility' ],
    long_description="""
        SDN Simulation and Routing
        """,
    classifiers=[
          "Programming Language :: Python",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Topic :: System :: Emulators",
    ],
    keywords='networking emulator protocol Internet OpenFlow SDN',
    install_requires=[
        'setuptools'
    ],
)
