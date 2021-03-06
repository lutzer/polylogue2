# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-19 10:45:09
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-23 11:09:19

from __future__ import with_statement
from socketIO_client import SocketIO,BaseNamespace
from threading import Thread
import logging

logger = logging.getLogger(__name__)

class KeyboardSocketSender(Thread):

	def __init__(self,address,port):
		self.socket = SocketIO(address,port)
		self.keyboard_nsp = self.socket.define(BaseNamespace, '/keyboard')
		self.running = True
		Thread.__init__(self)

	def run(self):
		logger.info('started Socket Thread.')
		while (self.running):
			self.socket.wait(seconds=1); #TODO: test if this is ok
		self.socket.disconnect()

	def sendText(self,key):
		self.keyboard_nsp.emit('keypress',dict(key=key, type='text'))

	def sendTextMotion(self,key):
		self.keyboard_nsp.emit('keypress',dict(key=key, type='motion'))

	def stop(self):
		logger.info('stopping Socket Thread.')
		self.running = False


