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
from Link import wlink


# Large Topology (Example Network 3)
#
# Link costs:
#	randomized
class LargeTopo( LinkTopo ):
	displayName = 'Large Topology'
	
	def build( self ):
		switches = 0 #!
		hostsPerSwitch = 0 #!
		linkWeights = () #!
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )
