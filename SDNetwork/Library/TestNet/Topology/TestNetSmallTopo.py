#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetTopo.py
#  Test Network Topologies
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from TestNetTopo import LinkTopo
from Link import wlinks


# Small Topology (Example Network 2)
class SmallTopo( LinkTopo ):
	displayName = 'Small Topology'
	
	def build( self ):
		switches = 6
		hostsPerSwitch = 2
		linkWeights = wlinks(
			((1, 2), 2), ((1, 3), 5), ((1, 4), 1),
			((2, 3), 3), ((2, 4), 2),
			((3, 4), 3), ((3, 5), 1), ((3, 6), 5),
			((4, 5), 1),
			((5, 6), 2)
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )
