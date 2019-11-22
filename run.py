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

from TestNet import *
from TestNet.Utility import *


# Main function
def main( argc, *argv ):

	#MARK: - Select Network Topology
	# 1. Create environment for creating, running, and testing
	#    network simulations from presets
	env = TestNetEnvironment()
	display.section("Cleaning up")
	env.clean()
	# 2. Ask to input the index of a topology preset
	display.section("Select Network")
	index = env.getNetworkTopologyIndex( argv, env.presetTopologies.range() )
	# 3. Select the preset with that index
	selectedTopoPreset = env.presetTopologies.select( index )
	display.message('Selected network: %s (index: %s)' % (selectedTopoPreset.displayName, index))
	
	
	
	
	
	
	
	
	
	#MARK: - Begin Network Simulation and do the First Test
	# 4. Initialize a new network with selected topology
	display.section("Building Topology Preset")
	env.prepare( selectedTopoPreset )
	# 5. Launch the network
	display.section("Starting Network")
	env.start()
	# 6. Test 1: Destination Host Unreachable
	display.section("Test 1: Hosts are unreachable...")
	(host1, host2) = env.getTestHosts()
	test = env.nodeReachability(host1, host2)
	display.highlight(test)
	
	
	
	
	
	
	
	
	
	
	
	#MARK: - Compute the Paths, Create Flow Tables, and do the Second Test
	# 7. Get the switches and link weights
	switches = env.net.topo.switches()
	linkWeights = env.net.topo._slinks

	# 8. Run LS Routing algorithm
	display.section("Running Link-State Routing algorithm...")
	display.message('Switch Number\t Address\t Output Port')
	weights = []
	for i in linkWeights:
		weights.append( ('s'+str(i[0]), 's'+str(i[1]), i[2]) )
	# For each switch
	for source in switches:
		routes = get_routing_decision( source, weights )
		for pathToDestination in routes:
			# Least cost paths to destinations
			(destination, path) = pathToDestination
			# From source host to destination host
			dstHost = 'h%s' % destination[1:]
			dstAddress = env.IP(dstHost)
			
			
			
			#TODO: # 9. Add flow table entries
			## Switches to the connected host
			srcHost = 'h%s' % source[1:]
			srcAddress = env.IP(srcHost)
			outToSrc = env.outPort( source, srcHost )
			env.flows.add( source, srcAddress, outToSrc )
			
			## Switches to switches
			prev = source
			for i in range( 1, len(path) ):
				current = path[i]
				outToNext = env.outPort( prev, current )
				env.flows.add( prev, dstAddress, outToNext )
				prev = current
	
	# 10. Test 2: OK
	display.section("Test 2: Hosts are now connected...")
	test2 = env.nodeReachability(host1, host2)
	display.highlight(test2)
	
	
	
	
	
	
	
	
	
	
	#MARK: - Disable one of the Links and do the Third Test
	# 11. Disable a link
	link = env.net.topo.problemLink
	n1 = int( link[0][1:] )
	n2 = int( link[1][1:] )
	display.section("Changing network conditions")
	display.message('Problem link in this simulation is {%s, %s}' % link )
	display.message('Problem link between %s %s is down' % link )
#	env.disableLink(link)
	
	# 12. Test 3: Hosts
	display.section("Test 3: Hosts can't communicate...")
	test3 = env.nodeReachability(host1, host2)
	display.highlight(test3)
	
	
	
	
	
	
	
	
	
	
	#MARK: - Recompute the Least-Cost Paths and do the Fourth Test
	# 13.
	for (prev1, prev2, w) in linkWeights:
		if ((prev1 == n1 and prev2 == n2) or (prev1 == n2 and prev2 == n1)):
			linkWeights.remove( (prev1, prev2, w) )
			linkWeights.append( (str(n1), str(n2), 1000) )
			log.infoln('Replacing link %s with %s' % ([(prev1, prev2, w)], [(n1, n2, 1000)]) )
			break
	
	weightsUpdated = []
	for i in linkWeights:
		weightsUpdated.append( ('s'+str(i[0]), 's'+str(i[1]), i[2]) )
	
	log.info('Deleting all flows of switch s1')
	for source in switches:
		print(', %s' % source),
		env.flows.clear(source) # delete all old flows
	print('')
	
	
	display.section("Running Link-State Routing algorithm again...")
	display.message('Switch Number\t Address\t Output Port')
	# For each switch
	for source in switches:
		routes = get_routing_decision( source, weightsUpdated )
		for pathToDestination in routes:
			# Least cost paths to destinations
			(destination, path) = pathToDestination
			# From source host to destination host
			dstHost = 'h%s' % destination[1:]
			dstAddress = env.IP(dstHost)
			#MARK: Add flow table entries
			## Switches to the connected host
			srcHost = 'h%s' % source[1:]
			srcAddress = env.IP(srcHost)
			outToSrc = env.outPort( source, srcHost )
			env.flows.add( source, srcAddress, outToSrc )
			## Switches to switches
			prev = source
			for i in range( 1, len(path) ):
				current = path[i]
				outToNext = env.outPort( prev, current )
				env.flows.add( prev, dstAddress, outToNext )
				prev = current
	# 14. Test 4:
	display.section("Test 4: Hosts can communicate again...")
	test4 = env.nodeReachability(host1, host2)
	display.highlight(test4)
	
	
	
	
	#MARK: - Command Line Interface
	# 15. Start the CLI to run other tests
	display.section("Starting Command Line Interface")
	env.startCLI()
	
	
	
	#MARK: - Stop Network Simulation
	# 16. Stop network
	display.section("Shutting down")
	env.stop()
	
	


if __name__ == '__main__':
	argc = len( sys.argv )
	main( argc, sys.argv )
