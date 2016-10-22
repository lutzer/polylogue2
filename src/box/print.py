# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-22 16:20:38
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-22 16:24:58

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-01-21 14:58:30
# @Last Modified by:   lutz
# @Last Modified time: 2016-01-25 19:41:16

# This script sends a message to the adafruit thermal printer.
# It prints the message vertically on the paper roll.

#!/usr/bin/python

from printer.Adafruit_Thermal import *

PRINTER_WIDTH_PIXELS = 384 # in pixels

# read arguments
def main(argv):
   try:
      opts, args = getopt.getopt(argv,"m:",["message="])
   except getopt.GetoptError:
      print 'polylogue.py -m <message>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'polylogue.py -m <message>'
         sys.exit()
      if opt in ("-m", "--message"):
         sendToPrinter(arg)

# prints message on printer
def sendToPrinter(message):

   print 'Printing message:', message

   printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
   printer.wake()

   printer.println(message)
   
   printer.feed(3)

   printer.sleep()

   print 'done.'

if __name__ == "__main__":
   main(sys.argv[1:])