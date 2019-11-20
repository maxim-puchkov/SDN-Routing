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
#   k:      _hosts per every switch
#   _wlinks: link costs from every switch to its
#           directly connected _switches
class LinkTopo( Topo ):

	def build( self, n, k, _wlinks = {}, **_kwargs ):
		#MARK: - _switches
		## Get switch by index: s(1) = Switch 's1'
		def s( index ):
			return self._switches[index - 1]
		## Create n _switches
		def add_switches():
			return [ self.addSwitch( 's%s' % i )
				for i in irange( 1, n ) ]
		# Create all _wlinks between _switches (with cost)
		def addSwitchLinks():
			switchLinks = []
			for weightedLink in _wlinks:
				(i, j) = weightedLink.nodes
				w = weightedLink.weight
				link = self.addLink( s(i), s(j), loss = (w - 1) )
				print(link)
				switchLinks.append( link )
			return switchLinks
		
		#MARK: - _hosts
		## Get host by index: h(1) = Host 'h1'
		def h( index ):
			return self._hosts[index - 1]
		## Create (n * k) _hosts
		def add_hosts():
			h = n * k
			return [ self.addHost( 'h%s' % i )
				for i in irange( 1, h )]
		## Create k _wlinks from _hosts to every switch (no cost)
		def addHostLinks():
			hostLinks = []
			for i in irange( 1, n ):
				last = i * k
				first = last - k + 1
				for j in irange( first, last ):
					link = self.addLink( s(i), h(j) )
					print(link)
					hostLinks.append( link )
			return hostLinks
		
		# Add all nodes and _wlinks
		self._switches = add_switches()
		self._hosts = add_hosts()
		self._slinks = addSwitchLinks()
		self._hlinks = addHostLinks()


		# Debug display
		print("Printing links weights for input:")
		print("\t _wlinks = "),
		for w in _wlinks: print(w.toString())
		self.printLinkCosts( _wlinks )
	
	#MARK: - DEBUG
	def printLinkCosts( self, _wlinks ):
		print("\n")
		for weightedLink in _wlinks:
			(i, j) = weightedLink.nodes
			w = weightedLink.weight
			print("\tCost of link (s%s <-> s%s): %s" % (i, j, w))
		print('\n\n')
