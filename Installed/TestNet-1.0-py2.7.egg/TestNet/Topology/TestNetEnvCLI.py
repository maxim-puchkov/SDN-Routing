#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetEnvCLI.py
#  Test Network Command Line Interface Extension
#
#  Created by mpuchkov on 2019-11-21.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.cli import CLI
from TestNet.Utility import display


class TestNetEnvCLI( CLI ):
	
	def __init__( self, _mininet ):
		CLI.__init__( self, _mininet )
		self.net = _mininet
	
	def do( self, shell ):
		self.mn.controller.cmd( shell )
	
	def do_arpAll( self, _line ):
		display.section("Showing ARP caches of all hosts")
		for h in self.mn.hosts:
			h.cmd( 'arp -a' )
	
	def do_flows( self, _line ):
		display.section("Showing all flows")
		for s in self.mn.switches:
			self.do( 'ovs-ofctl dump-flows %s' % s )
	
	def do_h1h2( self, _line ):
		display.section("Adding test flows to Network 1 (h1 to h2)")
		self.do( 'sudo ovs-ofctl add-flow s1 ip,ip_dst=10.0.0.2,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s1 ip,ip_dst=10.0.0.1,actions=output:4' )
		self.do( 'sudo ovs-ofctl add-flow s2 ip,ip_dst=10.0.0.1,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s2 ip,ip_dst=10.0.0.2,actions=output:3' )
		
		self.do( 'sudo ovs-ofctl add-flow s1 arp,arp_tpa=10.0.0.2,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s1 arp,arp_tpa=10.0.0.1,actions=output:4' )
		self.do( 'sudo ovs-ofctl add-flow s2 arp,arp_tpa=10.0.0.1,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s2 arp,arp_tpa=10.0.0.2,actions=output:3' )
	
	
	
	def do_testFlows1( self, _line ):
		display.section("Adding test flows to Network 1 (h1 to h2)")
		self.do( 'sudo ovs-ofctl add-flow s1 ip_dst=10.0.0.2,arp,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s1 ip_dst=10.0.0.1,arp,actions=output:4' )
		
		self.do( 'sudo ovs-ofctl add-flow s2 ip_dst=10.0.0.4,arp,actions=output:2' )
		self.do( 'sudo ovs-ofctl add-flow s2 ip_dst=10.0.0.1,arp,actions=output:1' )
		self.do( 'sudo ovs-ofctl add-flow s2 ip_dst=10.0.0.2,arp,actions=output:3' )
	
	def do_traffic( self, _line ):
		display.section("Monitoring sent and received packets of all hosts")
		for h in self.mn.hosts:
			h.cmd( 'tcpdump %s' % h.defaultIntf().name )
	
	def do_xterms( self, _line ):
		for h in self.mn.hosts:
			self.do( 'xterm %s' % h )
		for s in self.mn.switches:
			self.do( 'xterm %s' % s )

