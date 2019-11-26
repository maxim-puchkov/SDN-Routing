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
from random import randint

from mininet.topo import Topo
from mininet.util import irange
from TestNet.Topology import wlink, wlinks



class SuperTopo( Topo ):
	displayName = '< Super >'
	info = '< SuperClass >'
	
	def build( self, n, k, *_args, **_kwargs ):
		Topo.build( self, _args, _kwargs )
		self.n = n
		self.k = k
	
	# Description
	def shortDescription( self ):
		return self.info
	def longDescription( self ):
		return (( 'Topology Name: %s.\n' % self.displayName ) +
			( 'Total number of switches: %s\n' % self.nSwitches() ) +
			( '                   hosts: %s\n' % self.nHosts() ) +
			( '  switch-to-switch links: %s (each link has a weight)\n' % len(self._slinks) ) +
			(  '    switch-to-host links: %s (no weights)\n' % len(self._hlinks) ))
	
	# Number of
	def nHosts( self ):
		return len( self.hosts() )
	def nSwitches( self ):
		return len( self.switches() )
	def nLinks( self ):
		return len(self._slinks) + len(self._hlinks)
	
	
	#MARK: - DEBUG
	# Link input at start
	def printLinkInput( self, _wlinks ):
		print('Printing links weights for input:')
		for w in _wlinks:
			print('\t' + w.toString())
		self.printLinkCosts( _wlinks )
	# Created links at end
	def printLinkCosts( self, _wlinks ):
		print('\n')
		for weightedLink in _wlinks:
			(i, j) = weightedLink.nodes
			w = weightedLink.weight
			print('\tCost of link (s%s <-> s%s): %s' % (i, j, w))
		print('\n\n')
	def debugLinks( self, _wlinks ):
		self.printLinkInput( _wlinks )
		self.printLinkCosts( _hlinks )






# Debug topo
class SubnetTopo( SuperTopo ):
	_addrBase = '100.100'
	_addrPrefixLen = 24
	
	def build( self, n, k, _wlinks, *_args, **_kwargs ):
		
		def s( index ):
			return self.switches()[index - 1]
		def h( index ):
			return self.hosts()[index - 1]
		
		def addNodes():
			for i in irange( 1, n ):
				s_i = self.addSwitch( 's%s' % i )
				for j in irange( 1, k ):
					h_j = self.addHost( 'h%s' % (i + j - 1) )
		
		
		def addSwitchLinks():
			for weightedLink in _wlinks:
				(i, j) = weightedLink.nodes
				w = weightedLink.weight
				self._slinks.append( self.addLink( s(i), s(j), key = (i, j, w)) )
		
		def addHostLinks():
			for i in irange( 1, n ):
				last = i * k
				first = last - k + 1
				for j in irange( first, last ):
					self._hlinks.append( self.addLink( s(i), h(j), key = ( i, j, 0 ) ) )
		
		SuperTopo.build( self, n, k, _args, _kwargs )
		self._hlinks = []
		self._slinks = []
		self.linkWeights = _wlinks
		addNodes()
		addSwitchLinks()
		addHostLinks()
			# return [ [ ( self.addSwitch( 's%s' % i ), self.addHost( 'h%s' % i ) ) ]
				#for i range( 1, n ) ]
		



#MARK: - -  Link Topo Class  - -

# LinkTopo is a network topology with
#   n:      swtiches
#   k:      _hosts per every switch
#  _wlinks: weighted links from every switch to its
#           directly connected switches
class LinkTopo( SuperTopo ):
	displayName = 'LinkTopo'
	info = '<BaseClass>'
	problemLink = ('s1', 's2')
	
	def build( self, n, k, _wlinks, *_args, **_kwargs ):
		#MARK: - Switches
		## Create n switches
		def addSwitches():
			return [ self.addSwitch( 's%s' % i )
				for i in irange( 1, n ) ]
		## Get switch by index: s(1) = <Switch s1>
		def s( index ):
			return self.switches()[index - 1]
		# Create all slinks between switches ((with cost)
		def addSwitchLinks():
			switchLinks = []
			for weightedLink in _wlinks:
				(i, j) = weightedLink.nodes
				w = weightedLink.weight
				switchLinks.append( self.addLink(s(i), s(j), key = (i, j, w)) )
			return switchLinks
		
		#MARK: - Hosts
		## Create (n * k) _hosts
		def addHosts():
			h = n * k
			return [ self.addHost( 'h%s' % i )
				for i in irange( 1, h ) ]
		## Get host by index: h(1) = <Host h1>
		def h( index ):
			return self.hosts()[index - 1]
		## Create k _wlinks from _hosts to every switch (no cost)
		def addHostLinks():
			hostLinks = []
			for i in irange( 1, n ):
				last = i * k
				first = last - k + 1
				for j in irange( first, last ):
					hostLinks.append( self.addLink( s(i), h(j), key = ( i, j, 0 ) ) )
			return hostLinks
		
		
		# Add all nodes and links
		SuperTopo.build( self, n, k, _args, _kwargs )
		addSwitches()
		self._slinks = addSwitchLinks()
		
		addHosts()
		self._hlinks = addHostLinks()
		




#MARK: - Custom Topology Presets
# The smallest topology with 3 switches
# (assignment 2 question 1)X
class BabyTopo( LinkTopo ):
	displayName = 'Baby Topology'
	info = 'very small network with 3 switches and 3 links'
	
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
	info = 'simple network with 4 switches and 5 links'
	
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
	info = 'a network with 6 switches and 10 links'
	
	def build( self ):
		switches = 6
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 2), ((1, 3), 5), ((1, 4), 1),
			((2, 3), 3), ((2, 4), 2),
			((3, 4), 3), ((3, 5), 1), ((3, 6), 5),
			((4, 5), 1),
			((5, 6), 2)
		)
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )



# Large Topology (Example Network 3)
#
# Link costs:
#	randomized
class LargeTopo( LinkTopo ):
	displayName = 'Large Topology'
	info = 'network of 16 connected switches (debug)'
	
	def build( self ):
		switches = 16
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 1), ((1, 11), 2), ((1, 10), 1),((10,9),1),((10,16),3),((10,7),1),((9,7),2),((7,16),2),((7,8),2),((4,5),100),((4,12),100),
			((7,3),1),((16,8),2),((16,15),1),((7,4),1),((1,7),3),((10,11),1),((11,2),1),((2,4),6),((6,3),4),((11,12),4),
			((12,5),3),((12,14),4),((14,13),1),((2,14),1),((14,3),1),((15,14),1),
			((15,8),1),((15,4),1),((8,4),1),((4,3),1),((5,13),1),((13,4),2))
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )


class MassiveTopo( LinkTopo ):
	displayName = 'Massive Topology'
	info = '200 switches and 1000 links, on average (debug)'
	
	def build( self ):
		switches = randint(175, 225)
		srange = irange(1, switches)
		hostsPerSwitch = 1
		try:
			linkWeights = []
			for s in srange:
				for eCount in irange(1, randint(1, 10)):
					e = randint(1, switches)
					w = randint(1, 15)
					link = wlink((s, e), w)
					linkWeights.append(link)
			LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )
		except:
			print('Unable to construct')


class TestTopo( LinkTopo ):
	displayName = 'Test Topology'
	
	def build( self ):
		switches = 3
		hostsPerSwitch = 1
		linkWeights = wlinks(
			((1, 2), 1), ((1, 11), 2), ((1, 10), 1),((10,9),1),((10,16),3),((10,7),1),((9,7),2),((7,16),2),((7,8),2),
			((7,3),1),((16,8),2),((16,15),1),((7,4),1),((1,7),3),((10,11),1),((11,2),1),((2,4),6),((6,3),4),((11,12),4),
			((12,5),3),((12,14),4),((14,13),1),((2,14),1),((14,3),1),((15,14),1),
			((15,8),1),((15,4),1),((8,4),1),((4,3),1),((5,13),1),((13,4),2))
		LinkTopo.build( self, switches, hostsPerSwitch, linkWeights )


# Allows the file to be imported using `mn --custom <filename> --topo minimal`
topos = {
    'baby': BabyTopo,
    'tiny': TinyTopo,
    'small': SmallTopo,
    'large': LargeTopo,
    'massive': MassiveTopo,
    'test': TestTopo
}
