#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetEnvCLI.py
#  Test Network Command Line Interface Extension
#
#  Created by mpuchkov on 2019-11-21.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from subprocess import Popen, PIPE

from mininet.cli import CLI
from mininet.term import makeTerms, runX11
from mininet.util import irange

from TestNet.Logger import log
from TestNet.Utility import UITextStyle, colorizeEach, display, get_routing_decision, get_route_cost


# Check if route directly connects two switches
def isDirect( route ):
	return (len(route) == 2)
# Add purple background for indirect routes
def brightLabel( text ):
	return (UITextStyle.BackgroundColor.purple + str(text) + UITextStyle.Format.reset)

def __wait__( *commandList ):
	steps = len(commandList)
	for i in range( steps ):
		commandList[i]('')
		display.prompt('\n\nPress <Return> to continue (%s/%s)' %(i + 1, steps))
		try:
			x = input('')
		except:
			x = ''


class TestNetEnvCLI( CLI ):
	
	prompt = 'TestNet> '
	
	def __init__( self, _mininet, _env ):
		self.env = _env
		self.net = _mininet
		CLI.__init__( self, _mininet )

	
	# Tell the controller to do a command
	def do( self, shell, quiet = False ):
		if (quiet):
			return self.mn.controller.cmd( shell )
		return self.mn.controller.cmdPrint( shell )
	def doPrint( self, shell ):
		display.cmdHighlight( True )
		self.mn.controller.cmdPrint( shell )
		display.cmdHighlight( False )
	

	
	def do_all( self, _ ):
		__wait__(
			# Show ip
			self.do_ips,
			# Routing commands
			self.do_weights, self.do_costs, self.do_routes, self.do_paths,
			# Flow commands
			self.do_flows, self.do_stats
		)
	
	# Show object info
	#   info [node1, node2, ...]
	def do_info( self, line ):
		locals = self.getLocals()
		_nodes = line.split()
		display.section("All functions")
		if not (_nodes):
			_nodes = self.mn.keys()
		for n in _nodes:
			if not (locals.__contains__(n)):
				break
			obj = locals[n]
			display.subsection('%s (%s)' % (n, obj.IP()))
			print(dir(obj))
	
	
	# Show IP addresses
	#   ips
	def do_ips( self, _ ):
		display.section("IP Addresses")
		locals = self.getLocals()
		def showIP( *keys ):
			for key in keys:
				display.message('%s\t%s' % ( key.name, key.IP() ))
		def showAll( *keys ):
			for key in keys:
				display.message('%s\t%s\t%s' % ( key.name, key.IP(), key.MAC() ))
		# For each node
		display.subsection('Controllers')
		for c in self.mn.controllers:
			showIP( locals[c.name] )
		display.subsection('Switches')
		for s in self.mn.switches:
			showIP( locals[s.name] )
		display.subsection('Hosts')
		for h in self.mn.hosts:
			showAll( locals[h.name] )
	
	
	#MARK: - Routing Tests
	
	# Show link weights
	#   weights
	def do_weights( self, _ ):
		display.section("Weights")
		log.infoln('Link\t\tWeight')
		log.infoln('--------------------')
		for (i, j, w) in self.mn.topo._slinks:
			log.infoln('{s%s, s%s}\t%s' % (i, j, w))
	
	# Show costs of reaching every other switch
	#   costs
	def do_costs( self, _ ):
		# Algorithm input
		switches = self.mn.topo.switches()
		weights = [ ( 's'+str(i[0]), 's'+str(i[1]), i[2] )
			for i in self.mn.topo._slinks ]
		# Print cost of reaching 'end' switch from 'start' switch
		display.section("Total path costs")
		print('From\\To'), ('\t'.join(switches))
		for start in switches:
			print(start + '\t'),
			for end in switches:
				if (start == end):
					print('--\t'),
					continue
				route = get_routing_decision( start, weights, end )
				cost = get_route_cost( [route] )
				if ( isDirect(route) ):
					# Print result for directly connected switches
					print( cost ),
				else:
					# Print and highlight routes with intermediate switches
					print( brightLabel(cost) ),
				print('\t'),
			print('')
	
	
	#MARK: routes
	# Show least-cost paths from every switch to every other switch
	def do_routes( self, _ ):
		# Algorithm input
		switches = self.mn.topo.switches()
		weights = [ ( 's'+str(i[0]), 's'+str(i[1]), i[2] )
			for i in self.mn.topo._slinks ]
		# Print next hop switch
		display.section("First-Hop with lowest cost")
		print('From\\To\t'), ('\t'.join(switches))
		for start in switches:
			print(start + '\t'),
			for end in switches:
				if (start == end):
					print('--\t'),
					continue
				route = get_routing_decision( start, weights, end )
				if ( isDirect(route) ):
					# Print result for directly connected switches
					print( end ),
				else:
					# Print and highlight routes with intermediate switches
					print( brightLabel(route[1]) ),
				print('\t'),
			print('')
	
	
	#MARK: paths
	# Show the complete shortest path from one switch to every other switch
	def do_paths( self, line ):
		# Algorithm input
		switches = self.mn.topo.switches()
		weights = [ ( 's'+str(i[0]), 's'+str(i[1]), i[2] )
			for i in self.mn.topo._slinks ]
		# Least cost paths to every node
		display.section("Least-cost paths to other nodes")
		display.message('From -> To\tCost\t\tFull Shortest Path')
		for start in switches:
			display.subsection('%s' % start)
			for end in switches:
				if (start == end):
					continue
				route = get_routing_decision( start, weights, end )
				cost = get_route_cost( [route] )
				display.message('%s   -> %s\t%s\t\t%s' % (start, end, cost, route))
	
	
	# Run commands on every node
	#MARK: arp
	def do_arps( self, _line ):
		display.section("ARP caches of all hosts")
		sh = 'arp -a'
		for h in self.mn.hosts:
			h.cmdPrint( sh )
	
	#MARK: route
	def do_netstats( self, _line ):
		display.section("Routing Tables")
		sh = 'netstat -rn'
		display.subsection('Hosts')
		for h in self.mn.hosts:
			h.cmdPrint( sh )
		display.subsection('Controller')
		self.doPrint( sh )
	
	#MARK: ifconfig
	def do_ifconfigs( self, _line ):
		display.section("Showing Interface Configuration")
		sh = 'ifconfig -a'
		display.subsection('Hosts')
		for h in self.mn.hosts:
			h.cmdPrint( sh )
		display.subsection('Controller')
		self.doPrint( sh )
	
	#MARK: ovs-ofctl
	## View
	def do_flows( self, _line ):
		display.section("Showing all flows of all OVSSwitches")
		for s in self.mn.switches:
			self.doPrint( 'sudo ovs-ofctl dump-flows %s' % s )
	## Delete
	def do_deleteFlows( self, _line ):
		display.section("Deleting all flows of all OVSSwitches")
		for s in self.mn.switches:
			self.doPrint( 'sudo ovs-ofctl del-flows %s' % s )
	
	# Display flow statistics
	def do_stats( self, _ ):
		display.section("OpenFlow: Sent/Received Packets")
		display.message('Packets passing through a switch on the way host with IP address = "nw_dst"')
		for s in self.mn.switches:
			display.subsection('%s - Traffic' % s.name)
			self.doPrint( 'sudo ovs-ofctl dump-flows %s | grep -e "n_packets=[1-9]*.*n_bytes=[1-9]*.*nw_dst=10.10.[1-9].[1-9]" -To' % (s.name) )
	
	
	def do_xxx_testFlows1( self, _line ):
		display.section("Adding test flows to Tiny Network")
		self.do( 'sudo ovs-ofctl add-flow s1 ip,ip_dst=10.0.0.2,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s1 ip,ip_dst=10.0.0.1,actions=output:4' )
		self.do( 'sudo ovs-ofctl add-flow s2 ip,ip_dst=10.0.0.1,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s2 ip,ip_dst=10.0.0.2,actions=output:3' )
		
		self.do( 'sudo ovs-ofctl add-flow s1 arp,arp_tpa=10.0.0.2,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s1 arp,arp_tpa=10.0.0.1,actions=output:4' )
		self.do( 'sudo ovs-ofctl add-flow s2 arp,arp_tpa=10.0.0.1,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s2 arp,arp_tpa=10.0.0.2,actions=output:3' )
	
	def do_xxx_traffic( self, _line ):
#		display.section("Monitoring sent and received packets of all hosts")
		for h in self.mn.hosts:
			h.cmdPrint( 'tcpdump -i %s' % h.defaultIntf().name )
	
	def do_xxx_xterms( self, _line ):
		locals = self.getLocals()
		terms = makeTerms( [ locals[name]
			for name in [ 'h1', 'h2', 's1', 's2' ] ] )
		self.mn.terms += terms
	
	
	def do_xxx_sharks( self, line ):
		display.section("Launching Wireshark")
		sh = 'sudo wireshark &'
		
		locals = self.getLocals()
		_nodes = line.split()
		if not (_nodes):
			_nodes = self.mn.keys()
		for n in _nodes:
			if not (locals.__contains__(n)):
				break
			obj = locals[n]
			obj.cmdPrint( sh )
