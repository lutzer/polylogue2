# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-22 16:07:52
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-22 21:51:52

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-01-26 16:07:22
# @Last Modified by:   lutz
# @Last Modified time: 2016-02-03 17:32:56

from __future__ import with_statement
from threading import Lock
import logging
from PIL import Image

from Adafruit_Thermal import *
from fontRenderer import *

logger = logging.getLogger(__name__)

FONT_WIDTH = 24
PRINTER_PAPER_WIDTH = 300

class LinePrinter:

	printer = None
	fontRenderer = None

	def __init__(self):

		self.printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
		self.printer.sleep()

		fontRenderer = FontRenderer('../font/cutivemono.png','../font/cutivemono.json',FONT_WIDTH)
                
		self.queue = [] # message queue
		self.queueLock = Lock()

		logger.info("printer initialized")

	# adds message to queue
	def addMessage(self,text):
		job = dict(type="message", text=text)
		with self.queueLock:
			self.queue.append(job)

	# add horizontal line to queue
	def addLine(self):
		job = dict(type="line", text='---')
		with self.queueLock:
			self.queue.append(job)

	# add question text
	def addQuestion(self,text):
		job = dict(type="question", text=text)
		with self.queueLock:
			self.queue.append(job)

	def hasJobs(self):
		return len(self.queue) > 0

	def printNextJob(self):
		with self.queueLock:
			if len(self.queue) > 0:
				job = self.queue.pop(0)
			else:
				return

		logger.info("printing" + str(job))

		self.printer.wake()
		self.__printText(job['text'])
		# if job['type'] == "question":
  #                       self.__printText(job['text'])
  #                       self.printer.feed(3)
  #               else:
  #                       self.printer.setSize('M')
  #                       self.printer.println(job['text'])
                        
		self.printer.sleep()

	def __printText(text):

		columnImg = Image.new("RGB", (PRINTER_PAPER_WIDTH, FONT_WIDTH), (255, 255, 255))

		columnIndex = 0
		for character in enumerate(text):

			columnStart = PRINTER_PAPER_WIDTH - columnWidth * FONT_WIDTH

			if columnStart > 0:
				# add character to column
				symbol = fontRenderer.getCharacterImage(character)
				symbol = symbol.rotate(180, 0, True)
         		symbol = fontRenderer.makeBgWhite(symbol)
				columnImg.paste(symbol, box=(PRINTER_PAPER_WIDTH - columnWidth, 0))
			else:
				# print image
				self.printer.printImage(columnImg)
				# set everything to white
				columnImg = Image.new("RGB", (PRINTER_PAPER_WIDTH, FONT_WIDTH), (255, 255, 255))
				# start new column
				columnIndex = 0



		
