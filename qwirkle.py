#!/usr/bin/env python3

# import classes #
import inspect, pygame, sys



### Global variables ###
# global constants #
CLASSESDIR = "Classes/"
CONFIGDIR = ""
GRAPHICSDIR = "Graphics/"
LANGUAGEDIR = "Lang/"
#insert the CLASSESDIR into the search list for importing scripts
sys.path.insert(1, CLASSESDIR)
#import the custom classes
import gui



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

# Container for all menu data #
class Menu:
	"""
	Manager for all menus for Qwirkle
	"""
	#possible menu values
	EMPTY = 0
	MAIN = 1
	RULES = 2
	NEW_GAME = 3
	GAME = 4
	
	def __init__(self, window_size):
		self.size = window_size
		
		# button templates #
		#button dimensions
		self.btn_size = [int(self.size[0] * .24), int(self.size[1] * .08)]
		btn_edge_size = int(min(self.size) * .004)
		#button template
		btn_unavailable = gui.rectangle(self.btn_size, (102, 102, 102), btn_edge_size, (61, 61, 61))
		btn_idle = gui.rectangle(self.btn_size, (34, 85, 170), btn_edge_size, (0, 44, 121))
		btn_hover = gui.rectangle(self.btn_size, (146, 178, 255), btn_edge_size, (34, 85, 170))
		btn_active = gui.rectangle(self.btn_size, (0, 44, 121), btn_edge_size, (34, 85, 170))
		self.button_template = [btn_unavailable, btn_idle, btn_hover, btn_active]
		#small button dimensions
		self.btn_small_size = [self.btn_size[1]] * 2
		#small button template
		btn_unavailable = gui.rectangle(self.btn_small_size, (102, 102, 102), btn_edge_size, (61, 61, 61))
		btn_idle = gui.rectangle(self.btn_small_size, (34, 85, 170), btn_edge_size, (0, 44, 121))
		btn_hover = gui.rectangle(self.btn_small_size, (146, 178, 255), btn_edge_size, (34, 85, 170))
		btn_active = gui.rectangle(self.btn_small_size, (0, 44, 121), btn_edge_size, (34, 85, 170))
		self.button_small_template = [btn_unavailable, btn_idle, btn_hover, btn_active]
		
		# input templates #
		#input dimensions
		self.input_size = [int(self.size[0] * .48), int(self.size[1] * .08)]
		input_edge_size = int(min(self.size) * .004)
		#input template
		input_unavailable = gui.rectangle(self.input_size, (128, 128, 128), input_edge_size, (32, 32, 32))
		input_idle = gui.rectangle(self.input_size, (224, 224, 224), input_edge_size, (32, 32, 32))
		input_hover = gui.rectangle(self.input_size, (224, 224, 224), input_edge_size, (64, 64, 64))
		input_active = gui.rectangle(self.input_size, (255, 255, 255), input_edge_size, (128, 128, 128))
		self.input_template = [input_unavailable, input_idle, input_hover, input_active]
		
		#initialize the main menu
		self.select_menu(self.MAIN)
		return
	
	def get_menu(self):
		"""
		Returns the currently selected menu
		"""
		return self.menu
	
	def select_menu(self, menu):
		"""
		Select another menu to display
		"""
		#save the menu value
		self.menu = menu
		#set the surface and widgets for the current menu
		if menu == self.EMPTY:
			self.background = self.__get_menu_empty()
			self.widgets = []
		elif menu == self.MAIN:
			self.background = self.__get_menu_main()
			self.widgets = self.__get_widgets_main()
		elif menu == self.RULES:
			self.background = self.__get_menu_rules()
			self.widgets = self.__get_widgets_rules()
		elif menu == self.NEW_GAME:
			self.background = self.__get_menu_new_game()
			self.widgets = self.__get_widgets_new_game()
		elif menu == self.GAME:
			self.background = self.__get_menu_game()
			self.widgets = self.__get_widgets_game()
		else:
			print("[qwirkle.py]Menu.get_background:\x1b[91m Unknown menu is set, defaulting to empty.\x1b[97m")
			self.menu = self.EMPTY
			self.background = self.__get_menu_empty()
			self.widgets = []
		#return the selected menu
		return menu
	
	def get_background(self):
		"""
		Returns the pygame.Surface object containing the graphics for the current menu
		"""
		return self.background
	
	def __get_menu_empty(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		#fill the surface with black
		surf.fill((0, 0, 0))
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_main(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		surf.fill((200, 200, 200))
		#place the qwirkle title graphic
		gui.renderimage(surf, GRAPHICSDIR + "qwirkle.png", [int(self.size[0]*.5), int(self.size[1]*.05)], "midtop")
		#place the copyright notice
		gui.rendertext(surf, lang.copyright, int(self.size[1]*.03), None, [int(self.size[0]*.5), int(self.size[1]*.97)], "midbottom")
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_rules(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background for the menu
		surf.fill((200, 200, 200))
		#place the menu title
		gui.rendertext(surf, lang.rules, int(self.size[1]*.1), None, [int(self.size[0]*.5), int(self.size[1]*.02)], "midtop")
		#place the rules text
		gui.rendertext(surf, lang.rules_text, int(self.size[1]*.04), None, [int(self.size[0]*.02), int(self.size[1]*.11)])
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_new_game(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background for the menu
		surf.fill((200, 200, 200))
		#place the menu title
		gui.rendertext(surf, lang.player_selection, int(self.size[1]*.1), None, [int(self.size[0]*.5), int(self.size[1]*.02)], "midtop")
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_game(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background for the menu
		surf.fill((200, 200, 200))
		
		#load the tileset for the tiles
		tileset = Tileset(GRAPHICSDIR + "tiles.png", 32)
		#<test> draw the tileset
		for tile in range(1, 37):
			tileset.draw_tile(surf, tile, [(tile - 1) % 6, (tile - 1) // 6], offset=[50, 50])
		
		#return the pygame.Surface object
		return surf
	
	def get_widgets(self):
		"""
		Returns the Widget objects for the current menu
		"""
		return self.widgets
	
	def __get_widgets_main(self):
		#initialize a list of widgets
		widgets = []
		
		# button objects #
		#new game button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.4)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.NEW_GAME), lang.new_game)
		widgets.append(btn)
		#rules button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.5)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.RULES), lang.rules)
		widgets.append(btn)
		#settings button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.6)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], None, lang.settings)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#exit button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.7)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], full_quit, lang.exit)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_rules(self):
		#initialize a list of widgets
		widgets = []
		
		# button objects #
		#back button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.MAIN), lang.back)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_new_game(self):
		#initialize a list of widgets
		widgets = []
		
		# button objects #
		#add player button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.75), int(self.size[1]*.15)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_small_template], self.__add_input, lang.add)
		widgets.append(btn)
		#remove player button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.75), int(self.size[1]*.25)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_small_template], self.__remove_input, lang.subtract)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#back button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.3), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.MAIN), lang.back)
		widgets.append(btn)
		#start button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.7), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.GAME), lang.start_game)
		widgets.append(btn)
		
		# input objects #
		inptRect = gui.set_relpos(pygame.Rect([0, 0]+self.input_size), [int(self.size[0]*.45), int(self.size[1]*.15)], "center")
		inpt = input_builder(inptRect, [t.copy() for t in self.input_template], lang.default_player %(1))
		widgets.append(inpt)
		inptRect = gui.set_relpos(pygame.Rect([0, 0]+self.input_size), [int(self.size[0]*.45), int(self.size[1]*.25)], "center")
		inpt = input_builder(inptRect, [t.copy() for t in self.input_template], lang.default_player %(2))
		widgets.append(inpt)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_game(self):
		#initialize the list of widgets
		widgets = []
		
		#return the Widget objects
		return widgets
	
	def __add_input(self):
		#only run if the current menu is the new game menu
		if self.menu != self.NEW_GAME:
			return
		
		#get the current amount of inputs
		widget_types = [type(w) for w in self.widgets]
		inpt_cnt = widget_types.count(gui.Input)
		#add an input
		inpt_cnt += 1
		inptRect = gui.set_relpos(pygame.Rect([0, 0]+self.input_size), [int(self.size[0]*.45), int(self.size[1]*(inpt_cnt*.1+.05))], "center")
		inpt = input_builder(inptRect, [t.copy() for t in self.input_template], lang.default_player %(inpt_cnt))
		self.widgets.append(inpt)
		#disable the button that adds inputs when the 8'th input is added
		if inpt_cnt == 8:
			for w in self.widgets:
				if type(w) == gui.Button:
					if w.get_label() == lang.add:
						w.set_current_state(gui.Widget.UNAVAILABLE)
						break
		#enable the button that removes inputs when the input count surpasses 2
		if inpt_cnt == 3:
			for w in self.widgets:
				if type(w) == gui.Button:
					if w.get_label() == lang.subtract:
						w.set_current_state(gui.Widget.IDLE)
						break
		#return the current input count
		return inpt_cnt
	
	def __remove_input(self):
		#only run if the current menu is the new game menu
		if self.menu != self.NEW_GAME:
			return
		
		#get the current amount of inputs
		widget_types = [type(w) for w in self.widgets]
		inpt_cnt = widget_types.count(gui.Input)
		#remove an input
		inpt_cnt -= 1
		self.widgets.pop()
		#disable the button that removes inputs when only 2 inputs remain
		if inpt_cnt == 2:
			for w in self.widgets:
				if type(w) == gui.Button:
					if w.get_label() == lang.subtract:
						w.set_current_state(gui.Widget.UNAVAILABLE)
						break
		#enable the button that adds inputs when the input count drops below 8
		elif inpt_cnt == 7:
			for w in self.widgets:
				if type(w) == gui.Button:
					if w.get_label() == lang.add:
						w.set_current_state(gui.Widget.IDLE)
						break
		#return the current input count
		return inpt_cnt

# Container for tilesets #
class Tileset:
	"""
	Store and manage tilesets
	"""
	def __init__(self, image, tilesize):
		#Load the tileset image file
		self.tileset = pygame.image.load(image)
		#Set the tile size
		self.tilesize = tilesize
		
		#Calculate the amount of tiles total and in each direction
		self.tileheight = self.tileset.get_height() // self.tilesize
		self.tilewidth = self.tileset.get_width() // self.tilesize
		self.tilecount = self.tileheight * self.tilewidth
		return
	
	def get_tile(self, tile):
		"""
		Returns a surface containing the requested tile from the tileset.
		
		Returns a 0x0 surface if tile is outside the range of possible tiles.
		"""
		if tile > 0 and tile < self.tilecount:
			#Create a new surface the size of a tile
			tileSurf = pygame.Surface([self.tilesize] * 2)
			#Draw the tile to the new surface
			tileSurf.blit(self.tileset, [0, 0], pygame.Rect((tile % self.tilewidth) * self.tilesize, (tile // self.tilewidth) * self.tilesize, self.tilesize, self.tilesize))
			#Return the surface containing the tile
			return tileSurf
		else:
			#Given tile does not exist within the tileset
			return pygame.Surface([0, 0])
	
	def draw_tile(self, surface, tile, pos, tilecoords=True, offset=[0, 0]):
		"""
		Draw a tile from the tileset on a surface
		
		Returns -1 if the tile could not be drawn, returns tile otherwise.
		If tilecoords is set to False, x and y will be interpreted as absolute
		coordinates. Otherwise, x and y are considered positions in a tile grid.
		"""
		if tile < 0 or tile >= self.tilecount:
			#Tile does not exist
			return -1
		elif tilecoords:
			#Interpret x and y as tile coordinates
			surface.blit(self.get_tile(tile), [pos[0] * self.tilesize + offset[0], pos[1] * self.tilesize + offset[1]])
		else:
			#Interpret x and y as absolute coordinates
			surface.blit(self.get_tile(tile), [pos[0] + offset[0], pos[1] + offset[1]])
		#Return the index of the tile that was drawn to the screen
		return tile



### Functions ###
def full_quit():
	"""
	Quit the pygame environment before exit of program
	"""
	pygame.quit()
	exit()

def button_builder(rect, states, function, label, labelcolor=None, labelpadding=None):
	"""
	Returns a fully set up button object
	"""
	#define the button object
	button = gui.Button()
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

def input_builder(rect, states, default=None, textpadding=None):
	"""
	Returns a fully set up input object
	"""
	#define the input object
	if default == None and textpadding == None:
		inpt = gui.Input()
	elif default == None:
		inpt = gui.Input(text_padding=textpadding)
	elif textpadding == None:
		inpt = gui.Input(default)
	else:
		inpt = gui.Input(default, textpadding)
	#move the input in place
	inpt.place(rect.topleft)
	#define the input's states (seperate list into individual arguments using '*')
	inpt.define_states(*states)
	#return the input object
	return inpt



### Main program ###
if __name__ == "__main__":
	#set variables
	ALPHA = (0, 0, 0)
	background = pygame.Surface(user.winsize)
	clock = pygame.time.Clock()
	loop = True
	rtrn = None
	selected = None
	sprites_layer = pygame.Surface(user.winsize)
	update = []
	widgets = []
	widgets_layer = pygame.Surface(user.winsize)
	
	# window setup #
	window = pygame.display.set_mode(user.winsize)
	pygame.display.set_caption(lang.qwirkle)
	
	# menu setup #
	menus = Menu(user.winsize)
	background = menus.get_background()
	widgets = menus.get_widgets()
	widgets_layer.fill(ALPHA)
	widgets_layer.set_colorkey(ALPHA)
	sprites_layer.fill(ALPHA)
	sprites_layer.set_colorkey(ALPHA)
	
	#add the surfaces and widgets to the update list
	update.append(background)
	update.extend(widgets)
	update.extend([widgets_layer, sprites_layer])
	
	# main loop #
	while loop == True:
		#set the frame-rate
		clock.tick(user.fps)
		#get window events
		for event in pygame.event.get():
			#close window event
			if event.type == pygame.QUIT:
				loop = False
			#keyboard events
			if event.type == pygame.KEYDOWN:
				#sent pressed keys to input widget
				if type(selected) == gui.Input:
					selected.type(event)
					update.append(selected)
			#check mouse button events
			if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[pygame.BUTTON_LEFT - 1]:
				for w in widgets:
					#activate a widget
					if w.get_current_state() == gui.Widget.HOVER:
						w.set_current_state(gui.Widget.ACTIVE)
						update.append(w)
			if event.type == pygame.MOUSEBUTTONUP:
				if type(selected) in [gui.Widget, gui.Button, gui.Input]:
					#deactivate a widget
					if selected.get_current_state() == gui.Widget.ACTIVE and type(selected) != gui.Input:
						#run button function
						if type(selected) == gui.Button:
							rtrn = selected.run_function()
						else:
							rtrn = None
						#a menu was selected
						if rtrn != None:
							#clear the update list of old updates
							update = []
							#get the new menu data
							background = menus.get_background()
							widgets = menus.get_widgets()
							#clear the widgets and sprites layer
							widgets_layer.fill(ALPHA)
							sprites_layer.fill(ALPHA)
							#add the surfaces and widgets to the update list
							update.append(background)
							update.extend(widgets)
							update.extend([widgets_layer, sprites_layer])
						#update the widget state (if it still exists)
						if selected in widgets and selected.get_current_state() != gui.Widget.UNAVAILABLE:
							selected.set_current_state(gui.Widget.HOVER)
							#add the widget to the update list, if it isn't there already
							if not selected in update:
								update.append(selected)
		
		#look whether the mouse was moved
		mouse_move = pygame.mouse.get_rel()
		if mouse_move != (0, 0):
			for w in widgets:
				#check whether the widget is being hovered over (and the widget is set to idle)
				if w.get_rect().collidepoint(pygame.mouse.get_pos()) and w.get_current_state() == gui.Widget.IDLE:
					selected = w
					w.set_current_state(gui.Widget.HOVER)
					update.append(w)
				#check whether the widget is not being hovered over (and this has not been set)
				elif not w.get_rect().collidepoint(pygame.mouse.get_pos()) and (w.get_current_state() == gui.Widget.HOVER or w.get_current_state() == gui.Widget.ACTIVE):
					if selected == w:
						selected = None
					w.set_current_state(gui.Widget.IDLE)
					update.append(w)
		
		#update the display
		for u in update:
			#update a button or input
			if type(u) == gui.Button or type(u) == gui.Input:
				u.blit_on(widgets_layer)
		if len(update) > 0:
			update = []
			window.blit(background, [0, 0])
			window.blit(widgets_layer, [0, 0])
			window.blit(sprites_layer, [0, 0])
			pygame.display.update()
	
	#quit the program
	full_quit()
