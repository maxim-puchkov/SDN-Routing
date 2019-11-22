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

#from Logger import log
#from Topology import *
##from Environment import TestNetEnvironment
#from Utility import display, parser

#import TestNet

from TestNet import *
from TestNet.Utility import *



#sys.path.insert(1, '../LSRouting')
#import dijkstra

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
	display.section("Building Topology Preset")
	env.prepare( selectedTopoPreset )
	# 5. Launch the network
	display.section("Starting Network")
#	env.launcher.startNetwork( net )
	env.start()
	# 6. Test 1: Destination Host Unreachable
	display.section("Wait: Performing Host Reachability Test 1...")
#	stat = env.netstat.hostReachability()
#	display.highlight(stat)
	
	
	
	#MARK: - Compute the Paths, Create Flow Tables, and do the Second Test
	# 7. Get the switches and link weights
	switches = env.net.topo.switches()
	linkWeights = env.net.topo._slinks

	# 8. Run LS Routing algorithm
	display.section("Wait: Running Link-State Routing algorithm...")
	weights = []
	for i in linkWeights:
		weights.append(('s'+str(i[0]), 's'+str(i[1]), i[2]))
	#
	
	# For each switch
	for switch in switches:
		routes = get_routing_decision( switch, weights )
		for pathToDestination in routes:
			# Least cost paths to destinations
			(destination, path) = pathToDestination
			source = path[0]
			# From source host to destination host
			srcHost = 'h%s' % source[1:]
			dstHost = 'h%s' % destination[1:]
			dstAddress = env.IP(dstHost)
			
			# Add flows
			prev = source
			for i in range( 1, len(path) ):
				current = path[i]
				port = env.outPort(prev, current)
				prev = current
				print('flow add switch=', prev, 'destination address=', dstAddress, 'actions output port = ', port )
				env.flows.add( prev, dstAddress, port )
				
				
#
#				connection = env.connection(prev, current)
#				print(connection)
#				outputPort = env.outPort(connection)
#				print(outputPort)
				
#				env.flows.add( s, 'source ip....', 'outputport....', 'destination ip' )
				
				#add( self, switch, address, outPort )
			
#			print("PATH")
#			print(source, destination)
#			print(path)
#			print(srcHost, dstHost)
			
		
#		env.flows.add( switch, 10.0.0.1, 3 )
		
#		routes = get_routing_decision( s, temp )
#		host
#		(hostIntf, gatewayIntf) host.connectionsTo(src)[0]
#
#		src.IP()
#		(srcIntf, dstIntf) = node.connectionsTo(nextNode)[0]
#		# {dest: [src, node1, node2..., dst]}
	
	display.message("END")
	display.message(routes)
	# 9. Add flow table entries
	# TODO: ...
	
	# 10. Test 2: OK
	display.section("Wait: Performing Host Reachability Test 2...")
#	stat2 = env.netstat.hostReachability( net )
#	display.highlight(stat2)
	
	
	
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
	env.startCLI()
#	env.launcher.enableCommandLineInterface( net )
	
	
	
	#MARK: - Stop Network Simulation
	# N. Stop network
	display.section("Shutting down")
	env.flows.add( 's1', '10.0.0.2', 1 )
	print( env.flows.dump('s1') )
	env.stop()
	
	


if __name__ == '__main__':
	argc = len( sys.argv )
	main( argc, sys.argv )
#	try:
#
#	except:
#		print('\n\nException caught: ')
#		print(sys.exc_info()[0])
		





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
