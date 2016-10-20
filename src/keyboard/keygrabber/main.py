# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-20 23:45:27
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-21 01:28:29

import curses
import logging

from comm.keyboardSocketSender import KeyboardSocketSender

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8091

#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)

running = True
stdscr = None
socket = None

def init():
	global stdscr, socket

	logging.info('started keygrabber')

	# start socket
	socket = KeyboardSocketSender(SERVER_ADDRESS,SERVER_PORT)
	socket.start()

	#init the curses screen
	stdscr = curses.initscr()
	# turn of echo
	curses.noecho()
	# do not require enter 
	curses.cbreak()
	# enable arrow keys
	stdscr.keypad(1) 

def stop():
	global stdscr, socket

	logging.info('stopped keygrabber')
	# listening and revert console
	curses.nocbreak()
	stdscr.keypad(0) 
	curses.echo()
	curses.endwin()

	socket.stop()

def loop():
	global stdscr, running, socket

	c = stdscr.getch()
	# output key press

	if c == 27: # escape key, quit program
		running = False
	elif c == curses.KEY_LEFT:
		onKeypress(65361,motion=True)
	elif c == curses.KEY_RIGHT:
		onKeypress(65363,motion=True)
	elif c == curses.KEY_UP:
		onKeypress(65362,motion=True)
	elif c == curses.KEY_DOWN:
		onKeypress(65364,motion=True)
	elif c == 127 or c == 330:
		onKeypress(65288,motion=True)
	else:
		onKeypress(c)

def onKeypress(key,motion=False):
	global socket
	
	printKey(key)

	if motion:
		socket.sendTextMotion(key)
	else:	
		socket.sendText(key)

def printKey(string):
	stdscr.addstr(0, 0, '                           ')
	stdscr.addstr(0, 0, 'key pressed: ' + str(string))

try:
	init()
	while running:
		loop()
except KeyboardInterrupt:
   print("# program loop interrupted")
finally:
   stop()