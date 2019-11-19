#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetLauncher.py
#  Test Network Launcher
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.net import MininetWithControlNet
from mininet.cli import CLI
from Logger import log


# Configure and run preset networks
class TestNetLauncher:
	# test
	def test( self, *args ):
		log.infoln("TEST")
		return args
	
	# Build a preset network and add NAT
	def prepareNetwork( self, preset, **kwargs ):
		log.DO("Prepare TestNet.")
		topo = preset()
		network = MininetWithControlNet( topo, **kwargs )
		log.infoln("Built TestNet topology from template class %s" % type(topo))
		network.addNAT().configDefault()
		log.infoln("Added and configured NAT.")
		log.DONE("Network<id%s> is ready to start." % id(network))
		return network
	
	# Run a Mininet network with CLI
	def startNetwork( self, network ):
		log.DO("Start Network<id%s>." % id(network))
		network.start()
		CLI( network )
		network.stop()
		log.DONE("Stopped Network<id%s>." % id(network))


# Shared TestNet instance
launcher = TestNetLauncher()
