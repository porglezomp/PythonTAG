#!/usr/bin/env python
import cPickle

class World:
	play = True
	strings = []
	
	@classmethod	
	def load(world, filename):
		if len(filename) > 0:
			tobeloaded = open(filename, 'r')
			data = cPickle.load(tobeloaded)
			world.player = data[0]
			world.areas = []
			for item in data[1]:
				world.areas.append(item.area)
			return data
		return False
		
	@classmethod
	def save(world, data, filename):
		save = open(filename, 'w')
		cPickle.dump(data, save)
		save.close()
		print "saved", filename