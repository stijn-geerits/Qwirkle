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
	NEW_GAME = 2
	
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
			self.surface = self.__get_menu_empty()
			self.widgets = []
		elif menu == self.MAIN:
			self.surface = self.__get_menu_main()
			self.widgets = self.__get_widgets_main()
		elif menu == self.NEW_GAME:
			self.surface = self.__get_menu_new_game()
			self.widgets = self.__get_widgets_new_game()
		else:
			print("[qwirkle.py]Menu.get_surface:\x1b[91m Unknown menu is set, defaulting to empty.\x1b[97m")
			self.menu = self.EMPTY
			self.surface = self.__get_menu_empty()
			self.widgets = []
		#return the selected menu
		return menu
	
	def get_surface(self):
		"""
		Returns the pygame.Surface object containing the graphics for the current menu
		"""
		return self.surface
	
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
	
	def __get_menu_new_game(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background for the menu
		surf.fill((200, 200, 200))
		#place the menu title
		gui.rendertext(surf, lang.player_selection, int(self.size[1]*.1), None, [int(self.size[0]*.5), int(self.size[1]*.02)], "midtop")
		
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
		#settings button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.5)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], None, lang.settings)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#exit button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.6)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], full_quit, lang.exit)
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
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.MAIN), lang.back)
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
	clock = pygame.time.Clock()
	loop = True
	rtrn = None
	selected = None
	surface = pygame.Surface([0, 0])
	update = []
	widgets = []
	
	# window setup #
	window = pygame.display.set_mode(user.winsize)
	pygame.display.set_caption(lang.qwirkle)
	
	# menu setup #
	menus = Menu(user.winsize)
	surface = menus.get_surface()
	widgets = menus.get_widgets()
	
	#add the surfaces and widgets to the update list
	update.append(surface)
	update.extend(widgets)
	
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
						#a menu was selected
						if rtrn != None:
							rtrn = None
							update = []
							surface = menus.get_surface()
							widgets = menus.get_widgets()
							update.append(surface)
							update.extend(widgets)
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
			#update a surface
			if type(u) == pygame.Surface:
				window.blit(u, u.get_rect())
			#update a button
			elif type(u) == gui.Button or type(u) == gui.Input:
				window.blit(surface.subsurface(u.get_rect()), u.get_rect())
				u.blit_on(window)
		if len(update) > 0:
			update = []
			pygame.display.update()
	
	#quit the program
	full_quit()
