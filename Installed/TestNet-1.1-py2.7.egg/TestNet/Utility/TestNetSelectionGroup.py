#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetSelectionGroup.py
#  Test Network Selection Group
#
#  Created by mpuchkov on 2019-11-17.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#


# TestNetSelectionGroup maintains an indexed group of items
class TestNetSelectionGroup:

	# Set main container
	def __init__( self, group, defaultIndex ):
		self._group = group
		self.defaultIndex = defaultIndex
	
	# Get the group of all items
	def items( self ):
		return self._group
	# Select an item by its index
	def select( self, index ):
		return self._group[ ( index - 1 )  % self.size() ]
	
	# Get the group size
	def size( self ):
		return len( self._group )
	def isEmpty( self ):
		return ( self.size() == 0 )
	
	# Selection range
	def min( self ):
		if ( self.isEmpty() ):
			return 0
		return 1
	def max( self ):
		return self.size()
	def range( self ):
		return ( self.min(), self.max() )
