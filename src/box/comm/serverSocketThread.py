# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 11:21:32
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-21 14:41:46

from __future__ import with_statement
from socketIO_client import SocketIO,BaseNamespace
from threading import Thread
import logging

from utils.eventHandler import EventHandler
from config import *

logger = logging.getLogger(__name__)

class ServerSocketThread(Thread):

	messageReceivedEvent = EventHandler()

	def __init__(self,address,port):
		
		self.socket = SocketIO(address,port)
		self.box_namespace = self.socket.define(BaseNamespace, '/box')
		self.box_namespace.on('message:new',self.messageReceivedEvent.emit)
		Thread.__init__(self)

	def run(self):
		logger.info('started Socket Thread.')
		self.running = True
		while (self.running):
			self.socket.wait(seconds=1); #TODO: test if this is ok
		self.socket.disconnect()

	def stop(self):
		logger.info('stopping Socket Thread.')
		self.running = False

	def sendNewQuestion(self,boxId,question):
		data = dict(boxId=boxId, question=question, duration=QUESTION_DURATION)
		self.box_namespace.emit('question:new', data)

	def sendQuestionExpired(self,boxId):
		data = dict(boxId=boxId)
		self.box_namespace.emit('question:expired', data)
