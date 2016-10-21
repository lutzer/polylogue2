# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 11:15:49
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-21 15:27:13

from __future__ import with_statement
import time
import logging
import sys
import pyglet

from config import *
from comm.keyboardSocketThread import *
from comm.serverSocketThread import *
from ui.uiThread import UiThread

keyboardSocket = None
serverSocket = None
uiThread = None

# Debug options
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init():
   global keyboardSocket, uiThread, serverSocket

   # start socket connection to keyboard
   logger.info('connection to keyboard socket on '+ KEYBOARD_SOCKET_URL)
   keyboardSocket = KeyboardSocketThread(KEYBOARD_SOCKET_URL,KEYBOARD_SOCKET_PORT)
   keyboardSocket.keypressEvent += onKeypress
   keyboardSocket.start()

   # start socket connection to webserver
   logger.info('connection to webserer socket on '+ WEBSERVER_SOCKET_URL)
   serverSocket = ServerSocketThread(WEBSERVER_SOCKET_URL,WEBSERVER_SOCKET_PORT)
   serverSocket.messageReceivedEvent += onNewMessageReceived
   serverSocket.start()

   logger.info('starting ui thread')
   # setup display
   uiThread = UiThread()
   uiThread.screen.lockBoxEvent += onBoxLock
   uiThread.screen.unlockBoxEvent += onBoxUnlocked
   uiThread.start()
   
   logger.info('service initialized, starting loop.')

# check the socketThread if there are any new messages received
def loop():
   time.sleep(1)

def stop():
   global keyboardSocket, uiThread, serverSocket

   uiThread.stop();
   keyboardSocket.stop();
   serverSocket.stop();
   sys.exit()

### Box events

def onKeypress(data):
   global uiThread
   data['event'] = 'keypress'
   uiThread.addEvent(data)

def onBoxUnlocked():
   global serverSocket

   logger.info('Box unlocked')
   serverSocket.sendQuestionExpired(BOX_ID)

def onBoxLock(question):
   global serverSocket

   logger.info('Received new question: '+question)
   serverSocket.sendNewQuestion(BOX_ID,question)

### Socket events


def onNewMessageReceived(data):
   logger.info('received new message: ' + str(data))
   if data['boxId'] == BOX_ID:
      logger.info("printing message: " + str(data['message']))


# start main loop
init()
try:
   while True:
      loop()
except KeyboardInterrupt:
   print("# program loop interrupted")
finally:
   stop()