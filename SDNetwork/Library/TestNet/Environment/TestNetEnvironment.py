#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetEnvironment.py
#  Test Network Environment
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.net import Mininet # MininetWithControlNet
from mininet.cli import CLI

from Logger import log
from Topology import TinyTopo, SmallTopo, LargeTopo
from Utility import TestNetSelectionGroup


#class TestNetEnvironment( MininetWithControlNet ):
class TestNetEnvironment( Mininet ):
	def __init__( self, **_kwargs ):
		def topologySelectionGroup():
			group = ( TinyTopo, SmallTopo, LargeTopo )
			return TestNetSelectionGroup( group )
			
		log.do("Initialize %s." % self.__module__)
		self.allTopologies = topologySelectionGroup()
		#Mininet.__init__( self, _kwargs )
		log.done("Initialized TestNetEnvironment<%s>." % id(self))
	
	def prepare( self, **_kwargs ):
		self = Mininet.__init__( self, _kwargs )
		
	
	
	
