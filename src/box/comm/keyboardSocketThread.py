# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 11:21:32
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-19 23:55:39

from __future__ import with_statement
from socketIO_client import SocketIO
from threading import Thread
from utils.eventHandler import EventHandler
import logging

logger = logging.getLogger(__name__)

class KeyboardSocketThread(Thread):

	keypressEvent = EventHandler()

	def __init__(self,address,port):
		self.socket = SocketIO(address,port)
		self.socket.on('keypress', self.keypressEvent.emit)
		Thread.__init__(self)

	def run(self):
		logger.info('started Socket Thread.')
		self.running = True
		while (self.running):
			self.socket.wait(seconds=1); #TODO: test if this is ok
		self.socket.disconnect()

	def stop(self):
		logger.info('stopping Socket Thread.')
		del self.keypressEvent
		self.running = False
