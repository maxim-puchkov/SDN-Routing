#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetLink.py
#  Test Network Link
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.link import Link


class WeightedLink( Link ):

	def __init__( self, node1, node2, weight, **_kwargs ):
		Link.__init__( self, node1, node2, _kwargs)
		self.src = node1
		self.dst = node2
		self.weight = weight
		
	def nodes( self ):
		return ( self.src, self.dst )
	
	def cost( self ):
		return self.weight
