#!/usr/bin/env python

from Area import *
from Tkinter import *
import tkFileDialog
import tkMessageBox
from Player import *
import string

class Editor:
	
	def __init__(self, root):
		self.play = True
		self.root = root
		self.connecting = False
		self.areas = []
		self.tool = Tool(self)
		self.selection = None
		self.init_GUI()
		self.player = Player()
		
	def init_GUI(self):
		self.root.geometry(str(900) + "x" + str(600))
		self.root.minsize(width = 600, height = 400)
		self.root.title("World Editor")
		self.palette = Frame(master = self.root, width = 200, height = 600, bg = "dark grey")
		self.palette.pack(side = RIGHT, fill = Y)
		self.palette.grid_propagate(False)
		self.canvas = Canvas(master = self.root, width = 700, height = 600, bg = "black")
		self.canvas.pack(side = LEFT, fill = BOTH, expand = 1)
		Button(self.palette, text = "Load", command = self.load).grid(row = 0, columnspan = 3, sticky = W)
		Button(self.palette, text = "Save", command = self.save).grid(row = 0, column = 3, sticky = W)
		Button(self.palette, text = "Add Area", command = lambda: self.tool_enable("add_area")).grid(row = 1, columnspan = 5, sticky = W)
		Button(self.palette, text = "Select", command = lambda: self.tool_enable("select")).grid(row = 2, columnspan = 3, sticky = W)
		Button(self.palette, text = "Connect Areas", command = lambda: self.tool_enable("connect")).grid(row = 3, columnspan = 6, sticky = W)
		self.canvas.bind("<Button-1>", self.click)
		self.canvas.bind("<B1-Motion>", self.mouse_move)
		self.canvas.bind("<ButtonRelease-1>", self.unclick)
		self.areas.append(Box(self.canvas, 100, 100))
		self.areas.append(Box(self.canvas, 500, 500))
		self.areas.append(Box(self.canvas, 500, 0))
		String(self.canvas, self.areas[0], self.areas[1])
		self.title = Entry(self.palette)
		self.title.grid(row = 7, column = 0, columnspan = 8, sticky = W)
		self.description = Text(self.palette, height = 8, width = 25)
		self.description.grid(row = 8, columnspan = 8, rowspan = 4, sticky = W)
			
	def set_pp(self):
		if self.editing == False or self.editing == "set_player":
			self.editing = "set_player"
		
		else:
			tkMessageBox.showwarning("Hey!", "Close the Area Editor before setting the player position.")
	
	def save(self):
		filename = string.split(tkFileDialog.asksaveasfilename(title = "Save Adventure:", parent = self.root), ".")[0]
		saveareas = []
		for item in self.areas:
			saveareas.append(Box(item.parent, item.x, item.y, width = item.width, height = item.height,
								forsave = True, area = item.area))
		
		savestrings = []
		for savestring in World.strings:
			savestrings.append(String(savestring.parent, savestring.a, savestring.b, forsave = True))
		
		if len(filename) > 0:
			print "saving..."
			World.save([self.player, saveareas], filename  + ".ta")
			#World.save([self.player, saveareas, savestrings], filename  + ".ta")
			return True
	
	def load(self):
		filename = tkFileDialog.askopenfilename(title = "Load Adventure:", parent = self.root)
		data = World.load(filename)
		self.player = data[0]
		self.areas = []
		for item in data[1]:
			self.areas.append(Box(self.canvas, item.x, item.y, width = item.width,
								height = item.height, area = item.area))
		
		if data[2]:
			for string in data[2]:
				String(self.canvas, string.a, string.b)
		
		
		#old areaedit code
