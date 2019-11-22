#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetLauncher.py
#  Test Network Launcher
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController, NOX
from mininet.clean import Cleanup
from mininet.link import TCLink
from TestNet.Topology import *
from TestNet.Logger import log


# Configure and run preset networks
class TestNetLauncher:
	
	def __init__( self ):
		self.allPresetTopologies = ( TinyTopo, SmallTopo, LargeTopo )
	
	# test
	def test( self, *args ):
		log.infoln("TEST")
		return args
	
	#MARK: Network Start and Stop
	# Build the selected topology and created a network
	def prepareNetwork( self, preset, **kwargs ):
		log.do("Prepare TestNet.")
		topo = preset()
		network = Mininet(
			topo,
			controller = RemoteController( 'c0', ip = '127.0.0.1', port = 6653, xterms = True ),
#			link = TCLink,
			autoSetMacs = True,
			**kwargs
		)
		log.infoln("Built TestNet topology from template class %s" % type(topo))
		log.done("Network<id%s> is ready to start." % id(network))
		return network
	
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
		
		
	
