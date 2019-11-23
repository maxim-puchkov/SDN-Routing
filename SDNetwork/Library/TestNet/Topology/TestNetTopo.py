#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetTopo.py
#  Test Network Topologies
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

import itertools

from mininet.topo import Topo
from mininet.util import irange
from TestNetRawLink import wlinks


# LinkTopo is a network topology with
#   n:      swtiches
#   k:      _hosts per every switch
#  _wlinks: weighted links from every switch to its
#           directly connected switches
class LinkTopo( Topo ):
	displayName = 'LinkTopo'
	info = '<BaseClass>'
	
	def build( self, n, k, _wlinks = {}, **_kwargs ):
		#MARK: - Switches
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
		
		#MARK: - Hosts
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
					link = self.addLink( s(i), h(j), key = ( i, j, 0 ) )
					hostLinks.append( link )
			return hostLinks
			
		
		# Add all nodes and _wlinks
		self._switches = add_switches()
		self._hosts = add_hosts()
		self._slinks = addSwitchLinks() # switch links
		self._hlinks = addHostLinks() # host links
		# Debug display
		# self.debugLinks( _wlinks )
	
	
	def nHosts( self ):
		return len( self._hosts )
	def nSwitches( self ):
		return len( self._switches )
	def nLinks( self ):
		return ( len(self._slinks), len(self._hlinks) )
	
	def shortDescription( self ):
		return self.info
	def longDescription( self ):
		return (( 'Topology Name: %s. - %s.\n' % ( self.displayName, self.info ) ) +
			( 'Total number of switches: %s\n' % self.nSwitches() ) +
			( '                   hosts: %s\n' % self.nHosts() ) +
			(('  switch-to-switch links: %s (each link has a weight)\n' +
			  '    switch-to-host links: %s (no weights)\n') % self.nLinks() ))
	
	
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





def nodeGroup(n, iterable, fillvalue=None):
	args = [iter(iterable)] * n
	return itertools.izip_longest(*args, fillvalue=fillvalue)

#MARK: - Custom Topology Presets
# The smallest topology with 3 switches
# (assignment 2 question 1)X
class BabyTopo( LinkTopo ):
	displayName = 'Baby Topo'
	problemLink = ('s1', 's2')
	info = 'very small network with 3 switches and 3 links'
#	exampleProblemLink = (
	
	def build( self ):
		switches = 3
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 1), ((1, 3), 1),
			((2, 3), 5)
		)


		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )



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
	problemLink = ('s1', 's2')
	info = 'simple network with 4 switches and 5 links in-between them'
	
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
	problemLink = ('s1', 's2')
	info = 'a network with 6 switches and 10 links'
	
	def build( self ):
		_switches = 6
		hostsPerSwitch = 1
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
	problemLink = ('s1', 's2')
	info = ''
	
	def build( self ):
		switches = 3
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 1), ((1, 3), 1), ((2, 3), 1)
		)
		LinkTopo.build( self, _switches, hostsPerSwitch, linkWeights )



class TestTopo( LinkTopo ):
	displayName = 'Test Topology'
	problemLink = ('s1', 's2')
	
	def build( self ):
		switches = 3
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 1), ((1, 11), 2), ((1, 10), 1),((10,9),1),((10,16),3),((10,7),1),((9,7),2),((7,16),2),((7,8),2),
			((7,3),1),((16,8),2),((16,15),1),((7,4),1),((1,7),3),((10,11),1),((11,2),1),((2,4),6),((6,3),4),((11,12),4),
			((12,5),3),((12,14),4),((14,13),1),((2,14),1),((14,3),1),((15,14),1),
			((15,8),1),((15,4),1),((8,4),1),((4,3),1),((5,13),1),((13,4),2))
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )
