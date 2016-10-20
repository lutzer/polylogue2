# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 11:15:49
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-20 10:03:40

from __future__ import with_statement
import time
import logging
import sys
import pyglet

from comm.keyboardSocketThread import *
from ui.uiThread import UiThread

KEYBOARD_SOCKET_URL = "localhost"
KEYBOARD_SOCKET_PORT = 8091

WEBSERVER_SOCKET_URL = ""
WEBSERVER_SOCKET_PORT = 8090

keyboardSocket = None
uiThread = None

# Debug options
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init():
   global keyboardSocket, uiThread

   # start socket connection to keyboard
   keyboardSocket = KeyboardSocketThread(KEYBOARD_SOCKET_URL,KEYBOARD_SOCKET_PORT)
   keyboardSocket.start()
   keyboardSocket.keypressEvent += onKeypress

   # start socket connection to webserver
   
   # setup display
   uiThread = UiThread()
   uiThread.start()
   
   logger.info('service initialized, starting loop.')

# check the socketThread if there are any new messages received
def loop():
   time.sleep(1)

def stop():
   logger.info('stopping main application')
   global keyboardSocket, uiThread
   uiThread.stop();
   keyboardSocket.stop();
   sys.exit()

def onKeypress(data):
   global uiThread

   if data['key'] == "\r":
       print "return pressed"
   elif data['type'] == 'motion':
      uiThread.screen.moveCursor(data['key'])
   else:
      uiThread.screen.write(data['key'])

def sendToPrinter(message):
   logger.info('Printing message:' + message)

def receivedQuestion(question):
	logger.info('Received question:' + question)

# start main loop
init()
try:
   while True:
      loop()
except KeyboardInterrupt:
   print("# program loop interrupted")
finally:
   stop()