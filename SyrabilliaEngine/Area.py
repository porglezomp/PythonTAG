#!/usr/bin/env python
from Object import *
from World import *

class Area:
	
	def __init__(self, north = None, east = None, south = None, west = None, up = None,
										down = None, enterance = None, exit = None, objects = [],
										description = "You are in a boring white room. Blah blah blah.",
										name = "Room", enterable = True) :
		
		self.neighbor = {}
		self.neighbor["north"] = north
		self.neighbor["east"] = east
		self.neighbor["south"] = south
		self.neighbor["west"] = west
		self.neighbor["up"] = up
		self.neighbor["down"] = down
		self.neighbor["in"] = enterance
		self.neighbor["out"] = exit
		self.description = description
		self.objects = []
		self.name = name
		self.has_been_visited = False
		self.enterable = enterable
		
	def set_neighbor(self, direction, area):
		if direction in self.neighbor:
			self.neighbor[direction] = area
			
	def set_name(self, name):
		self.name = name
	
	def add_item(self, object):
		self.objects.append(object)
	
	def describe(self):
		description = self.description
		for object in self.objects:
			description += " " + object.describe()
		
		return description
		
	def enter_area(self):
		if self.has_been_visited:
			print self.name
		
		else:
			self.has_been_visited = True
			print self.name
			print self.describe()
	
	def go(self, direction):
		if direction in self.neighbor:
			try: next_area = World.areas[self.neighbor[direction]]
			except: next_area = None
			
		else:
			print direction , "is not a real direction."
			return False
		
		if (next_area):
			if (next_area.enterable):
				next_area.enter_area()
				return self.neighbor[direction]
		
			else:
				next_area.describe()
				return False
		else:
			print "You can't go that way."
			return False
			
	def find_object(self, name):
		for object in self.objects:
			if object.is_a(name):
				return object
		
		return False
		
	def remove_item(self, item):
		for o in range(len(self.objects)):
			if self.objects[o].name == item.name:
				self.objects.pop(o)