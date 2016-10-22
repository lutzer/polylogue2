# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 11:30:39
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-22 12:16:15

import pyglet
import sys
import logging
import random

from config import *
from utils.eventHandler import EventHandler

#colors
BG_COLOR = [244, 223, 66, 255]
TEXT_COLOR = [0,0,0,255]
PROMPT_COLOR = [61,61,61,255]

# console params
FONT_FAMILY = "Perfect DOS VGA 437"
FONT_SIZE = 24
LINE_SPACING = 36
TEXT_LENGTH = 140
TEXT_INDENT = "70px"
TEXT_PROMPT = "pl>"

# progress bar params
BAR_HEIGHT = 50
BAR_COLOR = [0, 0, 0, 255]
STROKE_WIDTH = 4

# dialog params
DIALOG_BG_COLOR = [66, 66, 66, 255]
DIALOG_TEXT_COLOR = [255, 255, 255, 255]
DIALOG_PADDING = 100

# layout params
PADDING = 20
MARGIN = 10

logger = logging.getLogger(__name__)

class Rectangle(object):
	'''Draws a rectangle into a batch.'''
	def __init__(self, x1, y1, x2, y2, batch, color, filled=True):

		self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS if filled else pyglet.gl.GL_LINE_LOOP, None,
			('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
			('c4B', color * 4)
		)

class ProgressBar(object):
	def __init__(self, time, x, y, width, height, batch):

		self.width = width;
		self.x = x

		self.box = Rectangle(x, y, 
           x + width, y + height, batch, BAR_COLOR, filled=False)

		self.bar = Rectangle(x, y, 
           x + width/2, y + height, batch, BAR_COLOR, filled=True)

		self.progress = 1.0;

	def setProgress(self,progress):

		self.progress = min(1,max(0,progress))

		self.bar.vertex_list.vertices[2] = int(self.x + self.width * self.progress);
		self.bar.vertex_list.vertices[4] = int(self.x + self.width * self.progress);

class Dialog(object):

	visible = True

	def __init__(self, x1, y1, x2, y2, batch):

		height = y2 - y1
		width = x2 - x1

		self.box = Rectangle(x1, y1, 
           x2, y2, batch, DIALOG_BG_COLOR, filled=True)

		self.text = pyglet.text.Label("Dialog Test", x = x1 + width/2, y = y2 - height/2 , 
			width= width- 2 * MARGIN, anchor_x='center', anchor_y="center",
			font_name=FONT_FAMILY, font_size=FONT_SIZE, color=DIALOG_TEXT_COLOR,
			batch=batch )

	def setText(text):
		self.text.text = text


class Console(object):

	def __init__(self, text, x, y, width, height, batch):

		# load font
		font = pyglet.font.load(FONT_FAMILY, FONT_SIZE)

		self.document = pyglet.text.document.FormattedDocument(text)
		self.document.set_style(0, TEXT_LENGTH, dict(
			font_name= FONT_FAMILY, 
			font_size=FONT_SIZE)
		)
		self.document.set_paragraph_style(0, TEXT_LENGTH, dict(
			line_spacing=str(LINE_SPACING)+"pt",
			wrap=True,
			indent=TEXT_INDENT,
			margin_left=MARGIN,
			margin_right=MARGIN)
		)

		# draw text box
		self.layout = pyglet.text.layout.IncrementalTextLayout(
			self.document, width, height, multiline=True, batch=batch)
		self.layout.x = x
		self.layout.y = y

		# draw prompt
		self.prompt = pyglet.text.Label(TEXT_PROMPT, x = x+MARGIN, y = y + height - LINE_SPACING,
			font_name=FONT_FAMILY, font_size=FONT_SIZE, color=PROMPT_COLOR, anchor_y='center',
			batch=batch )

		# add cursor
		self.caret = pyglet.text.caret.Caret(self.layout)