# 			if (self.editing == False) and (self.editing != "set_player"):
# 			self.editing = area_num
# 			self.areaEditor = Toplevel()
# 			self.areaEditor.protocol("WM_DELETE_WINDOW", self.done_editing_area)
# 			self.areaEditor.title("Area Editor for #" + str(area_num))
# 			self.title = Entry(self.areaEditor, width = 52)
# 			self.title.grid(row = 0, column = 0, columnspan = 5, sticky = W)
# 			self.describe = Text(self.areaEditor, relief = SUNKEN, width = 52, height = 6)
# 			self.describe.grid(row = 1, column = 0, rowspan = 5, columnspan = 5, sticky = W)
# 			self.donebutton = Button(self.areaEditor, text = "Edit Connections", command = self.edit_connections).grid(row = 5, column = 6, sticky = W)
# 			self.donebutton = Button(self.areaEditor, text = "Done", command = self.done_editing_area).grid(row = 6, column = 6, sticky = W)
# 			self.title.insert(END, self.areas[area_num].name)
# 			self.describe.insert(END, self.areas[area_num].description)	
# 		
# 		elif self.editing == "set_player":
# 			self.player.area = area_num
# 			self.editing = False
# 		
# 		else:
# 			tkMessageBox.showwarning("Hey!", "You are already editing area #" + str(self.editing) + "!")

	def edit_area(self):
		self.title.delete(0, END)
		self.description.delete("0.0", END)
		self.title.insert(END, self.areas[self.selection].area.name)
		self.description.insert(END, self.areas[self.selection].area.description)
		
	def done_editing_area(self):
		self.areas[self.selection].area.set_name(string.rstrip(self.title.get()))
 		self.areas[self.selection].area.description = string.rstrip(self.description.get(1.0, END))
	
	def edit_connections(self):
		if self.connecting == False:
			self.current_direction = "north"
			self.connecting = self.editing
			self.connectionEditor = Toplevel()
			self.connectionEditor.protocol("WM_DELETE_WINDOW", self.done_editing_connections)
			self.connectionEditor.title("Connection Editor")
			self.connection_buttons = []
			for b in range(self.area_count):
				if b != self.editing:
					self.connection_buttons.append(Button(self.connectionEditor, command = lambda i = b:
													self.connect_to(i)).grid(row = (b - b%self.grid_width) / 
													self.grid_height, column = b%self.grid_width)) 
			
			Button(self.connectionEditor, text = "North", command = lambda : self.set_direction("north")).grid(row = 0, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "East", command = lambda : self.set_direction("east")).grid(row = 1, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "South", command = lambda : self.set_direction("south")).grid(row = 2, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "West", command = lambda : self.set_direction("west")).grid(row = 3, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "Up", command = lambda : self.set_direction("up")).grid(row = 4, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "Down", command = lambda : self.set_direction("down")).grid(row = 5, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "In", command = lambda : self.set_direction("in")).grid(row = 6, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "Out", command = lambda : self.set_direction("out")).grid(row = 7, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "Delete Connection", command = lambda : self.connect_to(None)).grid(row = 8, column = self.grid_width + 1, sticky = W)
			Button(self.connectionEditor, text = "Done", command = self.done_editing_connections).grid(row = 9, column = self.grid_width + 1, sticky = W)

		else:
			tkMessageBox.showwarning("Hey!", "You are already editing the connections for this area!")
		
	def connect_to(self, area):
		print area
		self.areas[self.editing].set_neighbor(self.current_direction, area)
	
	def set_direction(self, direction):
		self.current_direction = direction
	
	def done_editing_connections(self):
		self.connecting = False
		self.connectionEditor.destroy()
	
	def done_editing_game(self):
		dosave = tkMessageBox.askyesnocancel("Save?", "Do you want to save before quitting?",
											type = tkMessageBox.YESNOCANCEL)
		if  dosave == False:
			self.root.destroy()
			self.play = False
		
		elif dosave == True:
			if self.save():
				self.root.destroy()
				self.play = False
				
		else:
			print "canceling."
	
	def tool_enable(self, tool):
		print "New", tool, "tool."
		self.tool = Tool(self, type = tool)
		
	def find(self, x, y):
		for i in range(len(self.areas)):
			if self.areas[i].detect_click(x, y):
				return i
		
		return None
	
	def click(self, event):
		self.tool.click(event)
	
	def unclick(self, event):
		self.tool.unclick(event)
		
	def mouse_move(self, event):
		self.tool.mouse_move(event)
	
	def select(self, index, state = None):
		if state == None:
			if self.selection != None:
				if self.selection != index:
					if self.areas[self.selection].selected:
						self.done_editing_area()
						self.areas[self.selection].deselect()
				
			if index != None:
				self.selection = index
				if self.areas[index].selected:
					self.done_editing_area()
					self.areas[index].deselect()
				else:
					self.areas[index].select()
					self.edit_area()
		elif state == True:	
			if self.selection != index:
				self.areas[self.selection].deselect()
				self.selection = index
				self.areas[index].select()
		else:
			if self.selection == index:
				self.areas[index].deselect()
				self.selection = None
			

