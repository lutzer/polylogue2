# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-18 11:15:49
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-25 00:31:53

from __future__ import with_statement
import time
import logging
import sys
import pyglet

from config import *
from comm.keyboardSocketThread import *
from comm.serverSocketThread import *
from ui.uiThread import UiThread
from printer.linePrinter import LinePrinter

keyboardSocket = None
serverSocket = None
uiThread = None
linePrinter = None

currentQuestion = ""

print sys.path[0]

# Debug options
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init():
   global keyboardSocket, uiThread, serverSocket, linePrinter

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

   try:
      linePrinter = LinePrinter(PRINTER_DISABLED)
   except Exception as err:
      logger.error("Could not start printer: " + str(err))
      stop()

   logger.info('starting ui thread')
   # setup display
   uiThread = UiThread()
   uiThread.screen.lockBoxEvent += onBoxLock
   uiThread.screen.unlockBoxEvent += onBoxUnlocked
   uiThread.start()
   
   logger.info('service initialized, starting loop.')

# check the socketThread if there are any new messages received and print them
def loop():
   global linePrinter
   
   if linePrinter.hasJobs():
      linePrinter.printNextJob()
   else:
      time.sleep(1)

def stop():
   global keyboardSocket, uiThread, serverSocket
   if uiThread:
      uiThread.stop();
   if keyboardSocket:
      keyboardSocket.stop();
   if serverSocket:
      serverSocket.stop();
   sys.exit()

### Box events

def onKeypress(data):
   global uiThread
   data['event'] = 'keypress'
   uiThread.addEvent(data)

def onBoxUnlocked():
   global serverSocket,currentQuestion, linePrinter

   logger.info('Box unlocked')
   serverSocket.sendQuestionExpired(BOX_ID)
   keyboardSocket.sendAvailable(True);
   linePrinter.addQuestion(currentQuestion)
   linePrinter.addLine()
   linePrinter.feed(6)

def onBoxLock(question):
   global serverSocket, currentQuestion, linePrinter

   logger.info('Received new question: '+question)
   currentQuestion = question

   serverSocket.sendNewQuestion(BOX_ID,question)
   keyboardSocket.sendAvailable(False);
   linePrinter.addLine()

### Socket events

def onNewMessageReceived(data):
   global linePrinter
   logger.info('received new message: ' + str(data))
   if data['boxId'] == BOX_ID:
      linePrinter.addMessage(data['message'])

### start main loop
init()
try:
   while True:
      loop()
except KeyboardInterrupt:
   print("# program loop interrupted")
finally:
   stop()
