#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetSmallTopo.py
#  Test Network Topologies
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from TestNetTopo import LinkTopo
from Link import wlinks


# Tiny Topology (Example Network 1)
# Network with 4 switches, with 5 bidirectional links.
#
# One-directional links (10):
#   s1 <-> (s2, s3, s4)
#   s2 <-> (s1, s4)
#   s3 <-> (s1, s4)
#   s4 <-> (s1, s2, s3)
#
# Link costs:
#   s1-s2:  2
#   s1-s3:  1
#   s1-s4:  2
#   s2-s4:  3
#   s3-s4:  3
class TinyTopo( LinkTopo ):
	displayName = 'Tiny Topology'
	
	def build( self ):
		switches = 4
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 2), ((1, 3), 1), ((1, 4), 2),
			((2, 4), 3),
			((3, 4), 3)
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )


class TestTopo( LinkTopo ):
	displayName = 'Tiny Topology'
	
	def build( self ):
		switches = 3
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 1), ((1, 3), 1), ((2, 3), 1)
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )

#
#s1-s2 1 2
#s1-s3 1 3
#s2-s3 2 3
#
#s1-s2 1 1
#s1-s3 2 1
#s2-s3 2 2
