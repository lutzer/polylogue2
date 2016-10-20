# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 17:42:58
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-20 16:04:27

from threading import Thread,Lock
import logging
import time
import pyglet

from ui.boxScreen import BoxScreen

UPDATE_INTERVAL = 0.05 # 50 fps

logger = logging.getLogger(__name__)

class UiThread(Thread):

	screen = None

	def __init__(self):
		Thread.__init__(self)
		self.screen = BoxScreen()

		self.queue = []
		self.queueLock = Lock()

		self.update()

	def run(self):
		logger.info("started ui thread")
		while self.screen.running:
			self.update()
			time.sleep(UPDATE_INTERVAL)

	def update(self):
		pyglet.clock.tick()
		self.screen.switch_to()

		# read keypresses
		for data in self.queue:
			self.screen.triggerKeypress(data)

		# delete queue
		with self.queueLock:
			self.queue[:] = []

		self.screen.dispatch_events()
		self.screen.dispatch_event('on_draw')
		self.screen.flip()

	def stop(self):
		self.screen.close()

	def triggerKeypress(self,data):
		with self.queueLock:
			self.queue.append(data)