# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 11:15:49
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-20 19:44:00

from __future__ import with_statement
import time
import logging
import sys
import pyglet

from config import *
from comm.keyboardSocketThread import *
from ui.uiThread import UiThread

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
   uiThread.screen.newQuestionEvent += onNewQuestion
   uiThread.screen.unlockBoxEvent += onBoxUnlocked
   uiThread.start()
   
   logger.info('service initialized, starting loop.')

# check the socketThread if there are any new messages received
def loop():
   # after ui thread finishes, stop program
   time.sleep(1)
   #uiThread.join()
   #stop()

def stop():
   global keyboardSocket, uiThread

   uiThread.stop();
   keyboardSocket.stop();
   sys.exit()

def onKeypress(data):
   global uiThread
   data['event'] = 'keypress'
   uiThread.addEvent(data)

def onNewQuestion(question):
   logger.info('Received new question: '+question)

def onBoxUnlocked():
   logger.info('Box unlocked')

def sendToPrinter(message):
   logger.info('Printing message:' + message)

# start main loop
init()
try:
   while True:
      loop()
except KeyboardInterrupt:
   print("# program loop interrupted")
finally:
   stop()