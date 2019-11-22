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
	
	def getNode( self, name ):
		return self.net.nameToNode[name]
	
	def IP( self, name ):
		return self.getNode(name).IP()
	
	# Output port from node with name1
	def outPort( self, name1, name2 ):
		node1 = self.getNode(name1)
		node2 = self.getNode(name2)
		con = node1.connectionsTo(node2)[0]
		(intf1, intf2) = con
		return intf1.node.ports[intf1]
	
	# Remove previous mininet data
	def clean( self ):
		cleanup()
		log.infoln("Cleaned up old files")
	
	def prepare( self, preset ):
		self.net = self.launcher.prepareNetwork( preset )
		self.netstat = TestNetEnvironment.NetworkStatistics( self.net )
		self.flows = TestNetEnvironment.FlowTableManager( self.net.controller )
	
	def start( self ):
		self.launcher.startNetwork( self.net )
		
	def stop( self ):
		self.launcher.stopNetwork( self.net )
	
	def startCLI( self ):
		self.CLI = TestNetEnvCLI( self.net )
	
	
	# OpenFlow
	class FlowTableManager:
		shell = 'sh'
		program = 'sudo ovs-ofctl'
		
		def __init__( self, controller ):
			self.controller = controller
		
		def do( self, ofCommand ):
			shCommand = ' '.join( [self.program, ofCommand] )
			return self.controller.cmd( shCommand )
		
		# Dump flows
		def dump( self, switch ):
			return self.do( 'dump-flows ' + switch )
		
		# Add new flow
		def add( self, switch, dstIP, outPort ):
			log.infoln("Adding new flow for switch %s to destination %s via port %s\n" % (switch, dstIP, outPort))
			ret = [self.do( 'add-flow ' + switch + ' ip,nw_dst=' + dstIP + ',actions=output:' + str(outPort) )]
			ret.append(self.do( 'add-flow ' + switch + ' arp,nw_dst=' + dstIP + ',actions=output:' + str(outPort) ))
			return ret
	
	
	# Statistics
	class NetworkStatistics:
		def __init__( self, network ):
			self.net = network
		
		def hostReachability( self ):
			n = self.net
			first = n.hosts[0]
			last = n.hosts[len( n.hosts ) - 1]
			return ping( first, last ), ping( last, first )
		#
		def switchReachability( self ):
			n = self.net
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
	

	
	
