# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 11:30:39
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-20 11:25:42

import pyglet
import sys
import logging
import random

#colors
BG_COLOR = (244, 223, 66, 255)
TEXT_COLOR = (0,0,0,255)
PROMPT_COLOR = (61,61,61,255)

# console params
FONT_FAMILY = "Perfect DOS VGA 437"
FONT_SIZE = 24
LINE_SPACING = 36
TEXT_LENGTH = 500
TEXT_INDENT = "75px"
TEXT_PROMPT = "pl>"

# progress bar params
BAR_HEIGHT = 50
BAR_COLOR = [0, 0, 0, 255]
STROKE_WIDTH = 3

# layout params
PADDING = 20

logger = logging.getLogger(__name__)

class Rectangle(object):
	'''Draws a rectangle into a batch.'''
	def __init__(self, x1, y1, x2, y2, batch, filled=True):

		self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS if filled else pyglet.gl.GL_LINE_LOOP, None,
			('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
			('c4B', BAR_COLOR * 4)
		)

class ProgressBar(object):
	def __init__(self, time, x, y, width, height, batch):

		self.width = width;
		self.x = x

		self.box = Rectangle(x, y, 
           x + width, y + height, batch, False)

		self.bar = Rectangle(x, y, 
           x + width/2, y + height, batch, True)

		self.progress = 1.0;

	def setProgress(self,progress):

		self.progress = min(1,max(0,progress))

		self.bar.vertex_list.vertices[2] = int(self.x + self.width * self.progress);
		self.bar.vertex_list.vertices[4] = int(self.x + self.width * self.progress);



class Console(object):
    def __init__(self, text, x, y, width, height, batch):

        self.document = pyglet.text.document.FormattedDocument(text)
        self.document.set_style(0, TEXT_LENGTH, dict(
        	font_name= FONT_FAMILY, 
        	font_size=FONT_SIZE)
        )
        self.document.set_paragraph_style(0, TEXT_LENGTH, dict(
        	line_spacing=str(LINE_SPACING)+"pt",
        	wrap=True,
        	indent=TEXT_INDENT
        ))

        # draw text box
        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=True, batch=batch)
        self.layout.x = x
        self.layout.y = y

        # draw prompt
        self.prompt = pyglet.text.Label(TEXT_PROMPT, x = x, y = y + height - LINE_SPACING,
        	font_name=FONT_FAMILY, font_size=FONT_SIZE, color=PROMPT_COLOR, anchor_y='center',
        	batch=batch )

        # add cursor
        self.caret = pyglet.text.caret.Caret(self.layout)

class BoxScreen(pyglet.window.Window):

	text = None
	progressBar = None
	textBatch = pyglet.graphics.Batch()
	barBatch = pyglet.graphics.Batch()
	running = True

	def __init__(self):
		pyglet.window.Window.__init__(self);

		# load fonts
		if pyglet.font.have_font(FONT_FAMILY):
			font = pyglet.font.load(FONT_FAMILY, FONT_SIZE)

		# display text
		self.textBatch = pyglet.graphics.Batch()
		self.text = Console(list_allowed_chars(), PADDING, PADDING + BAR_HEIGHT, width=self.width - 2*PADDING, 
			height=self.height - 2*PADDING - BAR_HEIGHT, batch=self.textBatch)
		
		# display progress bar
		self.progressBar = ProgressBar("Test", PADDING, PADDING, 
			width = self.width - 2*PADDING, height = BAR_HEIGHT, batch=self.barBatch)
		self.progressBar.setProgress(0)
		# focus on text
		self.focus_caret()


	def open(self):
		pyglet.app.run()
		self.text.document.text = " "

	def close(self):
		pyglet.app.exit()
		self.running = False

	def on_draw(self):
		self.clear()
		pyglet.gl.glClearColor(BG_COLOR[0]/255.0,BG_COLOR[1]/255.0,BG_COLOR[2]/255.0,BG_COLOR[3]/255.0)
		pyglet.gl.glLineWidth(STROKE_WIDTH)
		self.textBatch.draw()
		self.barBatch.draw()

	def focus_caret(self):
		self.text.caret.position = len(self.text.document.text)

	def write(self, char):
		if allowed_char(char) and len(self.text.document.text) < TEXT_LENGTH:
			self.text.document.text += char
			#self.text.caret.on_text(char)

	def moveCursor(self,motion):
		self.text.caret.on_text_motion(motion)

	### properties
	
	def getText(self):
		return self.text.document.text

	def setText(self,text):
		self.text.document.text = text

	def getProgress(self):
		return self.progressBar.progress

	def setProgress(self,progress):
		self.progressBar.setProgress(progress)

def allowed_char(c):
    return (ord(c) < 128 and ord(c) > 31)

def list_allowed_chars():
	string = ""
	for i in range(0,256):
		if allowed_char(unichr(i)):
			string += unichr(i)
	return string

