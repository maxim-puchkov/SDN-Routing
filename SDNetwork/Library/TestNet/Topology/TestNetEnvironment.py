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
from TestNet.Topology import * # TinyTopo, SmallTopo, LargeTopo
from TestNet.Logger import log
from TestNet.Utility import *


# Three default Topology presets
def defaultPresetGroup():
	group = ( TinyTopo, SmallTopo, LargeTopo, BabyTopo )
	return TestNetSelectionGroup( group )

# Check a value is within (min, max) value range
def inRange( value, valueRange ):
	(min, max) = valueRange
	return ( value >= min and value <= max )

# Ping a node from another node
def ping( n1, n2, c = 1 ):
	return n1.cmd( 'ping -c %s %s' % (c, n2.IP()) )
	
	

#
class TestNetEnvironment:
	def __init__(self):
		self.launcher = TestNetLauncher()
		self.presetTopologies = defaultPresetGroup()
	
	# Remove previous mininet data
	def clean( self ):
		cleanup()
		log.infoln("Cleaned up old files")
	
	def prepare( self, preset ):
		self.net = self.launcher.prepareNetwork( preset )
		self.netstat = TestNetEnvironment.NetworkStatistics( self.net )
	
	def start( self ):
		self.launcher.startNetwork( self.net )
		
	def stop( self ):
		self.launcher.stopNetwork( self.net )
	
	def startCLI( self ):
		self.CLI = TestNetEnvCLI( self.net )
	
	
	class NetworkStatistics:
		def __init__( self, network ):
			self.network = network
		
		def hostReachability( self ):
			n = self.network
			first = n.hosts[0]
			last = n.hosts[len( n.hosts ) - 1]
			return ping( first, last ), ping( last, first )
		#
		def switchReachability( self ):
			n = self.network
			first = n.switches[0]
			last = n.switches[len( n.switches ) - 1]
			return ping( first, last ), ping( last, first )
	
	# Get the index of one of the three networks to start.
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
	

	
	
