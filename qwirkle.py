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
	
	def __init__(self, window_size):
		self.size = window_size
		self.menu = self.MAIN
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
		self.menu = menu
		return menu
	
	def get_surface(self):
		"""
		Returns the pygame.Surface object containing the graphics for the current menu
		"""
		if self.menu == self.EMPTY:
			surf = self.__get_menu_empty()
		elif self.menu == self.MAIN:
			surf = self.__get_menu_main()
		else:
			print("[qwirkle.py]Menu.get_surface:\x1b[91m Unknown menu is set, defaulting to empty.\x1b[97m")
			surf = self.__get_menu_empty()
		
		#return the pygame.Surface object
		return surf
	
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
	
	def get_widgets(self):
		"""
		Returns the Widget objects for the current menu
		"""
		if self.menu == self.EMPTY:
			widgets = []
		elif self.menu == self.MAIN:
			widgets = self.__get_widgets_main()
		else:
			print("[qwirkle.py]Menu.get_widgets:\x1b[91m Unknown menu is set, defaulting to empty.\x1b[97m")
			widgets = []
		
		return widgets
	
	def __get_widgets_main(self):
		#initialize a list of widgets
		widgets = []
		
		# button templates #
		#button dimensions
		btn_size = [int(self.size[0] * .24), int(self.size[1] * .08)]
		btn_edge_size = int(min(self.size) * .004)
		#templates
		btn_unavailable = gui.rectangle(btn_size, (102, 102, 102), btn_edge_size, (61, 61, 61))
		btn_idle = gui.rectangle(btn_size, (34, 85, 170), btn_edge_size, (0, 44, 121))
		btn_hover = gui.rectangle(btn_size, (146, 178, 255), btn_edge_size, (34, 85, 170))
		btn_active = gui.rectangle(btn_size, (0, 44, 121), btn_edge_size, (34, 85, 170))
		
		# button objects #
		#new game button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+btn_size), [int(self.size[0]*.5), int(self.size[1]*.4)], "center")
		btn = button_builder(btnRect, [btn_unavailable.copy(), btn_idle.copy(), btn_hover.copy(), btn_active.copy()], None, lang.new_game)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#settings button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+btn_size), [int(self.size[0]*.5), int(self.size[1]*.5)], "center")
		btn = button_builder(btnRect, [btn_unavailable.copy(), btn_idle.copy(), btn_hover.copy(), btn_active.copy()], None, lang.settings)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#exit button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+btn_size), [int(self.size[0]*.5), int(self.size[1]*.6)], "center")
		btn = button_builder(btnRect, [btn_unavailable.copy(), btn_idle.copy(), btn_hover.copy(), btn_active.copy()], full_quit, lang.exit)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets



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
	#define the button object with the correct dimensions
	button = gui.Button(rect.size)
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
	surface = pygame.Surface([0, 0])
	update = []
	widgets = []
	
	# window setup #
	window = pygame.display.set_mode(user.winsize)
	pygame.display.set_caption(lang.qwirkle)
	#add a seperate layer for widgets
	widget_layer = pygame.Surface(user.winsize)
	widget_layer.set_colorkey((0, 0, 0))
	
	# menu setup #
	menus = Menu(user.winsize)
	surface = menus.get_surface()
	widgets = menus.get_widgets()
	
	#add the surfaces and widgets to the update list
	update.append(surface)
	update.extend(widgets)
	update.append(widget_layer)
	
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
					if w.get_current_state() == gui.Widget.HOVER:
						w.set_current_state(gui.Widget.ACTIVE)
						update.append(w)
			if event.type == pygame.MOUSEBUTTONUP:
				for w in widgets:
					if w.get_current_state() == gui.Widget.ACTIVE:
						if type(w) == gui.Button:
							w.run_function()
						w.set_current_state(gui.Widget.HOVER)
						update.append(w)
		
		#look whether the mouse was moved
		mouse_move = pygame.mouse.get_rel()
		if mouse_move != (0, 0):
			for w in widgets:
				#check whether the widget is being hovered over (and the widget is set to idle)
				if w.get_rect().collidepoint(pygame.mouse.get_pos()) and w.get_current_state() == gui.Widget.IDLE:
					w.set_current_state(gui.Widget.HOVER)
					update.append(w)
				#check whether the widget is not being hovered over (and this has not been set)
				elif not w.get_rect().collidepoint(pygame.mouse.get_pos()) and (w.get_current_state() == gui.Widget.HOVER or w.get_current_state() == gui.Widget.ACTIVE):
					w.set_current_state(gui.Widget.IDLE)
					update.append(w)
		
		#update the display
		for u in update:
			#update a surface
			if type(u) == pygame.Surface:
				window.blit(u, u.get_rect())
			#update a button
			elif type(u) == gui.Button:
				pygame.draw.rect(widget_layer, (0, 0, 0), u.get_rect())
				u.blit_on(widget_layer)
				#add the widget layer to the end of the update list
				if update[-1] != widget_layer:
					update.append(widget_layer)
		if len(update) > 0:
			update = []
			pygame.display.update()
	
	#quit the program
	full_quit()
