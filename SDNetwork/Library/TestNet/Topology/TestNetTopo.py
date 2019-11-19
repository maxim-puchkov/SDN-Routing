#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetTopo.py
#  Test Network Topologies
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.topo import Topo
from mininet.util import irange
from Link import *


# LinkTopo is a network topology with
#   n:      swtiches
#   k:      hosts per every switch
#   wlinks: link costs from every switch to its
#           directly connected switches
class LinkTopo( Topo ):

	def build( self, n, k, wlinks = {}, **_kwargs ):
		#MARK: - Switches
		## Get switch by index: s(1) = Switch 's1'
		def s( index ):
			return self.switches[index - 1]
		## Create n switches
		def addSwitches():
			return [ self.addSwitch( 's%s' % i )
				for i in irange( 1, n ) ]
		# Create all wlinks between switches (with cost)
		def addSwitchLinks():
			switchLinks = []
			for weightedLink in wlinks:
				(i, j) = weightedLink.nodes
				w = weightedLink.weight
				link = self.addLink( s(i), s(j), weight = w)
				switchLinks.append( link )
			return switchLinks
		
		#MARK: - Hosts
		## Get host by index: h(1) = Host 'h1'
		def h( index ):
			return self.hosts[index - 1]
		## Create (n * k) hosts
		def addHosts():
			h = n * k
			return [ self.addHost( 'h%s' % i )
				for i in irange( 1, h )]
		## Create k wlinks from hosts to every switch (no cost)
		def addHostLinks():
			hostLinks = []
			for i in irange( 1, n ):
				last = i * k
				first = last - k + 1
				for j in irange( first, last ):
					link = self.addLink( s(i), h(j) )
					hostLinks.append( link )
			return hostLinks
		
		# Add all nodes and wlinks
		self.switches = addSwitches()
		self.hosts = addHosts()
		self.links = addSwitchLinks() + addHostLinks()


		# Debug display
		print("Printing links weights for input:")
		print("\t wlinks = "),
		for w in wlinks: print(w.toString())
		self.printLinkCosts( wlinks )
	
	#MARK: - DEBUG
	def printLinkCosts( self, wlinks ):
		print("\n")
		for weightedLink in wlinks:
			(i, j) = weightedLink.nodes
			w = weightedLink.weight
			print("\tCost of link (s%s <-> s%s): %s" % (i, j, w))
		print('\n\n')
