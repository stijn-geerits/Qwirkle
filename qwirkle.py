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
	IDLE = 0
	HOVER = 1
	ACTIVE = 2
	UNAVAILABLE = 3
	
	def __init__(self):
		#set class properties
		self.current_state = self.IDLE
		self.states = [pygame.Surface([0, 0])] * 4
		self.rect = self.states[self.current_state].get_rect()
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
		self.rect = self.states[state]
		self.update()
		return
	
	def get_states(self):
		"""
		Returns all possible states of the widget
		"""
		return self.states
	
	def define_states(self, idle, hover, active, unavailable):
		"""
		Define the presentation of the widget for all four states
		
		All variables should contain pygame.Surface objects
		Any state defined prior will be overridden
		"""
		self.states = [idle, hover, active, unavailable]
		self.rect = self.states[self.current_state].get_rect()
		return
	
	def get_rect(self):
		"""
		Returns the pygame.Rect object for the current state of the widget
		"""
		return self.rect
	
	def place(self, location, relpos="topleft"):
		"""
		Move the widget to the specified location
		"""
		self.rect = set_relpos(self.rect, location, relpos)
		return
	
	def update(self):
		"""
		Updates the appearance of the widget
		"""
		self.blit(self.states[self.current_state], self.rect)
		return

# Class for graphical button widgets #
class Button(Widget):
	"""
	Class for button widgets in the pygame environment
	"""
	
	def __init__(self):
		self.label = "Button"
		self.function = None
		return
	
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
				if rect.width > state_rect.width - pad:
					#resize the label to fit within the button
					ratio = rect.width // (state_rect.width - pad)
					font = pygame.font.SysFont(None, ratio)
					text = font.render(label, True, color)
					rect = text.get_rect()
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
			print("[Qwirkle]Button.activate:\x1b[91m Cannot run the function of a button that is not active.\x1b[97m")
		#prevent running the function prior to its definition
		elif self.function != None:
			self.function()
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
	
	#update the display
	pygame.display.update()
	
	### main loop ###
	while loop == True:
		#set the frame-rate
		clock.tick(user.fps)
		#get window events
		for event in pygame.event.get():
			#close window event
			if event.type == pygame.QUIT:
				loop = False
	
	#quit the program
	pygame.quit()
	exit()
