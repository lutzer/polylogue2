# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-19 10:45:09
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-20 08:56:37

import logging
import pyglet
import time
import sys

from comm.keyboardSocketSender import KeyboardSocketSender

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# params
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8091

# global vars
socket = None
window = None

class Window(pyglet.window.Window):

	def __init__(self):
		pyglet.window.Window.__init__(self);
		pyglet.app.run()

	def stop(self):
		pyglet.app.exit()

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			self.stop()

	def on_text(self, text):
		onKeypress(text)

	def on_text_motion(self, motion):
		onKeypress(motion,motion=True)

def init():
	global socket, window
	logger.info("starting service")

	# start socket
	socket = KeyboardSocketSender(SERVER_ADDRESS,SERVER_PORT)
	socket.start()

	# start window for keylistener
	window = Window()

def stop():
	global socket, window
	logger.info("stopping service")
	window.stop()
	socket.stop()
	sys.exit(0)

def loop():

	# stop program when reaching loop
	stop()

def onKeypress(key,motion=False):
	global socket
	if motion:
		socket.sendTextMotion(key)
	else:	
		socket.sendText(key)

init()
try:
	while True:
		loop()
except KeyboardInterrupt:
   print("# program loop interrupted")
finally:
   stop()