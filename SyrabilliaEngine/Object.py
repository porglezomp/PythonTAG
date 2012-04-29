#!/usr/bin/env python

class Object:
	
	def __init__(self, description = "A thing is lying on the ground.", name = "something", can_stab = False):
		self.description = description
		self.name = name
		self.nicknames = [self.name]
		self.can_stab = can_stab
		
	def describe(self):
		return self.description
		
	def info(self):
		return self.name
		
	def is_a(self, thing):
		#if the name is one of the object's names, return true
		if thing in self.nicknames:
			return True
		
		else:
			return False
			
	def add_name(self, name):
		if name not in self.nicknames:
			self.nicknames.append(name)