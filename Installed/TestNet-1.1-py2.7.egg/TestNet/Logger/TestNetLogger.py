#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetLog.py
#  Test Network Logging
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

from mininet.log import lg as mnLog


# Logger formats and displays log messages
class TestNetLogger:
	def __init__( self ):
		self.setLogLevel( 'info' )
	def setLogLevel( self, level = 'info' ):
		mnLog.setLogLevel( level )
	
	# Log runtime error messages
	def __error__( self, content, pre, post ):
		mnLog.error(pre + content + post)
	# Default error log format
	def error( self, content, pre = '>> Error: ', post = '' ):
		self.__error__(content, pre, post)
	# Error log with new line
	def errorln( self, content, pre = '>> Error: ', post = '' ):
		self.__error__(content, pre, (post + '\n'))
	
	# Log informative messages
	def __info__( self, content, pre, post ):
		mnLog.info(pre + content + post)
	# Default info log format
	def info( self, content, pre = '> ', post = '' ):
		self.__info__(content, pre, post)
	# Info log with new line
	def infoln( self, content, pre = '> ', post = '' ):
		self.__info__(content, pre, (post + '\n'))
	
	# Default info log format
	def debug( self, content, pre = '> ', post = '' ):
		mnLog.debug(content, pre, post)
	# Info log with new line
	def debugln( self, content, pre = '> ', post = '' ):
		mnLog.debug(content, pre, (post + '\n'))
	
	# Special log '>> DO:' to log the beggining of a procedure
	def do( self, content ):
		self.__info__(content, '>> DO: ', '\n')
	# Special log '>> DONE:' to log the end of a procedure
	def done( self, content ):
		self.__info__(content, '>> DONE: ', '\n')
	# Special log '>> OK:' to log successful results
	def ok( self, content ):
		self.__info__(content, '>> OK: ', '\n')
	

# Shared TestNet instance
#   Usage: log.info("message")
log = TestNetLogger()
