from World import *

class Player:
	
	def __init__(self, position = 0):
		self.area = position
		self.inventory = []
		self.play = True
		
	def start_game(self):
		self.getarea().enter_area()
	
	def look_around(self):
		print self.getarea().describe()
		
	def go(self, direction):
		next_area = self.getarea().go(direction)
		if next_area:
			self.area = next_area
			
	def list_inventory(self):
		inv = "You are carrying: "
		if (len(self.inventory)) == 0:
			inv = "Your bag is empty."
		
		else:
			for object in self.inventory:
				inv += "\n	" + object.info()
		
		return inv
		
	def inventory_add(self, object):
		if len(self.inventory) >= inventory_limit:
			print "Your inventory is full!"
			return False
		
		else:
			self.inventory.append(object)
			print "Picked up", object.name + "."
			return True
	
	def remove_item(self, object):
		for o in range(len(self.inventory)):
			if self.inventory[o].name == object.name:
				self.inventory.pop(o)
				return
	
	def find_object(self, name):
		for object in self.inventory:
			if object.is_a(name):
				return object
		
		return False

	def getarea(self):
		return World.areas[self.area]