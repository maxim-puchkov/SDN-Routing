#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetBundle.py
#  Test Network Bundle
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from Logger import log
from Presets import selector
from Utility import parser, launcher

# old main file






if __name__ == '__main__':

	# Log info messages
	log.setLogLevel( 'info' )
	
	# 1. Read input and get selected preset network
	( name, index ) = parser.parseInput()
#	preset = selector.getPreset( index )
	
	
	launcher.test()
	
	
	# 2. Prepare Mininet network instance and start it
#	net = launcher.prepareNetwork( preset )
#	launcher.startNetwork( net )


