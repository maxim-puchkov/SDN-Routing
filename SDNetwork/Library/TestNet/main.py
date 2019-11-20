#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  main.py
#  Test Network main function
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.topo import *

from Logger import log
from Topology import *
from Link import wlink # makeRawWeightedLink as wlink
from Environment import *
#from Presets import selector
from Utility import display, parser, launcher
from LSRouting import dijkstra

import sys

#sys.path.insert(1, '../LSRouting')
#import dijkstra


def inRange( value, valueRange ):
	(min, max) = valueRange
	return ( value >= min and value <= max )

# Get the index of one of the three networks to start.
#   index 1: 'TinyNetwork', 4 switches s1-s4, 5 links
#   index 2: 'SmallNetwork', 6 switches s1-s6, 10 links
#   index 3: 'LargeNetwork',
def getNetworkTopologyIndex( argv, indexRange ):
	# Default preset index (index starts at 1).
	(minIndex, maxIndex) = indexRange
	index = minIndex
	if ( parser.validate(argc) ):
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
	

# Main function
def main( argc, *argv ):
	log.setLogLevel( 'info' )
	
	# Create a test network environment instance
	env = TestNetEnvironment()
	
	# 1. Read index or ask for input, then select the topology
	index = getNetworkTopologyIndex( argv, env.allTopologies.range() )
	selectedTopo = env.allTopologies.select( index )
#	selectedTopo = TestTopo()
	display.message('Selected network: %s (index: %s)' % (selectedTopo.displayName, index))
	
	
	# Create and start Mininet with the selected topology
	net = Mininet( topo = selectedTopo )
	net.start()
	CLI( net )
	
	# Calculate least-cost paths
	linkWeights = net.topo._slinks
	for switch in net.topo.switches():
		#dijkstra.get_routing_decision(
		print("Swtich:")
		print(switch)
		print("Links")
		print(linkWeights)
		print("Switch num:")
		switchNum = int(switch[1:])
		print(switchNum)
		routes = dijkstra.get_routing_decision(switchNum, linkWeights)
		print("Routes:")
		print(routes)
	
	# Stop Mininet and exit
	net.stop()
    
	
if __name__ == '__main__':
	argc = len(sys.argv)
	main( argc, sys.argv )
