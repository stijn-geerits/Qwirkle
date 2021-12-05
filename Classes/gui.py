#!/usr/bin/env python3

# import classes #
import pygame
#initialize pygame (required for use of fonts)
pygame.init()



### Classes ###
# General class for graphical widgets #
class Widget():
	"""
	General class for widgets in the pygame environment
	"""
	#possible state values
	UNAVAILABLE = 0
	IDLE = 1
	HOVER = 2
	ACTIVE = 3
	
	def __init__(self):
		self.current_state = self.IDLE
		self.states = [pygame.Surface([0, 0])] * 4
		self.position = [0, 0]
		return
	
	def get_current_state(self):
		"""
		Returns the current state of the widget
		"""
		return self.current_state
	
	def set_current_state(self, state):
		"""
		Update the current state of the widget
		"""
		self.current_state = state
		return
	
	def get_states(self):
		"""
		Returns all possible states of the widget
		"""
		return self.states
	
	def define_states(self, unavailable, idle, hover, active):
		"""
		Define the presentation of the widget for all four states
		
		All variables should contain pygame.Surface objects
		Any state defined prior will be overridden
		"""
		self.states = [unavailable, idle, hover, active]
		return
	
	def get_rect(self):
		"""
		Get the pygame.Rect object for the widget
		"""
		#pygame.Rect object of a pygame.Surface object is located at [0, 0] => move it into position
		return self.states[self.current_state].get_rect().move(self.position)
	
	def place(self, location, relpos="topleft"):
		"""
		Set the location at which to blit the widget
		"""
		rect = set_relpos(self.get_rect(), location, relpos)
		self.position = rect.topleft
		return
	
	def blit_on(self, surface):
		"""
		Blit the widget on the surface
		"""
		surface.blit(self.states[self.current_state], self.get_rect())
		return

# Class for graphical button widgets #
class Button(Widget):
	"""
	Class for button widgets in the pygame environment
	"""
	
	def __init__(self):
		Widget.__init__(self)
		self.label = "Button"
		self.function = None
		return
	
	def get_label(self):
		"""
		Returns the label of the button
		"""
		return self.label
	
	def set_label(self, label, color=(32, 32, 32), pad=4):
		"""
		Set the label to place on the button
		
		label should contain a string without line breaks
		color should contain a triplet with RGB color values
		pad should contain a positive integer defining the amount of padding
			between the edge of the button and the label text
		"""
		self.label = label
		#render the label on each state
		for state in self.states:
			#get the pygame.Rect object for the state
			state_rect = state.get_rect()
			#don't try rendering the label on a state that is too small
			if state_rect.width > pad and state_rect.height > pad:
				#render the font for the label
				font = pygame.font.SysFont(None, state_rect.height - pad)
				#render the label text
				text = font.render(label, True, color)
				#get the pygame.Rect object for the label
				rect = text.get_rect()
				if rect.width > (state_rect.width - pad):
					#resize the label to fit within the button
					ratio = (state_rect.width - pad) / rect.width
					font = pygame.font.SysFont(None, int(ratio * (state_rect.height - pad)))
					text = font.render(label, True, color)
					rect = text.get_rect()
				#set the center of the label to the center of the button
				rect.center = state_rect.center
				#render the label on the state
				state.blit(text, rect)
		return
	
	def set_function(self, function):
		"""
		Set the function for the button
		"""
		self.function = function
		return
	
	def run_function(self):
		"""
		Run the function bound to the button
		"""
		#verify that the button is active before running the function
		if self.current_state != self.ACTIVE:
			print("[gui.py]Button.activate:\x1b[91m Cannot run the function of a button that is not active.\x1b[00m")
		#prevent running the function prior to its definition
		elif self.function != None:
			return self.function()
		return

