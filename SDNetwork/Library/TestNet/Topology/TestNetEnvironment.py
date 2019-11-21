#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetEnvironment.py
#  Test Network Environment
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.clean import cleanup
from TestNet.Topology import TinyTopo, SmallTopo, LargeTopo
from TestNet.Logger import log
from TestNet.Utility import *


# Three default Topology presets
def defaultPresetGroup():
	group = ( TinyTopo, SmallTopo, LargeTopo )
	return TestNetSelectionGroup( group )

# Check a value is within (min, max) value range
def inRange( value, valueRange ):
	(min, max) = valueRange
	return ( value >= min and value <= max )

def ping( h1, h2, c = 1 ):
	return h1.cmd( 'ping -c %s %s' % (c, h2.IP()) )
	
	
# Analyze and test network simulation
class TestNetEnvironmentStatistics:
	
	
	# Test if two hosts can ping each other
	def hostReachability( self, network ):
		first = network.hosts[0]
		last = network.hosts[len(network.hosts) - 1]
		return ping( first, last ), ping( last, first )
		
	def switchReachability( self, network ):
		first = network.hosts[0]
		last = network.hosts[len(network.hosts) - 1]
		return ping( first, last ), ping( last, first )

#
class TestNetEnvironment:
	def __init__(self):
		self.launcher = TestNetLauncher()
		self.presetTopologies = defaultPresetGroup()
		self.netstat = TestNetEnvironmentStatistics()
	
	# Remove previous mininet data
	def clean( self ):
		cleanup()
		log.infoln("Cleaned up old files")
	
	# Get the index of one of the three networks to start.
	#   index 1: 'TinyNetwork', 4 switches s1-s4, 5 links
	#   index 2: 'SmallNetwork', 6 switches s1-s6, 10 links
	#   index 3: 'LargeNetwork',
	def getNetworkTopologyIndex( self, argv, indexRange ):
		# Default preset index (index starts at 1).
		(minIndex, maxIndex) = indexRange
		index = minIndex
		if ( parser.validate(argv) ):
			# If arguments are valid, get the index
			index = parser.getIndex( argv )
		else:
			# If network was not chosen on script start,
			#   show the list of preset networks, and
			#   ask to choose one.
			display.networkSelectionMenu()
			display.prompt('Input the index (%s to %s) of a network you want to test: ' % (minIndex, maxIndex))
			index = parser.waitForInput()
			# If input is invalid, then choose the first
			#   network in the list (starts at index 1).
			if not ( inRange(index, indexRange) ) :
				display.error('Index %s is out of range. Resetting index to %s.' % (index, minIndex))
				index = minIndex
		return index
	

	
	