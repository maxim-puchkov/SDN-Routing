#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  main.py
#  Test Network main function
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

import sys

from Logger import log
from Environment import TestNetEnvironment
from Utility import display, parser


#sys.path.insert(1, '../LSRouting')
#import dijkstra
from LSRouting import dijkstra

# [   {s2: (switchX, switchY) }, {}   ] = (switch, [costs, ...])
# for [ { }  ]



	









# Main function
def main( argc, *argv ):

	#MARK: - Select Network Topology
	# 1. Create environment for creating, running, and testing
	#    network simulations from presets
	env = TestNetEnvironment()
	# 2. Ask to input the index of a topology preset
	display.section("Select Network")
	index = env.getNetworkTopologyIndex( argv, env.presetTopologies.range() )
	# 3. Select the preset with that index
	selectedTopoPreset = env.presetTopologies.select( index )
	display.message('Selected network: %s (index: %s)' % (selectedTopoPreset.displayName, index))
	
	
	
	#MARK: - Begin Network Simulation and do the First Test
	# 4. Cleanup, then initialize a new network with selected topology
	display.section("Cleaning up")
	env.clean()
	net = env.launcher.prepareNetwork( preset = selectedTopoPreset )
	# 5. Launch the network
	display.section("Starting Network")
	env.launcher.startNetwork( net )
	# 6. Test 1: Destination Host Unreachable
	display.section("Wait: Performing Host Reachability Test 1...")
	stat = env.netstat.hostReachability( net )
	display.highlight(stat)
	
	
	
	#MARK: - Compute the Paths, Create Flow Tables, and do the Second Test
	# 7. Get the switches and link weights
	switches = net.topo.switches()
	linkWeights = net.topo._slinks
	num = lambda switch : int( switch[1:] )
	# 8. Run LS Routing algorithm
	display.section("Wait: Running Link-State Routing algorithm...")
	for s in switches:
		# routes = dijkstra.get_routing_decision(num(s), linkWeights)
		routes = [ {1: (2, 3, 4)}, {2: (3, 4, 5)}, {123: (4, 5, 6)} ]
	display.highlight(routes)
	# 9. Add flow table entries
	# TODO: ...
	
	# 10. Test 2: OK
	display.section("Wait: Performing Host Reachability Test 2...")
	stat = env.netstat.hostReachability( net )
	display.highlight(stat)
	
	
	
	#MARK: - Disable one of the Links and do the Third Test
	# N. Disable a link
	# TODO: ...
	
	# N. Test 4:
	# TODO: ...
	
	
	
	#MARK: - Recompute the Least-Cost Paths and do the Fourth Test
	# N.
	# TODO: ...
	
	# N. Test 3:
	# TODO: ...
	
	
	
	
	#MARK: - Command Line Interface
	# N. Start the CLI to run other tests
	display.section("Starting Command Line Interface")
	env.launcher.enableCommandLineInterface( net )
	
	
	#MARK: - Stop Network Simulation
	# N. Stop network
	display.section("Shutting down")
	env.launcher.stopNetwork( net )
	
	
	
if __name__ == '__main__':
	argc = len(sys.argv)
	main( argc, sys.argv )





#	# Calculate least-cost paths
#	linkWeights = net.topo._slinks
#	for switch in net.topo.switches():
#		#dijkstra.get_routing_decision(
#		print("Swtich:")
#		print(switch)
#		print("Links")
#		print(linkWeights)
#		print("Switch num:")
#		switchNum = int(switch[1:])
#		print(switchNum)
#		routes = dijkstra.get_routing_decision(switchNum, linkWeights)
#		print("Routes:")
#		print(routes)















	#	test = TestTopo()
		# Create and start Mininet with the selected topology

#	net = Mininet( topo = selectedTopo )
#	net.start()
#	CLI( net )
