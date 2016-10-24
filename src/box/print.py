# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-22 16:20:38
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-24 18:34:27

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-01-21 14:58:30
# @Last Modified by:   lutz
# @Last Modified time: 2016-01-25 19:41:16

# This script sends a message to the adafruit thermal printer.

#!/usr/bin/python2

from printer.linePrinter import LinePrinter
import sys,getopt
from config import *

PRINTER_WIDTH_PIXELS = 384 # in pixels

# read arguments
def main(argv):
   try:
      opts, args = getopt.getopt(argv,"m:",["message="])
   except getopt.GetoptError:
      print 'print.py -m <message>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'print.py -m <message>'
         sys.exit()
      if opt in ("-m", "--message"):
         sendToPrinter(arg)

# prints message on printer
def sendToPrinter(message):

   print 'Printing message:', message

   printer = LinePrinter(PRINTER_DISABLED)

   printer.wake()
   printer.printText(message,center=True)
   printer.feed(5)
   printer.sleep()
   print 'done.'

if __name__ == "__main__":
   main(sys.argv[1:])
