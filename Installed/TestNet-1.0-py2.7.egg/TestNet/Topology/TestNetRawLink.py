#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetRawLink.py
#  Test Network Raw Link
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

import __builtin__


# Raw weighted link data object
class RawWeightedLink( __builtin__.object ):
	def __init__( self, nodes, weight ):
		(self.src, self.dst) = nodes
		self.nodes = nodes
		self.weight = weight
	
	def nodes( self ):
		return ( self.src, self.dst )
	
	def toString( self ):
		return '((%s, %s), %s)' % (self.src, self.dst, self.weight)


# A weighted link
def wlink( nodes, weight ):
	return RawWeightedLink( nodes, weight )

# List of weighted links
def wlinks( *wlinkList ):
	return [ wlink(n, w)
		for (n, w) in wlinkList ]