# Class for graphical input widgets #
class Input(Widget):
	"""
	Class for input widgets in the pygame environment
	"""
	
	def __init__(self, default_value="", text_padding=4):
		#call the parent function
		Widget.__init__(self)
		self.value = default_value
		self.padding = text_padding
		return
	
	def get_value(self):
		"""
		Returns the inputted value
		"""
		return self.value
	
	def set_value(self, value):
		"""
		Set the current value of the input
		
		value should contain a single line string
		"""
		self.value = value
		return
	
	def type(self, keys):
		"""
		Type text to the input based on the pressed keys
		"""
		#only input if the input is selected
		if self.current_state == Widget.ACTIVE:
			#end of input
			if keys.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
				Widget.set_current_state(self, Widget.HOVER)
			#remove the last character from the value
			elif keys.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
				if len(self.value) > 0:
					self.value = self.value[:-1]
			#ignore the following key presses
			elif keys.key in [pygame.K_ESCAPE, pygame.K_HOME, pygame.K_END, pygame.K_INSERT, pygame.K_TAB]:
				inputted += ""
			elif keys.key in range(pygame.K_F1, pygame.K_F12 + 1):
				inputted += ""
			#add the typed character to the value
			else:
				self.value += keys.unicode
				#check whether the text still fits within the input box
				font = pygame.font.SysFont(None, self.states[self.current_state].get_height() - self.padding)
				txtRect = font.render(self.value, True, (0, 0, 0)).get_rect()
				#remove the last character
				if txtRect.width > (self.states[self.current_state].get_width() - 2 * self.padding):
					self.value = self.value[:-1]
		return
	
	def blit_on(self, surface):
		"""
		Blit the widget on the surface
		"""
		#call the parent function
		Widget.blit_on(self, surface)
		#calculate the font size for the text
		fontsize = self.states[self.current_state].get_height() - self.padding
		#render the value (move the rect object by the padding amount and only sent the topleft coordinate)
		rendertext(surface, self.value, fontsize, location=self.get_rect().move(self.padding, 0).midleft, relpos="midleft")
		return



### Functions ###
def set_relpos(rect, location, relpos):
	"""
	Set the location of the pygame.Rect object using the relpos value
	"""
	if relpos == "bottomleft":
		rect.bottomleft = location
	elif relpos == "bottomright":
		rect.bottomright = location
	elif relpos == "center":
		rect.center = location
	elif relpos == "centerx":
		rect.centerx = location
	elif relpos == "centery":
		rect.centery = location
	elif relpos == "midbottom":
		rect.midbottom = location
	elif relpos == "midleft":
		rect.midleft = location
	elif relpos == "midright":
		rect.midright = location
	elif relpos == "midtop":
		rect.midtop = location
	elif relpos == "topleft":
		rect.topleft = location
	elif relpos == "topright":
		rect.topright = location
	else:
		#invalid relpos value given, go with standard setting
		print("[gui.py]set_relpos:\x1b[91m Invalid relpos value '%s' received, defaulting to 'topleft'.\x1b[00m" % relpos)
		rect.topleft = location
	return rect

def rendertext(surface, text, size=32, font=None, location=[0, 0], relpos="topleft", color=(32, 32, 32)):
	"""
	Display the given text on the surface, with the given font and size, at the given location
	"""
	#render the font for the text
	if font == None:
		font = pygame.font.SysFont(None, size)
	else:
		font = pygame.font.Font(font, size)
	#split up the text into multiple strings when it contains a '\n'
	text = text.split("\n")
	#get the amount of lines of text
	if type(text) == list:
		lines = len(text)
	else:
		lines = 1
	
	#render the text and put it in place
	textpos = []
	for line in range(0, lines):
		text[line] = font.render(text[line], True, color)
		#update the position according to the relpos variable
		textpos.append(set_relpos(text[line].get_rect(), [location[0], location[1]+int(size*line)], relpos))
	
	#place the text on the surface
	for line in range(0, lines):
		surface.blit(text[line], textpos[line])
	return

def renderimage(surface, image, location=[0, 0], relpos="topleft"):
	"""
	Load and display an image on the given surface at the given location
	"""
	#load the image
	img = pygame.image.load(image)
	#place the image in the correct location based on the relpos value
	imgRect = set_relpos(img.get_rect(), location, relpos)
	#place the image on the surface
	surface.blit(img, imgRect)
	return

def rectangle(size, fill, edge_width=0, edge=(0, 0, 0)):
	"""
	Draws a rectangular shape with the given fill and edge on a pygame.Surface object
	
	fill should contain a triplet with RGB color values
	size should contain a tuple with the width and height of the rectangle
	edge_width should be a zero or positive integer defining the size of the edge
	edge should contain a triplet with RGB color values
	"""
	#initialize a pygame.Surface object for the rectangle
	surf = pygame.Surface(size)
	#draw a rectangle for the edge
	if edge_width > 0:
		pygame.draw.rect(surf, edge, surf.get_rect())
	#calculate the pygame.Rect object for the fill
	fill_rect = surf.get_rect().move(edge_width, edge_width)
	fill_rect.width -= 2 * edge_width
	fill_rect.height -= 2 * edge_width
	#fill the rectangle
	pygame.draw.rect(surf, fill, fill_rect)
	#return the pygame.Surface object
	return surf

