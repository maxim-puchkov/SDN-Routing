#!/usr/bin/env python

"Setuptools params"

import sys
from os.path import join
from os.path import dirname
from setuptools import setup, find_packages


modname = distname = 'LSRouting'
lsrlib = 'Library/' + modname

sys.path.append( '.' )
sys.path.append('..' + dirname(__file__))
print(sys.path)


setup(
    name=distname,
    version='1.0',
	description='Dijkstra\'s least-cost paths LS routing',
    author='Maxim Puchkov, Xiyu Zhang',
    author_email='mpuchkov@sfu.ca',
    packages=[ 'LSRouting' ],
    long_description="""
        LS Routing
        """,
    classifiers=[
          "Programming Language :: Python",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Topic :: System :: Emulators",
    ],
    keywords='Link-State routing algorithm for simulated OpenFlow SDN switches',
    install_requires=[
        'setuptools'
    ],
)
