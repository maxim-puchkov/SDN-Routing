#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetDisplay.py
#  Test Network command-line text display
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#


# Text color
class UITextStyle:
	# Regular colors
	class Color:
		black   = '\033[0;30m'
		red     = '\033[0;31m'
		green   = '\033[0;32m'
		yellow  = '\033[93m'
		blue    = '\033[0;34m'
		magenta = '\033[35m'
		cyan    = '\033[0;36m'
		gray    = '\033[0;37m'
		lightred     ='\033[91m'
		lightcyan    = '\033[96m'
		red_bold     = '\033[1;31m'
		magenta_bold = '\033[1;35m'
	class BackgroundColor:
		black		= '\033[40m'
		red			= '\033[41m'
		green		= '\033[42m'
		orange		= '\033[43m'
		blue		= '\033[44m'
		purple		= '\033[45m'
		cyan		= '\033[46m'
		lightgrey	= '\033[47m'
	class Format:
		underline = '\033[0;4m'
		# Reset color to default
		reset = '\033[m'


# Make one colored string
def colorize( _str, color ):
	return ( color + _str + UITextStyle.Format.reset )
# Make each string colored
def colorizeEach( strList, color ):
	ret = [ colorize( _str, color )
		for _str in strList ]
	ret.reverse()
	return ret


# Print colored message and reset color
def printColored( _str, color = UITextStyle.Format.reset ):
	print(color),
	print(_str),
	print(UITextStyle.Format.reset)
def printColoredEach( strList, color ):
	for _str in strList:
		print(color + _str + UITextStyle.Format.reset)



# Colorful title
def displayTitle( content ):
	printColored('< %s >' % content.upper(), UITextStyle.Color.magenta_bold)
# Subtitle
def displaySubtitle( content ):
	printColored(content)
# Body text
def displayText( content , indentLevel = 1 ):
	for _ in range(indentLevel):
		print('\t'),
	print(content)
# Colorful footnote
def displayFootnote( content ):
	printColored(content, UITextStyle.Color.gray)


# Display formatted blocks of text
class TestNetDisplay:
	
	#
	def section( self, content ):
		print('')
		displayTitle(content)
	# Default message
	def message( self, content ):
		printColored(content)
	# Input prompt
	def prompt( self, content ):
		printColored(content, UITextStyle.Color.magenta)
	# Error message
	def error( self, content ):
		printColored(content, UITextStyle.Color.lightred)
	
	# Highlighted block
	def highlight( self, block ):
		line = 0
		for n in range( len(block) ):
			printColored([n + 1, block[n]], UITextStyle.Color.yellow)
			
	
	# Selection menu of available networks
	def networkSelectionMenu( self ):
		# Colorize network names
		nets = colorizeEach(['Tiny Network', 'Small Network', 'Large Network', 'Baby Network'], UITextStyle.Color.lightcyan)
		# Display the menu
		displaySubtitle("Choose one of the network environments:")
		displayText('1. %s (default) - network with 4 switches and 5 links.' % nets.pop())
		displayText('2. %s - network with 6 switches and 10 links.' % nets.pop())
		displayText('3. %s - ...' % nets.pop())
		displayText('4. %s - smallest network with 3 switches, 6 hosts, and 3 links' % nets.pop())
		displayFootnote('(see network diagrams in the project definition)')
	

# Shared TestNet instance
display = TestNetDisplay()