class BoxScreen(pyglet.window.Window):

	text = None
	textBatch = pyglet.graphics.Batch()
	
	progressBar = None
	barBatch = pyglet.graphics.Batch()

	dialog = None
	dialogBatch = pyglet.graphics.Batch()

	running = True
	isEditable = True

	lockBoxEvent = EventHandler()
	unlockBoxEvent = EventHandler()

	def __init__(self):
		pyglet.window.Window.__init__(self,fullscreen=RUN_IN_FULLSCREEN);

		# load fonts
		if pyglet.font.have_font(FONT_FAMILY):
			font = pyglet.font.load(FONT_FAMILY, FONT_SIZE)

		# display text
		self.textBatch = pyglet.graphics.Batch()
		self.text = Console(' ', PADDING, PADDING + BAR_HEIGHT, width=self.width - 2*PADDING, 
			height=self.height - 2*PADDING - BAR_HEIGHT, batch=self.textBatch)
		
		# display progress bar
		self.progressBar = ProgressBar("Test", PADDING, PADDING, 
			width = self.width - 2*PADDING, height = BAR_HEIGHT, batch=self.barBatch)
		self.progressBar.setProgress(0)

		#setup dialog
		self.dialog = Dialog(DIALOG_PADDING,DIALOG_PADDING + BAR_HEIGHT, 
			self.width - DIALOG_PADDING, self.height - DIALOG_PADDING, batch=self.dialogBatch)
		self.dialog.visible = False

		# focus on text
		self.focus_caret()

		# clear text
		self.text.document.text = ''


	def open(self):
		pyglet.app.run()

	def close(self):
		#pyglet.app.exit()
		self.running = False

	### events
	
	def on_draw(self):
		self.clear()
		pyglet.gl.glClearColor(BG_COLOR[0]/255.0,BG_COLOR[1]/255.0,BG_COLOR[2]/255.0,BG_COLOR[3]/255.0)
		pyglet.gl.glLineWidth(STROKE_WIDTH)
		self.textBatch.draw()
		self.barBatch.draw()
		if self.dialog.visible:
			self.dialogBatch.draw()

	def on_text(self,text):
		if self.isEditable and allowed_char(text) and len(self.text.document.text) < TEXT_LENGTH:
			self.text.caret.on_text(text)

	def on_text_motion(self,motion):
                if self.isEditable:
                        self.text.caret.on_text_motion(motion)

	def focus_caret(self):
		self.text.caret.position = len(self.text.document.text)

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			self.close()
		elif symbol == pyglet.window.key.ENTER:
                        self.lockBox()

	### properties
	
	def triggerEvent(self,data):
		logger.debug('received event: ' + data['event'])
		# handle key events
		if data['event'] == 'keypress':
			if not self.isEditable:
				return
			if data['key'] == 10:
				self.lockBox()
			elif data['type'] == 'text':
				self.dispatch_event('on_text',chr(data['key']))
			else:
				self.dispatch_event('on_text_motion',data['key'])
		elif data['event'] == 'unlock':
			self.unlockBox()
		elif data['event'] == 'dialog':
			self.dialog.setText(data['text'])
			self.dialog.visible = data['show']
			self.isEditable = not data['show']
	
	### methods
	
	def lockBox(self):
		if not self.isEditable:
			return
		question = self.getText()
		self.isEditable = False
		self.progressBar.setProgress(1)
		self.lockBoxEvent.emit(question)
		self.text.caret.visible = False

		#start progress bar
		self.progressBar.setProgress(1)

		# start timer
		def updateProgress(dt,timeout):
			self.progressBar.setProgress(float(timeout)/QUESTION_DURATION)
			if timeout > 0:
				timeout -= dt * 1000
				pyglet.clock.schedule_once(updateProgress, 1, timeout)
			else:
				self.unlockBox()

		updateProgress(1,QUESTION_DURATION) #start timeout

	def unlockBox(self):
		self.isEditable = True
		self.setText('')
		self.progressBar.setProgress(0)
		self.text.caret.visible = True
		self.unlockBoxEvent.emit()

	def getText(self):
		return self.text.document.text

	def setText(self,text):
		self.text.document.text = text


def allowed_char(c):
    return (ord(c) < 128 and ord(c) > 31)

