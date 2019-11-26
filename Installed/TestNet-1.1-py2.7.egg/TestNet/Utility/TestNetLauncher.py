#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetLauncher.py
#  Test Network Launcher
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.net import Mininet, MininetWithControlNet
from mininet.node import RemoteController
from mininet.link import Link, TCLink
from mininet.cli import CLI
from mininet.clean import Cleanup
from mininet.util import irange
from TestNet.Logger import log


def s(i):
	return 's%s' % i
def h(i):
	return 'h%s' % i

#class TestNet( Mininet ):
#	def __init__( self, topology, controller, ipBase, autoSetMacs, **kwargs ):
#		Mininet.__init__( self, topology, controller, ipBase, autoSetMacs, **kwargs )
#
#	def node( self, name ):
#		return self.nameToNode( name )


# Configure and run preset networks
class TestNetLauncher:
	
	#MARK: Network Start and Stop
	# Build the selected topology and created a network
	def prepareNetwork( self, preset, **kwargs ):
		log.do("Prepare TestNet from %s." % preset)
		topology = preset()
		log.infoln(topology.longDescription())
		network = Mininet(
			topo = topology,
			controller = RemoteController( 'c0',
				ip = '127.0.0.1',
				port = 6653
			),
			ipBase = '10.10.0.0/16',
			autoSetMacs = True,
			**kwargs
		)
		log.infoln("Built TestNet topology from template class %s" % type(topology))
		log.done("Network<id%s> is ready to start." % id(network))
		return network
	
	def reassignAddresses( self, network ):
		log.infoln('Reassigning host IP addresses.')
		for i in irange( 1, len(network.switches) ):
			switch = network.nameToNode[s(i)]
			host = network.nameToNode[h(i)]
			host.setIP( '10.10.%s.%s' % (i, i) )
	
	# Start a Mininet network
	def startNetwork( self, network ):
		log.do("Start Network<id%s>." % id(network))
		network.start()
	
	# Start a Mininet network with CLI
	def startInteractiveNetwork( self, network ):
		log.do("Start Network<id%s> with CLI." % id(network))
		network.start()
		self.enableCommandLineInterface( network )
	
	# Stop an active network
	def stopNetwork( self, network ):
		network.stop()
		log.done("Stopped Network<id%s>." % id(network))
	
	
	#MARK: Network Options
	# CLI
	def enableCommandLineInterface( self, network ):
		CLI( network )
	# NAT
	def enableNetworkAddressTranslation( self, network ):
		log.infoln("Adding and configuring NAT...")
		network.addNAT().configDefault()
		
		
	
