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
	def __init__( self, group ):
		# Index '0' is displayed to the
		#   user as '1'; '1' as '2'; etc.
		self.elementOffset = 1
		self._group = group
	
	# Get the group of all items
	def group( self ):
		return self._group
	
	# Get the group size
	def size( self ):
		return len( self._group )
	
	def isEmpty( self ):
		return ( self.size() == 0 )
	
	# Select an item by its index
	def select( self, index ):
		return self._group[ ( index - self.elementOffset )  % self.size()]
	
	#MARK: - Selection range
	def min( self ):
		if ( self.isEmpty() ):
			return 0
		return self.elementOffset
	
	def max( self ):
		return self.size()
	
	def range( self ):
		return ( self.min(), self.max() )