def circle(radius, fill, edge_width=0, edge=(0, 0, 0)):
	"""
	Draws a circular shape with the given fill and edge on a pygame.Surface object
	
	fill should contain a triplet with RGB color values
	radius should contain a positive integer defining the radius of the circle
	edge_width should be a zero or positive integer defining the size of the edge
	edge should contain a triplet with RGB color values
	"""
	#initialize a pygame.Surface object for the circle
	surf = pygame.Surface([2 * radius] * 2)
	surf.set_colorkey((0, 0, 0))
	#draw a circle for the edge
	if edge_width > 0:
		pygame.draw.circle(surf, edge, [radius] * 2, radius)
	#fill the circle
	pygame.draw.circle(surf, fill, [radius] * 2, radius - edge_width)
	#return the pygame.Surface object
	return surf

def ellipse(size, fill, edge_width=0, edge=(0, 0, 0)):
	"""
	Draws a ellipse shape with the given fill and edge on a pygame.Surface object
	
	fill should contain a triplet with RGB color values
	size should contain a tuple with the width and height of the ellipse
	edge_width should be a zero or positive integer defining the size of the edge
	edge should contain a triplet with RGB color values
	"""
	#initialize a pygame.Surface object for the ellipse
	surf = pygame.Surface(size)
	surf.set_colorkey((0, 0, 0))
	#draw an ellipse for the edge
	if edge_width > 0:
		pygame.draw.ellipse(surf, edge, surf.get_rect())
	#calculate the pygame.Rect object for the fill
	fill_rect = surf.get_rect().move(edge_width, edge_width)
	fill_rect.width -= 2 * edge_width
	fill_rect.height -= 2 * edge_width
	#fill the rectangle
	pygame.draw.ellipse(surf, fill, fill_rect)
	#return the pygame.Surface object
	return surf

def grid(row_heights, column_widths, edge=(0, 0, 0), fill=(255, 255, 255)):
	"""
	Draws a grid with rows and columns with the given dimensions on a pygame.Surface object
	
	row_heights should contain a list of integers defining the height of each row in px
	column_widths should contain a list of integers defining the width of each column in px
	edge should contain a triplet with RGB color values
	fill should contain a triplet with RGB color values or a list of the previous
	"""
	#initialize a pygame.Surface object
	surf = pygame.Surface([sum(column_widths) - len(column_widths) + 1, sum(row_heights) - len(row_heights) + 1])
	#check the fill color
	if not is_rgb(fill):
		for color in fill:
			if not is_rgb(color):
				print("[gui.py]grid:\x1b[91m Parameter fill does not contain one or more RGB triplets.\x1b[00m")
				return surf
		#check whether enough colors were defined
		if len(fill) != (len(row_heights) * len(column_widths)):
			print("[gui.py]grid:\x1b[91m Parameter fill does not contain enough RGB triplets.\x1b[00m")
			return surf
		#draw each cell
		color = 0
		offset = [0, 0]
		for h in row_heights:
			for w in column_widths:
				#get and draw the cell
				cell = rectangle([w, h], fill[color], 1, edge)
				surf.blit(cell, offset)
				#update the color and offset value
				color += 1
				offset[0] += (w - 1)
			#update the offset value
			offset[0] = 0
			offset[1] += (h - 1)
	else:
		#draw the bounding box
		box = rectangle(surf.get_size(), fill, 1, edge)
		surf.blit(box, box.get_rect())
		#draw the row seperators
		offset = 0
		for h in row_heights:
			offset += (h - 1)
			pygame.draw.aaline(surf, edge, [0, offset], [surf.get_width(), offset])
		#draw the column seperators
		offset = 0
		for w in column_widths:
			offset += (w - 1)
			pygame.draw.aaline(surf, edge, [offset, 0], [offset, surf.get_height()])
	#return the pygame.Surface object
	return surf

def is_rgb(color):
	"""
	Test if the given color is a triplet containing RGB color values
	
	RGB color values can have contain any value in the range 0-255
	"""
	if len(color) != 3:
		return False
	for value in color:
		if type(value) != int:
			return False
		elif value < 0 or value > 255:
			return False
	return True
