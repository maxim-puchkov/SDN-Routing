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
from TestNetRawLink import *


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
				link = self.addLink( s(i), s(j), key = ( i, j, w ) )
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
		## Create k _wlinks from _hosts to every switch (no cost)h1
		def addHostLinks():
			hostLinks = []
			for i in irange( 1, n ):
				last = i * k
				first = last - k + 1
				for j in irange( first, last ):
					link = self.addLink( s(i), h(j), key = ( i, j ) )
					hostLinks.append( link )
			return hostLinks
		
		# Add all nodes and _wlinks
		self._switches = add_switches()
		self._hosts = add_hosts()
		self._slinks = addSwitchLinks() # switch links
		self._hlinks = addHostLinks() # host links


		# Debug display
		# self.debugLinks( _wlinks )
	
	
	#MARK: - DEBUG
	# Link input at start
	def printLinkInput( self, _wlinks ):
		print("Printing links weights for input:")
		print("\t _wlinks = "),
		for w in _wlinks:
			print('\t' + w.toString())
		self.printLinkCosts( _wlinks )
	# Created links at end
	def printLinkCosts( self, _wlinks ):
		print("\n")
		for weightedLink in _wlinks:
			(i, j) = weightedLink.nodes
			w = weightedLink.weight
			print("\tCost of link (s%s <-> s%s): %s" % (i, j, w))
		print('\n\n')
	
	def debugLinks( self, _wlinks ):
		self.printLinkInput( _wlinks )
		self.printLinkCosts( _wlinks )




#MARK: - Custom Topology Presets 
# Tiny Topology (Example Network 1)
# Network with 4 switches, with 5 bidirectional links.
#
# One-directional links (10):
#   s1 <-> (s2, s3, s4)
#   s2 <-> (s1, s4)
#   s3 <-> (s1, s4)
#   s4 <-> (s1, s2, s3)
#
# Link costs:
#   s1-s2:  2
#   s1-s3:  1
#   s1-s4:  2
#   s2-s4:  3
#   s3-s4:  3
class TinyTopo( LinkTopo ):
	displayName = 'Tiny Topology'
	
	def build( self ):
		switches = 4
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 2), ((1, 3), 1), ((1, 4), 2),
			((2, 4), 3),
			((3, 4), 3)
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )


# Small Topology (Example Network 2)
class SmallTopo( LinkTopo ):
	displayName = 'Small Topology'
	
	def build( self ):
		_switches = 6
		hostsPerSwitch = 2
		linkWeights = wlinks(
			((1, 2), 2), ((1, 3), 5), ((1, 4), 1),
			((2, 3), 3), ((2, 4), 2),
			((3, 4), 3), ((3, 5), 1), ((3, 6), 5),
			((4, 5), 1),
			((5, 6), 2)
		)
		LinkTopo.build( self, _switches, hostsPerSwitch, linkWeights )


# Large Topology (Example Network 3)
#
# Link costs:
#	randomized
class LargeTopo( LinkTopo ):
	displayName = 'Large Topology'
	
	def build( self ):
		_switches = 0 #!
		hostsPerSwitch = 0 #!
		linkWeights = () #!
		LinkTopo.build( self, _switches, hostsPerSwitch, linkWeights )


class TestTopo( LinkTopo ):
	displayName = 'Tiny Topology'
	
	def build( self ):
		switches = 3
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 1), ((1, 3), 1), ((2, 3), 1)
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )
