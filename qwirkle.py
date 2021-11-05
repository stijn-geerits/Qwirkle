#!/usr/bin/env python3

#import classes
import inspect, pygame
#initialize pygame (necessary for fonts)
pygame.init()



### Global variables ###
# global constants #
CLASSESDIR = "Classes/"
CONFIGDIR = ""
GRAPHICSDIR = "Graphics/"
LANGUAGEDIR = "Lang/"



### Classes ###
# Container for storing and retreiving user config files #
class user:
	exec(open(CONFIGDIR + "user.conf", 'r').read())
	
	def get_config(self):
		"""
		Returns multiline string containing formatted user config data
		"""
		#get all class attributes with their values
		attr = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
		attr = [a for a in attr if not(a[0].startswith("__") and a[0].endswith("__"))]
		#format attr to a multiline string containing "attribute = value\n"
		cfg = ""
		for a in attr:
			#"attribute = "
			cfg += a[0] + " = "
			if type(a[1]) == str:
				#"\"value\""
				cfg += "\"" + a[1] + "\""
			else:
				#"value"
				cfg += str(a[1])
			cfg += '\n'
		return cfg.rstrip('\n')

# Container for storing language files #
class lang:
	exec(open(LANGUAGEDIR + user.lang + ".lang", 'r').read())

# General class for graphical widgets #
class Widget(pygame.Surface):
	"""
	General class for widgets in the pygame environment
	"""
	#possible state values
	UNAVAILABLE = 0
	IDLE = 1
	HOVER = 2
	ACTIVE = 3
	#other class variables
	current_state = 1
	states = [pygame.Surface([0, 0])] * 4
	position = [0, 0]
	
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
		self.update()
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
		self.update()
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
	
	def update(self):
		"""
		Updates the appearance of the widget
		"""
		self.set_colorkey((0, 0, 0))
		self.fill((0, 0, 0))
		self.blit(self.states[self.current_state], pygame.Rect(0, 0, self.get_width(), self.get_height()))
		return
	
	def blit_on(self, surface):
		"""
		Blit the widget on the surface
		"""
		surface.blit(self, self.get_rect())
		return

# Class for graphical button widgets #
class Button(Widget):
	"""
	Class for button widgets in the pygame environment
	"""
	#class variables
	label = "Button"
	function = None
	
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
		self.update()
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
			print("[Qwirkle]Button.activate:\x1b[91m Cannot run the function of a button that is not active.\x1b[97m")
		#prevent running the function prior to its definition
		elif self.function != None:
			self.function()
		return

