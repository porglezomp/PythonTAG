#!/usr/bin/env python
from Player import *
import string
from World import *

class Command:
	commands = {"look around" : "look_around", "go" : "go", "inventory" : "examine_inventory",
				"pick up" : "take", "take" : "take", "grab" : "take", "drop" : "drop", 
				"i want" : "respond", "i wanna" : "respond", "say" : "say", "stab" : "stab", "quit" : "quit"}
	
	def __init__(self, player):
		self.player = player
		
	def command(self, input):
		for comm in self.commands.keys():
			#if the input is at least as long as the command you are testing for
			if len(input) >= len(comm):
				#check if the beginning is the same as the command name
				if input[:len(comm)] == comm:
					#run the command
					self.base = input[:len(comm)]
					function = getattr(Command, self.commands[comm])
					function(self, string.lstrip(input[len(comm):]))
					return
		
		if not self.parse(input):
			print "I don't understand the command '" + input + "'"
					
	def look_around(self, input):
		self.player.look_around()
	
	def go(self, direction):
		self.player.go(direction)
		
	def examine_inventory(self, input):
		print self.player.list_inventory()
		
	def take(self, itemName):		
		#look for the object in the scene
		item = self.player.getarea().find_object(itemName)
		#if the object exists
		if item:
			#if it is possible to add it to your inventory, do so
			if self.player.inventory_add(item):
				#remove the item from the area
				self.player.getarea().remove_item(item)
		
		else:
			print "There's no", itemName, "here!"
	
	def drop(self, itemName):
		#look for the object in the inventory
		item = self.player.find_object(itemName)
		#if the object exists
		if item:
			print "You drop the", item.name + "."
			self.player.remove_item(item)
			self.player.getarea().add_item(item)
		
		else:
			print "You aren't carrying a", itemName + "!"
			
	def respond(self, comment):
		responses = {"i want" : "Too bad.", "i wanna" : "Too bad"}
		print responses[self.base]
		
	def say(self, speech):
		print "You say:", speech
	
	def stab(self, item):
		#check for item in area
		in_area = self.player.getarea().find_object(item)
		#if object is in area
		if in_area:
			if in_area.can_stab:
				print "You stabbed the", item
			
			else:
				print "Why would you stab a", item + "?"
		else:
			print "What", item + "?"
	
	def damage(self, item):
		print "Damaging is not supported."
	
	def quit(self, input):
		positive = ["y", "yes"]
		quit_state = string.lower(raw_input("Are you sure you want to quit? (y/n): "))
		if quit_state in positive:
			World.play = False
			print "Goodbye!"
			
	def parse(self, input):
		commstrings = {"north" : "go", "south" : "go", "east" : "go", "west" : "go", "in" : "go",
		"out" : "go", "up" : "go", "down" : "go"}
		if input in commstrings:
			function = getattr(Command, commstrings[input])
			function(self, input)
			return True