#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetEnvironment.py
#  Test Network Environment, OpenFlow Table Management
#
#  Created by mpuchkov on 2019-11-18.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.clean import cleanup
from TestNet.Logger import log
from TestNet.Topology import ( BabyTopo, TinyTopo,
							   SmallTopo, LargeTopo,
							   TestNetEnvCLI )
from TestNet.Utility import ( TestNetLauncher, TestNetSelectionGroup,
							  parser, display )


# Three default Topology presets
def defaultPresetGroup():
	group = ( BabyTopo, TinyTopo, SmallTopo, LargeTopo )
	return TestNetSelectionGroup( group, 2 )

# Check a value is within (min, max) value range
def inRange( value, valueRange ):
	(min, max) = valueRange
	return ( value >= min and value <= max )

# Ping a node from another node
def ping( n1, n2, c = 1 ):
	_command = 'ping -c%s %s' % (c, n2.IP())
	return ( _command, n1.cmd(_command) )

def last( _list ):
	return _list[ len(_list) - 1 ]










# Provides interface to start networks, control,
#   and test simulated networks
class TestNetEnvironment:
	def __init__( self ):
		self.launcher = TestNetLauncher()
		self.presetTopologies = defaultPresetGroup()
	
	# Remove previous mininet data
	def clean( self ):
		cleanup()
		log.infoln('Cleaned up old files')
	
	
	# Update Routing Tables
	def updateRoutes( self, lsAlgorithm, switches, linkWeights ):
		display.section("Running Link-State Routing algorithm ...")
		log.infoln('Switch\t Protocols\t Dst-Address\t Actions')
		log.infoln('-------------------------------------------------------')

		weights = [ ( 's'+str(i[0]), 's'+str(i[1]), i[2] )
			for i in linkWeights ]
		# For each switch
		for source in switches:
			routes = lsAlgorithm( source, weights )
			# Compute the least cost route for each destination
			prev = source
			for route in routes:
				# Least cost paths to destinations
				dst = last(route)
				dstHost = 'h%s' % dst[1:]
				dstAddress = self.IP(dstHost)
				## Switches to the connected host
				srcHost = 'h%s' % source[1:]
				srcAddress = self.IP(srcHost)
				outToSrc = self.outputPort( source, srcHost )
				self.flows.add( source, srcAddress, outToSrc )
				## Switches to switches
				prev = source
				for i in range( 1, len(route) ):
					current = route[i]
					outToNext = self.outputPort( prev, current )
					self.flows.add( prev, dstAddress, outToNext )
					prev = current
		
	
	# Node instances
	def getNode( self, name ):
		return self.net.nameToNode[name]
	
	def getNodes( self, *names ):
		print('names: ', names )
		for n in names: print n
		return [ self.net.nameToNode[name]
			for name in names ]
		
	
	def IP( self, name ):
		return self.getNode(name).IP()
		
	
	# Output port from node with name1
	def outputPort( self, name1, name2 ):
		node1 = self.getNode(name1)
		node2 = self.getNode(name2)
		con = node1.connectionsTo(node2)[0]
		(intf1, intf2) = con
		return intf1.node.ports[intf1]
		
	
	# Initialize network and flow tables
	def prepare( self, preset ):
		self.net = self.launcher.prepareNetwork( preset )
		self.flows = TestNetEnvironment.FlowTableManager( self.net.controller )
	
	# Start simulation
	def start( self ):
		self.launcher.startNetwork( self.net )
	
	# Stop simulation
	def stop( self ):
		self.launcher.stopNetwork( self.net )
	
	# Interact
	def startCLI( self ):
		self.CLI = TestNetEnvCLI( self.net )
	
	
	
	# OpenFlow
	class FlowTableManager:
		shell = 'sh'
		program = 'sudo ovs-ofctl'
		protocols = ['ARP', 'IP']
		
		def __init__( self, controller ):
			self.controller = controller
		
		def do( self, ofCommand ):
			shCommand = ' '.join( [self.program, ofCommand] )
			return self.controller.cmd( shCommand )
		
		# Dump flows
		def dump( self, switch ):
			return self.do( 'dump-flows ' + switch )
		
		# Add a new flow
		def add( self, switch, dstAddress, oPort ):
			log.info('%s\t\t %s\t %s\t output:%s\n'
				% (switch, ', '.join(self.protocols), dstAddress, oPort))
			return [ self.do( 'add-flow %s %s,nw_dst=%s,actions=output:%s' % (switch, protocol.lower(), dstAddress, oPort) )
				for protocol in self.protocols ]
			
		
		def clear( self, switch ):
			return self.do( 'del-flows ' + switch )
		
	
	# Two test hosts (h1, h2)
	def getTestHosts( self ):
		return ( self.net.hosts[0], self.net.hosts[1] )
	
	# Testing network
	def nodeReachability( self, n1, n2 ):
		return ( ping(n1, n2), ping(n2, n1) )
	
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
			display.networkSelectionMenu( self.presetTopologies )
			display.prompt('Input the index (%s to %s) of a network you want to test: ' % (minIndex, maxIndex))
			index = parser.waitForInput()
			# If input is invalid, then choose the first
			#   network in the list (starts at index 1).
			if not ( inRange(index, indexRange) ) :
				display.error('Index %s is out of range. Resetting index to %s.' % (index, minIndex))
				index = minIndex
		return index
		
	
	# Disable the link between node1 and node2
	def disableLink( self, linkNodeNames ):
		(name1, name2) = linkNodeNames
		(node1, node2) = self.getNodes( name1, name2 )
		link = self.net.linksBetween(node1, node2)[0] #link.stop()
		log.infoln('Link between nodes %s and %s has been disabled' % (node1.name, node2.name))
		return link



