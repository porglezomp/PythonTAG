#!/usr/bin/env python
import cPickle

class World:
	play = True
	
	@classmethod	
	def load(world, filename):
		if len(filename) > 0:
			tobeloaded = open(filename, 'r')
			data = cPickle.load(tobeloaded)
			world.player = data[0]
			world.areas = data[1]
			return data
		return False
		
	@classmethod
	def save(world, data, filename):
		save = open(filename, 'w')
		cPickle.dump(data, save)
		save.close()
		print "saved", filename