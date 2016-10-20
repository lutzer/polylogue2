# -*- coding: utf-8 -*-
# @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
# @Date:   2016-10-19 10:24:06
# @Last Modified by:   lutzer
# @Last Modified time: 2016-10-19 10:30:09

class EventHandler(object):

	def __init__(self):
		self.__handlers = []

	def __del__(self):
		self.__handlers = [h for h in self._handlers if getattr(h, 'im_self', False) != obj]

	def __iadd__(self, handler):
		self.__handlers.append(handler)
		return self

	def __isub__(self, handler):
		self.__handlers.remove(handler)
		return self

	def emit(self, *args, **keywargs):
		for handler in self.__handlers:
			handler(*args, **keywargs)