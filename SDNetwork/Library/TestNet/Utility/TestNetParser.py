#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetParser.py
#  Test Network input Parser
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from Logger import log
import sys


# Read script input
class TestNetParser:
	# Maximum number of arguments = 2
	def __init__( self ):
		self._maxArgc = 2
	# Input is valid if 2 arguments are provided (string '*/TestNet*.py' and a number)
	def validate( self, argv ):
		argc = len(argv)
		return ( argc == self._maxArgc )
	
	# Get argument
	## Get by argument index (noexcept)
	def safeGet( self, argv, argIndex, convertor = None ):
		try:
			arg = argv[argIndex]
			if not (convertor is None):
				arg = convertor(arg)
			return arg
		except Exception:
			return ''
	## Name of the executable
	def getFilename( self, argv ):
		return self.safeGet( argv, 0 )
	## Preset index
	def getIndex( self, argv ):
		return int(self.safeGet( argv, 1 ))
	## List of all arguments (noexcept)
	def getAll( self, argv ):
		# Get filename
		name = self.getFilename( argv )
		if ( self.validate( len(argv) ) ):
			# Get index if input is valid
			index = self.getIndex( argv )
			ret = (name, index)
		else:
			# Otherwise, use default preset index 0
			log.infoln("Warning: invalid index. Setting index to default (0).")
			return ( name, 0 )
		# Log and return both arguments
		return ( name, index )
	
	# Get all input arguments
	def parseInput( self ):
		log.DO("Parse input arguments.")
		argv = sys.argv
		(name, index) = self.getAll( argv )
		log.DONE("Parsed arguments: \n\tname = %s, \n\tpreset index = %s" % (name, index))
		return (name, index)
	
	# Wait for additional input
	def waitForInput( self ):
		try:
			return input()
		except Exception:
			return 0
	

# Shared TestNet instance
parser = TestNetParser()