class Box:

	def __init__(self, parent, x, y, width = 75, height = 75, forsave = False, area = None):
		self.parent = None
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.border = 5
		self.selected = False
		self.connections = []
		self.area = area
		if area == None:
			self.area = Area()
		if not forsave:
			self.parent = parent
			self.create()
	
	def create(self):
		hw = self.width/2
		hh = self.height/2
		self.outline = self.parent.create_rectangle(self.x - hw - self.border,
					self.y - hh - self.border, self.x + hw + self.border,
					self.y + hh + self.border, fill = "white")
					
	def move(self, x, y):
		hw = self.width/2
		hh = self.height/2
		self.x = x
		self.y = y
		self.parent.coords(self.outline, self.x - hw - self.border,
					self.y - hh - self.border, self.x + hw + self.border,
					self.y + hh + self.border)
		for group in self.connections:
			group[1].update()
		
	def detect_click(self, x, y):
		if x > self.x - self.width/2 and x < self.x + self.width/2:
			if y > self.y - self.height/2 and y < self.y + self.height/2:
				return True
		
		return False
		
	def select(self):
		self.parent.itemconfig(self.outline, fill = "yellow")
		self.selected = True
			
	def deselect(self):
		self.parent.itemconfig(self.outline, fill = "white")
		self.selected = False
			
	def add_connection(self, direction, string, object):
		self.connections.append([direction, string, object])
		
class String:
	
	def __init__(self, parent, box_a, box_b, forsave = False):
		self.parent = None
		if not forsave:
			print "making stuff!"
			self.a = box_a
			self.b = box_b
			self.a.add_connection("to_rome", self, self.b)
			self.b.add_connection("to_rome", self, self.a)
			World.strings.append(self)	
			self.parent = parent
			self.line = self.parent.create_line(self.a.x, self.a.y, self.b.x, self.b.y, width = 5, fill = "white")
			self.parent.tag_lower(self.line)
			self.update()
		
	def update(self):
		self.parent.coords(self.line, self.a.x, self.a.y, self.b.x, self.b.y)
		
		
		
class Tool:
		
	def __init__(self, parent, type = "select"):
		self.type = type
		print self.type
		self.parent = parent
		self.held = None
		self.deltax = 0
		self.deltay = 0
		self.a = None
		self.todeselect = False
	
	def click(self, event):
		if self.type == "select":
			print self.type
			self.select(event)
		if self.type == "add_area":
			print self.type
			self.add_area(event)
		if self.type == "connect":
			print self.type
			self.connect(event)
			
	def unclick(self, event):
		if self.type == "select":
			self.drop()
			if self.todeselect:
				self.parent.select(self.parent.find(event.x, event.y))
			
	def mouse_move(self, event):
		if self.type == "select":
			if (self.held):
				self.drag(event)
				
	def select(self, event):
		obj = self.parent.find(event.x, event.y)
		if obj != None:
			if not self.parent.areas[obj].selected:
				self.parent.select(obj)
				self.pick_up(obj, event)
				self.todeselect = False
				
			else:
				self.pick_up(obj, event)
				self.todeselect = True
			
	def connect(self, event):
		obj = self.parent.find(event.x, event.y)
		if obj != None:
			self.parent.select(obj)
			if not self.a:
				self.a = self.parent.areas[obj]
			else:
				String(self.parent.canvas, self.a, self.parent.areas[obj])
				self.a = None
		
	def drag(self, event):
		self.held.move(event.x + self.deltax, event.y + self.deltay)
		self.todeselect = False
		
	def add_area(self, event):
		self.parent.areas.append(Box(self.parent.canvas, event.x, event.y))
		
	def drop(self):
		self.held = None
		
	def pick_up(self, object, event):
		self.held = self.parent.areas[object]
		self.deltax = self.held.x - event.x 
		self.deltay = self.held.y - event.y