# Container for graphical objects #
class Style(pygame.Surface):
	"""
	Container for graphical objects
	"""
	
	def rect(self, fill, edge_width=0, edge=(0, 0, 0)):
		"""
		Draws a rectangular shape with the given fill and edge on a pygame.Surface object
		
		fill should contain a triplet with RGB color values
		edge_width should be a zero or positive integer defining the size of the edge
		edge should contain a triplet with RGB color values
		"""
		#draw a rectangle for the edge
		if edge_width > 0:
			pygame.draw.rect(self, edge, self.get_rect())
		#calculate the pygame.Rect object for the fill
		fill_rect = self.get_rect().move(edge_width, edge_width)
		fill_rect.width -= 2 * edge_width
		fill_rect.height -= 2 * edge_width
		#fill the rectangle
		pygame.draw.rect(self, fill, fill_rect)
		return
	
	def circle(self, fill, edge_width=0, edge=(0, 0, 0)):
		"""
		Draws a circular shape with the given fill and edge on a pygame.Surface object
		
		fill should contain a triplet with RGB color values
		edge_width should be a zero or positive integer defining the size of the edge
		edge should contain a triplet with RGB color values
		"""
		#draw a circle for the edge
		if edge_width > 0:
			pygame.draw.circle(self, edge, self.get_rect().center, self.width // 2)
		#fill the circle
		pygame.draw.circle(self, fill, self.get_rect().center, (self.width - edge_width) // 2)
		return
	
	def ellipse(self, fill, edge_width=0, edge=(0, 0, 0)):
		"""
		Draws a ellipse shape with the given fill and edge on a pygame.Surface object
		
		fill should contain a triplet with RGB color values
		edge_width should be a zero or positive integer defining the size of the edge
		edge should contain a triplet with RGB color values
		"""
		#draw an ellipse for the edge
		if edge_width > 0:
			pygame.draw.ellipse(self, edge, self.get_rect())
		#calculate the pygame.Rect object for the fill
		fill_rect = self.get_rect().move(edge_width, edge_width)
		fill_rect.width -= 2 * edge_width
		fill_rect.height -= 2 * edge_width
		#fill the rectangle
		pygame.draw.ellipse(self, fill, fill_rect)
		return



### Functions ###
def full_quit():
	"""
	Quit the pygame environment before exit of program
	"""
	pygame.quit()
	exit()

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
		print("[Qwirkle]set_relpos:\x1b[91m Invalid relpos value '%s' received, defaulting to 'topleft'.\x1b[97m" % relpos)
		rect.topleft = location
	return rect

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
		textpos.append(set_relpos(text[line].get_rect(), [location[0], location[1]+int(1.25*size*line)], relpos))
	
	#place the text on the surface
	for line in range(0, lines):
		surface.blit(text[line], textpos[line])
	return

def button_builder(rect, states, function, label, labelcolor=None, labelpadding=None):
	"""
	Returns a fully set up button object
	"""
	#define the button object with the correct dimensions
	button = Button(rect.size)
	#move the button in place
	button.place(rect.topleft)
	#define the button's states (seperate list into individual arguments using '*')
	button.define_states(*states)
	#set the button's function
	button.set_function(function)
	#set the label for the button
	if labelcolor == None and labelpadding == None:
		button.set_label(label)
	elif labelcolor == None:
		button.set_label(label, pad=labelpadding)
	elif labelpadding == None:
		button.set_label(label, labelcolor)
	else:
		button.set_label(label, labelcolor, labelpadding)
	#return the button object
	return button



### Main program ###
if __name__ == "__main__":
	#set variables
	clock = pygame.time.Clock()
	loop = True
	
	# window setup #
	window = pygame.display.set_mode(user.winsize)
	pygame.display.set_caption(lang.qwirkle)
	
	#change window background
	window.fill((200, 200, 200))
	#show qwirkle title graphic
	renderimage(window, GRAPHICSDIR + "qwirkle.png", [int(user.winsize[0]*.5), int(user.winsize[1]*.05)], "midtop")
	#show the copyright notice
	rendertext(window, lang.copyright, int(user.winsize[1]*.03), None, [int(user.winsize[0]*.5), int(user.winsize[1]*.97)], "midbottom")
	
	# widgets setup #
	#define button dimensions
	button_size = [int(user.winsize[0] * .24), int(user.winsize[1] * .08)]
	button_edge_size = int(min(user.winsize) * .0016)
	#create button templates
	button_unavailable = Style(button_size)
	button_unavailable.rect((102, 102, 102), int(min(user.winsize) * .005), (61, 61, 61))
	button_idle = Style(button_size)
	button_idle.rect((34, 85, 170), int(min(user.winsize) * .005), (0, 44, 121))
	button_hover = Style(button_size)
	button_hover.rect((146, 178, 255), int(min(user.winsize) * .005), (34, 85, 170))
	button_active = Style(button_size)
	button_active.rect((0, 44, 121), int(min(user.winsize) * .005), (34, 85, 170))
	
	#define a list of widgets
	widgets = []
	#create the menu buttons
	bRect = set_relpos(pygame.Rect([0, 0]+button_size), [int(user.winsize[0]*.5), int(user.winsize[1]*.4)], "center")
	b = button_builder(bRect, [button_unavailable.copy(), button_idle.copy(), button_hover.copy(), button_active.copy()], None, lang.new_game)
	b.set_current_state(Widget.UNAVAILABLE)
	b.blit_on(window)
	widgets.append(b)
	
	bRect = set_relpos(pygame.Rect([0, 0]+button_size), [int(user.winsize[0]*.5), int(user.winsize[1]*.5)], "center")
	b = button_builder(bRect, [button_unavailable.copy(), button_idle.copy(), button_hover.copy(), button_active.copy()], full_quit, lang.exit)
	b.blit_on(window)
	widgets.append(b)
	
	#update the display
	pygame.display.update()
	
	# main loop #
	while loop == True:
		#set the frame-rate
		clock.tick(user.fps)
		#get window events
		for event in pygame.event.get():
			#close window event
			if event.type == pygame.QUIT:
				loop = False
			#check mouse button events
			if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[pygame.BUTTON_LEFT - 1]:
				for w in widgets:
					if w.get_current_state() == Widget.HOVER:
						w.set_current_state(Widget.ACTIVE)
						w.blit_on(window)
						pygame.display.update()
			if event.type == pygame.MOUSEBUTTONUP:
				for w in widgets:
					if w.get_current_state() == Widget.ACTIVE:
						if type(w) == Button:
							w.run_function()
						w.set_current_state(Widget.HOVER)
						w.blit_on(window)
						pygame.display.update()
		
		#look whether the mouse was moved
		mouse_move = pygame.mouse.get_rel()
		if mouse_move != (0, 0):
			for w in widgets:
				#check whether the widget is being hovered over (and the widget is set to idle)
				if w.get_rect().collidepoint(pygame.mouse.get_pos()) and w.get_current_state() == Widget.IDLE:
					w.set_current_state(Widget.HOVER)
					w.blit_on(window)
					pygame.display.update()
				#check whether the widget is not being hovered over (and this has not been set)
				elif not w.get_rect().collidepoint(pygame.mouse.get_pos()) and (w.get_current_state() == Widget.HOVER or w.get_current_state() == Widget.ACTIVE):
					w.set_current_state(Widget.IDLE)
					w.blit_on(window)
					pygame.display.update()
	
	#quit the program
	full_quit()
