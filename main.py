#!/usr/bin/env python

from SyrabilliaEngine import *
import string
import cPickle
import tkMessageBox
from Tkinter import *
import tkFileDialog

inventory_limit = 15
RUN_MODE = "edit" #edit or game
GAME_INFO = """0
Syribillia engine V.0.3 by Caleb Jones
Adventure: The Temple of Naru
"""

if RUN_MODE == "game":
	root = Tk()
	root.withdraw()
	filename = tkFileDialog.askopenfilename(title = "Load Adventure:", parent = root)
	if (World.load(filename)):
		
		print GAME_INFO
		World.player.start_game()	
		comm = Command(World.player)
		while World.play:
			input = string.lower(raw_input("\n> "))
			comm.command(input)

elif RUN_MODE == "edit":
	root = Tk()
	editor = Editor(root)
	root.protocol("WM_DELETE_WINDOW", editor.done_editing_game)
	root.lift()
	while editor.play:
		root.update()