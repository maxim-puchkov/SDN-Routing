#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#  TestNetDisplay.py
#  Test Network command-line text display
#
#  Created by mpuchkov on 2019-11-16.
#  Copyright © 2019 Maxim Puchkov. All rights reserved.
#

class UITextStyle:
	pass

class Display:
	pass


# Text color
class UITextStyle:
	# Regular colors
	black   = '\033[0;30m'
	red     = '\033[0;31m'
	green   = '\033[0;32m'
	yellow  = '\033[0;33m'
	blue    = '\033[0;34m'
	magenta = '\033[0;35m'
	cyan    = '\033[0;36m'
	gray    = '\033[0;37m'
	# Bold colors
	red_bold     = '\033[1;31m'
	magenta_bold = '\033[1;35m'
	# Other styles
	underline = '\033[0;4m'
	# Reset color to default
	reset = '\033[m'

# Make one colored string
def colorize( str, color ):
	return ( color + str + UITextStyle.reset )
# Make each string colored
def colorizeEach( strList, color ):
	ret = [ colorize( str, color )
		for str in strList ]
	ret.reverse()
	return ret

# Print colored message and reset color
def printColored( content, color ):
	print(color + content + UITextStyle.reset)


# Colorful title
def displayTitle( content ):
	printColored('< %s >' % content.upper(), UITextStyle.magenta_bold)
# Subtitle
def displaySubtitle( content ):
	print(content)
# Body text
def displayText( content , indentLevel = 1 ):
	for _ in range(indentLevel):
		print('\t'),
	print(content)
# Colorful footnote
def displayFootnote( content ):
	printColored(content, UITextStyle.gray)


# Display formatted blocks of text
class TestNetDisplay:
	
	# Default message
	def message( self, content ):
		print(content)
	# Input prompt
	def prompt( self, content ):
		printColored(content, UITextStyle.magenta)
	def error( self, content ):
		printColored(content, UITextStyle.red)
	
	# Selection menu of available networks
	def networkSelectionMenu( self ):
		# Colorize network names
		nets = colorizeEach(['Tiny Network', 'Small Network', 'Large Network'], UITextStyle.cyan)
		# Display the menu
		displayTitle("Select Network")
		displaySubtitle("Choose one of the three network environments:")
		displayText('1. %s (default) - network with 4 switches and 5 links.' % nets.pop())
		displayText('2. %s - network with 6 switches and 10 links.' % nets.pop())
		displayText('3. %s - ...' % nets.pop())
		displayFootnote('(see network diagrams in the project definition)')


display = TestNetDisplay()
