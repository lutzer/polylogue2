# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-22 16:07:52
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-24 23:14:59

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-01-26 16:07:22
# @Last Modified by:   lutz
# @Last Modified time: 2016-02-03 17:32:56

from __future__ import with_statement
from threading import Lock
import logging
from PIL import Image,ImageChops
import sys

from Adafruit_Thermal import *
from fontRenderer import *

logger = logging.getLogger(__name__)

PRINTER_PAPER_WIDTH = 384

class LinePrinter:

	printer = None
	fontRenderer = None
	fontRendererBig = None

	def __init__(self,disablePrinter=False):

		self.printerDisabled = disablePrinter

		if not self.printerDisabled:
			self.printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
			self.printer.sleep()

		currentDir = sys.path[0]
		self.fontRenderer = FontRenderer(currentDir +'/font/cutivemono32bold.png', currentDir + '/font/cutivemono32bold.json')
		self.fontRendererBig = FontRenderer(currentDir +'/font/cutivemono42bold.png', currentDir + '/font/cutivemono42bold.json')
        
                
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

		self.wake();
		
		if job['type'] == "question":
			self.printText(job['text'],fontRendererBig)
			self.feed(6)
		elif job['type'] == "line":
			self.printText("---=---",center=True)
			self.feed(3)
		else:
			self.printText(job['text'])
			self.feed(3)

		self.sleep();

                        

	def printText(self,text,font=False,center=False):
		if not font:
			font = self.fontRenderer

		fontHeight = font.fontHeight

		# holds all the images of the columns
		columns = []

		column = Image.new("RGB", (PRINTER_PAPER_WIDTH, fontHeight), (255, 255, 255))
		startX = PRINTER_PAPER_WIDTH # start from right
		for character in text:

			#first create character
			symbol = font.getCharacterImage(character)
			symbol = symbol.rotate(180, 0, True)
			symbol = font.makeBgWhite(symbol)

			charWidth = symbol.size[0]
			startX -= charWidth
			if startX > 0:
				# add character to column
				column.paste(symbol, box=(startX, 0))
			else:
				# prepend to columns array
				columns.insert(0,column)

				# start new column
				column = Image.new("RGB", (PRINTER_PAPER_WIDTH, fontHeight), (255, 255, 255))

				# add character
				startX = PRINTER_PAPER_WIDTH - charWidth
				column.paste(symbol, box=(startX, 0))

		if center:
			# shift column to the  left
			column = ImageChops.offset(column,-startX/2,0)

		#insert last column
		columns.insert(0,column)

		# print all the columns
		for img in columns:
			self.__printImage(img)

	def wake(self):
		if not self.printerDisabled:
			self.printer.wake()

	def sleep(self):
		if not self.printerDisabled:
			self.printer.sleep()

	def feed(self,amount):
		if not self.printerDisabled:
			self.printer.feed(amount)

	def __printImage(self,img):
		if not self.printerDisabled:
			self.printer.printImage(img,LaaT=False);
		else:
			img.show()




		
