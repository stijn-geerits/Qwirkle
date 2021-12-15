#!/usr/bin/env python3

# import classes #
import inspect, json, os, pygame, sys



### Global variables ###
# global constants #
CLASSESDIR = "Classes/"
CONFIGDIR = ""
GRAPHICSDIR = "Graphics/"
LANGUAGEDIR = "Lang/"
THEMESDIR = "Themes/"
#insert the CLASSESDIR into the search list for importing scripts
sys.path.insert(1, CLASSESDIR)
#import the custom classes
import gui; from game import Game; from player import Player; from tile import Tile



### Classes ###
# Container for storing and retreiving user config files #
class User:
	def __init__(self):
		file = open(CONFIGDIR + "user.conf", 'r')
		content = file.read()
		file.close()
		for line in content.splitlines():
			if not (line.strip().startswith('#') or line.strip() == ''):
				exec("self." + line)
		return
	
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
class Lang:
	def __init__(self):
		file = open(LANGUAGEDIR + user.lang + ".lang", 'r')
		content = file.read()
		file.close()
		for line in content.splitlines():
			if not (line.strip().startswith('#') or line.strip() == ''):
				exec("self." + line)
		return

# Container for storing color theme data #
class Color:
	def __init__(self):
		file = open(THEMESDIR + user.theme + ".theme", 'r')
		content = file.read()
		file.close()
		for line in content.splitlines():
			if not (line.strip().startswith('#') or line.strip() == ''):
				exec("self." + line)
		return

# Container for all menu data #
class Menu:
	"""
	Manager for all menus for Qwirkle
	"""
	#possible menu values
	EMPTY = 0
	MAIN = 1
	NEW_GAME = 2
	RULES = 3
	SETTINGS = 4
	WAIT_PLAYER = 5
	GAME = 6
	GAME_OVER = 7
	PAUSE = 8
	
	def __init__(self, window_size):
		self.size = window_size
		#set the widget templates
		self.__set_widget_templates()
		#initialize the main menu
		self.menu = self.MAIN
		self.select_menu(self.MAIN)
		#initialize a variable for all sort of menu data
		self.data = {}
		return
	
	def __set_widget_templates(self):
		# selector templates #
		#selector dimensions
		self.sltr_size = [int(self.size[0] * .24), int(self.size[1] * .08)]
		sltr_edge_size = int(min(self.size) * .004)
		#selector template
		sltr_unavailable = gui.rectangle(self.sltr_size, color.selector_fill, sltr_edge_size, color.selector_edge)
		sltr_idle = sltr_unavailable.copy()
		sltr_hover = sltr_unavailable.copy()
		sltr_active = sltr_unavailable.copy()
		self.selector_template = [sltr_unavailable, sltr_idle, sltr_hover, sltr_active]
		
		# button templates #
		#button dimensions
		self.btn_size = [int(self.size[0] * .24), int(self.size[1] * .08)]
		btn_edge_size = int(min(self.size) * .004)
		#button template
		btn_unavailable = gui.rectangle(self.btn_size, color.button_unavailable_fill, btn_edge_size, color.button_unavailable_edge)
		btn_idle = gui.rectangle(self.btn_size, color.button_idle_fill, btn_edge_size, color.button_idle_edge)
		btn_hover = gui.rectangle(self.btn_size, color.button_hover_fill, btn_edge_size, color.button_hover_edge)
		btn_active = gui.rectangle(self.btn_size, color.button_active_fill, btn_edge_size, color.button_active_edge)
		self.button_template = [btn_unavailable, btn_idle, btn_hover, btn_active]
		#small button dimensions
		self.btn_small_size = [self.btn_size[1]] * 2
		#small button template
		btn_unavailable = gui.rectangle(self.btn_small_size, color.button_unavailable_fill, btn_edge_size, color.button_unavailable_edge)
		btn_idle = gui.rectangle(self.btn_small_size, color.button_idle_fill, btn_edge_size, color.button_idle_edge)
		btn_hover = gui.rectangle(self.btn_small_size, color.button_hover_fill, btn_edge_size, color.button_hover_edge)
		btn_active = gui.rectangle(self.btn_small_size, color.button_active_fill, btn_edge_size, color.button_active_edge)
		self.button_small_template = [btn_unavailable, btn_idle, btn_hover, btn_active]
		#game button dimensions
		self.btn_game_size = [120, 40]
		#game button template
		btn_unavailable = gui.rectangle(self.btn_game_size, color.button_unavailable_fill, btn_edge_size, color.button_unavailable_edge)
		btn_idle = gui.rectangle(self.btn_game_size, color.button_idle_fill, btn_edge_size, color.button_idle_edge)
		btn_hover = gui.rectangle(self.btn_game_size, color.button_hover_fill, btn_edge_size, color.button_hover_edge)
		btn_active = gui.rectangle(self.btn_game_size, color.button_active_fill, btn_edge_size, color.button_active_edge)
		self.button_game_template = [btn_unavailable, btn_idle, btn_hover, btn_active]
		#confirm button dimensions
		self.btn_confirm_size = [int(self.btn_game_size[0]*2.2), 44]
		#confirm button template
		btn_unavailable = gui.rectangle(self.btn_confirm_size, color.confirm_unavailable_fill, btn_edge_size, color.confirm_unavailable_edge)
		btn_idle = gui.rectangle(self.btn_confirm_size, color.confirm_idle_fill, btn_edge_size, color.confirm_idle_edge)
		btn_hover = gui.rectangle(self.btn_confirm_size, color.confirm_hover_fill, btn_edge_size, color.confirm_hover_edge)
		btn_active = gui.rectangle(self.btn_confirm_size, color.confirm_active_fill, btn_edge_size, color.confirm_active_edge)
		self.button_confirm_template = [btn_unavailable, btn_idle, btn_hover, btn_active]
		
		# input templates #
		#input dimensions
		self.input_size = [int(self.size[0] * .48), int(self.size[1] * .08)]
		input_edge_size = int(min(self.size) * .004)
		#input template
		input_unavailable = gui.rectangle(self.input_size, color.input_unavailable_fill, input_edge_size, color.input_unavailable_edge)
		input_idle = gui.rectangle(self.input_size, color.input_idle_fill, input_edge_size, color.input_idle_edge)
		input_hover = gui.rectangle(self.input_size, color.input_hover_fill, input_edge_size, color.input_hover_edge)
		input_active = gui.rectangle(self.input_size, color.input_active_fill, input_edge_size, color.input_active_edge)
		self.input_template = [input_unavailable, input_idle, input_hover, input_active]
		return
	
	def get_menu(self):
		"""
		Returns the currently selected menu
		"""
		return self.menu
	
	def select_menu(self, menu, came_from=MAIN):
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
		elif menu == self.NEW_GAME:
			self.background = self.__get_menu_new_game()
			self.widgets = self.__get_widgets_new_game()
		elif menu == self.RULES:
			self.background = self.__get_menu_rules()
			self.widgets = self.__get_widgets_rules(came_from)
		elif menu == self.SETTINGS:
			self.background = self.__get_menu_settings()
			self.widgets = self.__get_widgets_settings()
		elif menu == self.WAIT_PLAYER:
			self.background = self.__get_menu_wait_player()
			self.widgets = self.__get_widgets_wait_player()
		elif menu == self.GAME:
			self.background = self.__get_menu_game()
			self.widgets = self.__get_widgets_game()
		elif menu == self.GAME_OVER:
			self.background = self.__get_menu_game_over()
			self.widgets = self.__get_widgets_game_over()
		elif menu == self.PAUSE:
			self.background = self.__get_menu_pause(came_from)
			self.widgets = self.__get_widgets_pause(came_from)
		else:
			print("[qwirkle.py]Menu.get_background:\x1b[91m Unknown menu is set, defaulting to empty.\x1b[00m")
			menu = self.select_menu(self.EMPTY)
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
		surf.fill(color.alpha)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_main(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		if gui.is_rgb(color.background_main):
			surf.fill(color.background_main)
		else:
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_main), self.size)
			surf.blit(bg, [0, 0])
		#place the qwirkle title graphic
		gui.renderimage(surf, GRAPHICSDIR + "qwirkle.png", [int(self.size[0]*.5), int(self.size[1]*.05)], "midtop")
		#place the copyright notice
		gui.rendertext(surf, lang.copyright, int(self.size[1]*.03), None, [int(self.size[0]*.5), int(self.size[1]*.97)], "midbottom", color.text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_new_game(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		if gui.is_rgb(color.background_new_game):
			surf.fill(color.background_new_game)
		else:
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_new_game), self.size)
			surf.blit(bg, [0, 0])
		#place the menu title
		gui.rendertext(surf, lang.player_selection, int(self.size[1]*.1), None, [int(self.size[0]*.5), int(self.size[1]*.02)], "midtop", color.text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_rules(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		if gui.is_rgb(color.background_rules):
			surf.fill(color.background_rules)
		else:
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_rules), self.size)
			surf.blit(bg, [0, 0])
		#place the menu title
		gui.rendertext(surf, lang.rules, int(self.size[1]*.1), None, [int(self.size[0]*.5), int(self.size[1]*.02)], "midtop", color.text)
		#place the rules text
		gui.rendertext(surf, lang.rules_text, int(self.size[1]*.04), None, [int(self.size[0]*.02), int(self.size[1]*.11)], color=color.text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_settings(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		if gui.is_rgb(color.background_settings):
			surf.fill(color.background_settings)
		else:
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_settings), self.size)
			surf.blit(bg, [0, 0])
		#place the menu title
		gui.rendertext(surf, lang.settings, int(self.size[1]*.1), None, [int(self.size[0]*.5), int(self.size[1]*.02)], "midtop", color.text)
		
		#render the text for selecting the resolution
		gui.rendertext(surf, lang.select_resolution, self.sltr_size[1]-4, None, [int(self.size[0]*.02), int(self.size[1]*.2)], "midleft", color.text)
		gui.rendertext(surf, lang.resolution_warning, self.sltr_size[1]//2, None, [int(self.size[0]*.02), int(self.size[1]*.22)], "topleft", color.text)
		#render the text for selecting the framerate
		gui.rendertext(surf, lang.select_framerate, self.sltr_size[1]-4, None, [int(self.size[0]*.02), int(self.size[1]*.3)], "midleft", color.text)
		#render the text for selecting the language
		gui.rendertext(surf, lang.select_lang, self.sltr_size[1]-4, None, [int(self.size[0]*.02), int(self.size[1]*.4)], "midleft", color.text)
		#render the text for selecting the theme
		gui.rendertext(surf, lang.select_theme, self.sltr_size[1]-4, None, [int(self.size[0]*.02), int(self.size[1]*.5)], "midleft", color.text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_wait_player(self):
		#get the surface for the game menu
		surf = self.__get_menu_game()
		#prepare a layer for the widgets
		w_layer = pygame.Surface(self.size)
		w_layer.fill(color.alpha)
		w_layer.set_colorkey(color.alpha)
		#draw the widgets on the surface
		widgets = self.__get_widgets_game()
		for w in widgets:
			w.blit_on(w_layer)
		#draw the widgets layer on the surface
		surf.blit(w_layer, [0, 0])
		
		#create a semi transparent overlay
		overlay = pygame.Surface(surf.get_size())
		overlay.fill(color.alpha)
		overlay.set_alpha(204)
		#draw the overlay
		surf.blit(overlay, [0, 0])
		#render the text announcing the next player
		gui.rendertext(surf, lang.player_on_hand %(self.data["game"].get_player_on_hand().get_name()), int(self.size[1]*.1), None, [self.size[0]//2, self.size[1]//2], "center", color.player_text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_game(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		if gui.is_rgb(color.background_game):
			surf.fill(color.background_game)
		else:
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_game), self.size)
			surf.blit(bg, [0, 0])
		
		#get the player data
		players = self.data["game"].get_players()
		player_count = len(players)
		active_player = players.index(self.data["game"].get_player_on_hand())
		
		#draw a grid for the playing field
		field_size = [(self.size[0]-int(self.btn_game_size[0]*2.3)-32)//36, (self.size[1]-32)//36]
		grid = gui.grid([36]*field_size[1], [36]*field_size[0], color.grid_edge, color.grid_fill)
		surf.blit(grid, gui.set_relpos(grid.get_rect(), [(self.size[0]-int(self.btn_game_size[0]*2.3))//2, self.size[1]//2], "center"))
		#draw the game field
		gridRect = gui.set_relpos(grid.get_rect(), [(self.size[0]-int(self.btn_game_size[0]*2.3))//2, self.size[1]//2], "center")
		for y in range(field_size[1]):
			for x in range(field_size[0]):
				surf.blit(self.data["game"].get_field([x, y]).get_image(), [gridRect.left + (x * 35) + 2, gridRect.top + (y * 35) + 2])
		#store the pygame.Rect object of the playing field grid for future reference
		self.data["field"] = gridRect
		
		#draw a line as section between playing field and user interactibles
		pygame.draw.aaline(surf, color.grid_edge, [self.size[0]-int(self.btn_game_size[0]*2.3), 0], [self.size[0]-int(self.btn_game_size[0]*2.3), self.size[1]])
		
		#draw the scoreboard
		gui.rendertext(surf, lang.score, 32, None, [self.size[0]-int(self.btn_game_size[0]*1.15), int(self.size[1]*.04)], "midtop", color.text)
		grid = gui.grid([32]*player_count, [int(self.btn_game_size[0]*1.6), 48], color.grid_edge, [color.grid_fill]*2*active_player+[color.player_on_hand]*2+[color.grid_fill]*2*(player_count-active_player-1))
		gridpos = [self.size[0]-int(self.btn_game_size[0]*1.15)-(grid.get_width()//2), int(self.size[1]*.04)+24]
		surf.blit(grid, gridpos)
		#draw the players and their scores
		for p in range(player_count):
			gui.rendertext(surf, players[p].get_name(), 24, None, [gridpos[0]+2, gridpos[1]+(p*31)+16], "midleft", color.text)
			gui.rendertext(surf, str(int(self.data["game"].get_player_score(players[p].get_id()))), 24, None, [gridpos[0]+grid.get_width()-2, gridpos[1]+(p*31)+16], "midright", color.text)
		
		#render the amount of tiles in the bag
		gui.rendertext(surf, lang.tiles_in_bag %(self.data["game"].get_tiles_left()), 24, None, [self.size[0]-int(self.btn_game_size[0]*1.15), int(self.size[1]*.55)], "center", color.text)
		#draw a grid for the bag
		grid = gui.grid([36]*2, [36]*3, color.grid_edge, color.grid_fill)
		surf.blit(grid, [self.size[0]-int(self.btn_game_size[0]*1.15)-(grid.get_width()//2), int(self.size[1]*.6)])
		#store the pygame.Rect object of the bag grid for future reference
		self.data["bag"] = grid.get_rect().move([self.size[0]-int(self.btn_game_size[0]*1.15)-(grid.get_width()//2), int(self.size[1]*.6)])
		
		#draw a grid for the hand
		grid = gui.grid([36], [36]*6, color.grid_edge, color.grid_fill)
		surf.blit(grid, [self.size[0]-int(self.btn_game_size[0]*1.15)-(grid.get_width()//2), self.size[1]-48])
		#draw the tiles in the hand
		gridRect = grid.get_rect().move([self.size[0]-int(self.btn_game_size[0]*1.15)-(grid.get_width()//2), self.size[1]-48])
		for tile in range(len(self.data["tiles"])):
			surf.blit(self.data["tiles"][tile].get_image(), [gridRect.left + (tile * 35) + 2, gridRect.top + 2])
			#also set the location of the tiles
			self.data["tiles"][tile].set_position([gridRect.left + (tile * 35) + 2, gridRect.top + 2])
		#store the pygame.Rect object of the hand grid for future reference
		self.data["hand"] = gridRect
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_game_over(self):
		#get the surface for the game menu
		surf = self.__get_menu_game()
		#prepare a layer for the widgets
		w_layer = pygame.Surface(self.size)
		w_layer.fill(color.alpha)
		w_layer.set_colorkey(color.alpha)
		#draw the widgets on the surface
		widgets = self.__get_widgets_game()
		for w in widgets:
			w.blit_on(w_layer)
		#draw the widgets layer on the surface
		surf.blit(w_layer, [0, 0])
		
		#create a semi transparent overlay
		overlay = pygame.Surface(surf.get_size())
		overlay.fill(color.alpha)
		overlay.set_alpha(204)
		#draw the overlay
		surf.blit(overlay, [0, 0])
		
		#render the text announcing the game is over
		gui.rendertext(surf, lang.game_over, int(self.size[1]*.1), None, [self.size[0]//2, self.size[1]//2], "midbottom", color.player_text)
		#render the text announcing the winner
		gui.rendertext(surf, lang.winner %(self.data["game"].get_winning_player().get_name()), int(self.size[1]*.05), None, [self.size[0]//2, self.size[1]//2], "midtop", color.player_text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_pause(self, prev_menu):
		#get the data for the previous menu
		if prev_menu == self.EMPTY:
			surf = self.__get_menu_empty()
			widgets = []
		elif prev_menu == self.MAIN:
			surf = self.__get_menu_main()
			widgets = self.__get_widgets_main()
		elif prev_menu == self.NEW_GAME:
			surf = self.__get_menu_new_game()
			widgets = self.__get_widgets_new_game()
		elif prev_menu == self.RULES:
			surf = self.__get_menu_rules()
			widgets = self.__get_widgets_rules()
		elif prev_menu == self.SETTINGS:
			surf = self.__get_menu_settings()
			widgets = self.__get_widgets_settings()
		elif prev_menu == self.WAIT_PLAYER:
			surf = self.__get_menu_wait_player()
			widgets = self.__get_widgets_wait_player()
		elif prev_menu == self.GAME:
			surf = self.__get_menu_game()
			widgets = self.__get_widgets_game()
		elif prev_menu == self.GAME_OVER:
			surf = self.__get_menu_game_over()
			widgets = self.__get_widgets_game_over()
		else:
			print("[qwirkle.py]Menu.__get_menu_pause:\x1b[91m Internal error, unknown previous menu passed.\x1b[00m")
			surf = pygame.Surface(self.size)
			widgets = []
		#prepare a layer for the widgets
		w_layer = pygame.Surface(self.size)
		w_layer.fill(color.alpha)
		w_layer.set_colorkey(color.alpha)
		#draw the widgets on the surface
		for w in widgets:
			w.blit_on(w_layer)
		#draw the widgets layer on the surface
		surf.blit(w_layer, [0, 0])
		
		#create a semi transparent overlay
		overlay = pygame.Surface(surf.get_size())
		overlay.fill(color.alpha)
		overlay.set_alpha(204)
		#draw the overlay
		surf.blit(overlay, [0, 0])
		
		#render the pause text
		gui.rendertext(surf, lang.pause, int(self.size[1]*.1), None, [self.size[0]//2, int(self.size[1]*.2)], "center", color.player_text)
		
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
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.NEW_GAME), lang.new_game, color.text)
		widgets.append(btn)
		#rules button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.5)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.RULES), lang.rules, color.text)
		widgets.append(btn)
		#settings button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.6)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.SETTINGS), lang.settings, color.text)
		widgets.append(btn)
		#exit button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.7)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], full_quit, lang.exit, color.text)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_new_game(self):
		#initialize a list of widgets
		widgets = []
		
		# button objects #
		#add player button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.75), int(self.size[1]*.15)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_small_template], self.__add_input, lang.add, color.text)
		widgets.append(btn)
		#remove player button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.75), int(self.size[1]*.25)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_small_template], self.__remove_input, lang.subtract, color.text)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#back button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.3), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.MAIN), lang.back, color.text)
		widgets.append(btn)
		#start button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.7), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], self.__init_game, lang.start_game, color.text)
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
	
	def __get_widgets_rules(self, go_to=MAIN):
		#initialize a list of widgets
		widgets = []
		
		# button objects #
		#back button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(go_to), lang.back, color.text)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_settings(self):
		#initialize a list of widgets
		widgets = []
		
		# selector objects #
		#resolution selector
		resolutions = ["800x600", "1024x768", "1280x720", "1280x800", "1280x1024", "1440x900", "1680x1050", "1920x1080"]
		sltrRect = gui.set_relpos(pygame.Rect([0, 0]+self.sltr_size), [int(self.size[0]*.8), int(self.size[1]*.2)], "center")
		sltr = selector_builder(sltrRect, [t.copy() for t in self.selector_template], resolutions, resolutions.index('x'.join([str(s) for s in user.winsize])), updater=lambda:self.__update_settings(0))
		widgets.append(sltr)
		#fps selector
		framerate = ["30", "60", "75", "120", "144", "240"]
		sltrRect = gui.set_relpos(pygame.Rect([0, 0]+self.sltr_size), [int(self.size[0]*.8), int(self.size[1]*.3)], "center")
		sltr = selector_builder(sltrRect, [t.copy() for t in self.selector_template], framerate, framerate.index(str(user.fps)), updater=lambda:self.__update_settings(1))
		widgets.append(sltr)
		#lang selector
		langs = []
		for l in os.listdir(LANGUAGEDIR):
			if l.endswith(".lang"):
				langs.append(l[:l.rfind('.')])
		sltrRect = gui.set_relpos(pygame.Rect([0, 0]+self.sltr_size), [int(self.size[0]*.8), int(self.size[1]*.4)], "center")
		sltr = selector_builder(sltrRect, [t.copy() for t in self.selector_template], langs, langs.index(user.lang), updater=lambda:self.__update_settings(2))
		widgets.append(sltr)
		#theme selector
		themes = []
		for t in os.listdir(THEMESDIR):
			if t.endswith(".theme"):
				themes.append(t[:t.rfind('.')])
		sltrRect = gui.set_relpos(pygame.Rect([0, 0]+self.sltr_size), [int(self.size[0]*.8), int(self.size[1]*.5)], "center")
		sltr = selector_builder(sltrRect, [t.copy() for t in self.selector_template], themes, themes.index(user.theme), updater=lambda:self.__update_settings(3))
		widgets.append(sltr)
		
		# button objects #
		#previous resolution button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.8)-(self.sltr_size[0]//2), int(self.size[1]*.2)], "midright")
		btn = button_builder(btnRect,  [t.copy() for t in self.button_small_template], widgets[0].select_previous, '<', color.text)
		widgets.append(btn)
		#next resolution button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.8)+(self.sltr_size[0]//2), int(self.size[1]*.2)], "midleft")
		btn = button_builder(btnRect,  [t.copy() for t in self.button_small_template], widgets[0].select_next, '>', color.text)
		widgets.append(btn)
		#previous framerate button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.8)-(self.sltr_size[0]//2), int(self.size[1]*.3)], "midright")
		btn = button_builder(btnRect,  [t.copy() for t in self.button_small_template], widgets[1].select_previous, '<', color.text)
		widgets.append(btn)
		#next framerate button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.8)+(self.sltr_size[0]//2), int(self.size[1]*.3)], "midleft")
		btn = button_builder(btnRect,  [t.copy() for t in self.button_small_template], widgets[1].select_next, '>', color.text)
		widgets.append(btn)
		#previous lang button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.8)-(self.sltr_size[0]//2), int(self.size[1]*.4)], "midright")
		btn = button_builder(btnRect,  [t.copy() for t in self.button_small_template], widgets[2].select_previous, '<', color.text)
		widgets.append(btn)
		#next lang button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.8)+(self.sltr_size[0]//2), int(self.size[1]*.4)], "midleft")
		btn = button_builder(btnRect,  [t.copy() for t in self.button_small_template], widgets[2].select_next, '>', color.text)
		widgets.append(btn)
		#previous theme button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.8)-(self.sltr_size[0]//2), int(self.size[1]*.5)], "midright")
		btn = button_builder(btnRect,  [t.copy() for t in self.button_small_template], widgets[3].select_previous, '<', color.text)
		widgets.append(btn)
		#next theme button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_small_size), [int(self.size[0]*.8)+(self.sltr_size[0]//2), int(self.size[1]*.5)], "midleft")
		btn = button_builder(btnRect,  [t.copy() for t in self.button_small_template], widgets[3].select_next, '>', color.text)
		widgets.append(btn)
		#apply and restart button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.85)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.__save_settings(True), lang.apply_restart, color.text)
		widgets.append(btn)
		#apply button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], self.__save_settings, lang.apply, color.text)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_wait_player(self):
		#initialize the list of widgets
		widgets = []
		
		# button objects #
		#confirm button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_confirm_size), [self.size[0]-int(self.btn_game_size[0]*1.15), self.size[1]-8], "midbottom")
		btn = button_builder(btnRect, [t.copy() for t in self.button_confirm_template], lambda:self.select_menu(self.GAME), lang.confirm, color.text)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_game(self):
		#initialize the list of widgets
		widgets = []
		
		# button objects #
		#cancel button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_game_size), [self.size[0]-int(self.btn_game_size[0]*.6), self.size[1]-78], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_game_template], self.__cancel, lang.cancel, color.text)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#play button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_game_size), [self.size[0]-int(self.btn_game_size[0]*1.7), self.size[1]-78], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_game_template], self.__play, lang.play, color.text)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#trade/skip button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_game_size), [self.size[0]-int(self.btn_game_size[0]*1.15), int(self.size[1]*.6+self.btn_game_size[1]*2.4)], "center")
		if self.data["game"].get_tiles_left() > 0:
			btn = button_builder(btnRect, [t.copy() for t in self.button_game_template], self.__trade, lang.trade, color.text)
			btn.set_current_state(gui.Widget.UNAVAILABLE)
		else:
			btn = button_builder(btnRect, [t.copy() for t in self.button_game_template], self.__skip, lang.skip, color.text)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_game_over(self):
		#initialize the list of widgets
		widgets = []
		
		# button objects #
		#confirm button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_confirm_size), [self.size[0]-int(self.btn_game_size[0]*1.15), self.size[1]-8], "midbottom")
		btn = button_builder(btnRect, [t.copy() for t in self.button_confirm_template], lambda:self.select_menu(self.MAIN), lang.end_game, color.text)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_pause(self, prev_menu):
		#initialize the list of widgets
		widgets = []
		
		# button objects #
		#continue button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [self.size[0]//2, self.size[1]//2], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(prev_menu), lang.go_on, color.text)
		widgets.append(btn)
		#rules button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [self.size[0]//2, int(self.size[1]*.6)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.RULES, self.GAME), lang.rules, color.text)
		widgets.append(btn)
		#main menu button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [self.size[0]//2, int(self.size[1]*.7)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.MAIN), lang.to_main, color.text)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __update_settings(self, update):
		#grab the globals
		global user, lang, color
		#grab the set settings
		setting = 0
		for w in self.widgets:
			if type(w) == gui.Selector:
				#the screen resolution is updated
				if setting == 0 and update == 0:
					user.winsize = [int(s) for s in w.get_selected().split('x')]
				#the framerate is updated
				elif setting == 1 and update == 1:
					user.fps = int(w.get_selected())
				#the language is updated
				elif setting == 2 and update == 2:
					user.lang = w.get_selected()
					lang = Lang()
					self.select_menu(self.menu)
				#the theme is updated
				elif setting == 3 and update == 3:
					user.theme = w.get_selected()
					color = Color()
					self.__set_widget_templates()
					self.select_menu(self.menu)
				setting += 1
		return update
	
	def __save_settings(self, restart=False):
		#grab the config global
		global user
		#open the user config file
		file = open(CONFIGDIR + "user.conf", 'w')
		#write the new user config
		file.write(user.get_config())
		#close the user config file
		file.close()
		#restart the game
		if restart:
			os.execv(sys.executable, ["python"] + sys.argv)
		#go to the main menu
		else:
			self.select_menu(self.MAIN)
		#return with an exit code of 0
		return 0
	
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
	
	def __init_game(self):
		# player objects #
		#initialize a list for the players
		players = []
		#create the player objects
		for w in self.widgets:
			if type(w) == gui.Input:
				players.append(Player(len(players), w.get_value()))
		
		# game object #
		#initialize the game variable
		self.data["game"] = Game(players, Tileset(GRAPHICSDIR + "tiles.png", 32, True))
		
		# tile objects #
		#get the tiles for the player on hand
		self.data["tiles"] = self.data["game"].get_player_on_hand().get_hand()
		
		#switch the menu to wait for player
		return self.select_menu(self.WAIT_PLAYER)
	
	def grab_tile(self, mouse_pos):
		"""
		Grab an available tile object on the surface
		
		Returns None if the mouse does not select a tile
		"""
		#check all player tiles
		for tile in self.data["tiles"]:
			#check whether the tile is selected
			if tile.get_rect().collidepoint(mouse_pos):
				#fill in the are where the tile was
				self.background.fill(color.grid_fill, tile.get_rect())
				#store the current position of the tile
				self.data["oldpos"] = tile.get_position()
				#return the tile object
				return tile
		#no tile selected
		return None
	
	def drop_tile(self, tile):
		"""
		Drop a tile at the current position
		"""
		#check whether the tile is on a valid grid
		for grid in ["field", "bag", "hand"]:
			#get the pygame.Rect object for the grid
			gridRect = self.data[grid].copy()
			#decrease grid dimensions by 1 (to prevent dropping tiles outside the bottom or right edge of the grid)
			gridRect.height -= 1
			gridRect.width -= 1
			#the tile is on the grid
			if gridRect.collidepoint(tile.get_rect().center):
				#calculate the new position for the tile
				xTile = (tile.get_rect().centerx - gridRect.left) // 35
				yTile = (tile.get_rect().centery - gridRect.top) // 35
				#look whether the space is occupied by a different tile
				search = self.data["tiles"].copy()
				search.remove(tile)
				for s in search:
					#the current tile is at the requested grid position
					if s.get_position() == [gridRect.left + (xTile * 35) + 2, gridRect.top + (yTile * 35) + 2]:
						#swap the positions of the current and active tile
						s.set_position(self.data["oldpos"])
						tile.set_position([gridRect.left + (xTile * 35) + 2, gridRect.top + (yTile * 35) + 2])
						self.background.blit(s.get_image(), s.get_rect())
						self.background.blit(tile.get_image(), tile.get_rect())
						return
				#if the space in the bag or hand is not occupied
				if grid == "bag" or grid == "hand":
					#place the tile in the grid
					tile.set_position([gridRect.left + (xTile * 35) + 2, gridRect.top + (yTile * 35) + 2])
					self.background.blit(tile.get_image(), tile.get_rect())
					#update the button states
					self.__update_widgets_game()
					return
				#the tile is on an empty space in the field
				elif grid == "field" and self.data["game"].get_field([xTile, yTile]).get_shape() == "empty":
					#place the tile in the grid
					tile.set_position([gridRect.left + (xTile * 35) + 2, gridRect.top + (yTile * 35) + 2])
					self.background.blit(tile.get_image(), tile.get_rect())
					#update the button states
					self.__update_widgets_game()
					return
		#the tile is not on a grid
		tile.set_position(self.data["oldpos"])
		self.background.blit(tile.get_image(), tile.get_rect())
		return
	
	def __update_widgets_game(self):
		if self.menu != self.GAME:
			print("[qwirkle.py]Menu.__update_widgets_game:\x1b[91m Internal error. Called with wrong menu set.\x1b[00m")
			return
		#search for the widgets that need to be updated
		for w in self.widgets:
			if type(w) != gui.Button:
				continue
			#cancel button
			if w.get_label() == lang.cancel:
				#only disable the button when all tiles are in hand
				disable = True
				for tile in self.data["tiles"]:
					if tile.get_rect().colliderect(self.data["field"]) or tile.get_rect().colliderect(self.data["bag"]):
						disable = False
				if disable:
					w.set_current_state(gui.Widget.UNAVAILABLE)
				else:
					w.set_current_state(gui.Widget.IDLE)
			#play button
			elif w.get_label() == lang.play:
				#only disable the button when no tiles are on the field
				disable = True
				for tile in self.data["tiles"]:
					if tile.get_rect().colliderect(self.data["field"]):
						disable = False
				if disable:
					w.set_current_state(gui.Widget.UNAVAILABLE)
				else:
					w.set_current_state(gui.Widget.IDLE)
			#trade button
			elif w.get_label() == lang.trade:
				#only disable the button when no tiles are in the bag (both visual and technical bag)
				disable = True
				for tile in self.data["tiles"]:
					if tile.get_rect().colliderect(self.data["bag"]):
						disable = False
				if disable and self.data["game"].get_tiles_left() > 0:
					w.set_current_state(gui.Widget.UNAVAILABLE)
				else:
					w.set_current_state(gui.Widget.IDLE)
		return
	
	def __cancel(self):
		if self.menu != self.GAME:
			print("[qwirkle.py]Menu.__cancel:\x1b[91m Internal error. Called with wrong menu set.\x1b[00m")
			return
		#search for the tiles that are not in hand
		moved = []
		for tile in self.data["tiles"]:
			#the current tile is on the playing field or bag
			if tile.get_rect().colliderect(self.data["field"]) or tile.get_rect().colliderect(self.data["bag"]):
				#add the tile to the list of moved tiles
				moved.append(tile)
		#move all tiles into available slots in hand
		moving = 0
		for x in range(6):
			pos = [self.data["hand"].left + (x * 35) + 2, self.data["hand"].top + 2]
			#check if the current spot already has a tile
			has_tile = False
			t = self.grab_tile(pos)
			#the spot is emtpy
			if type(t) != Tile:
				#grab the tile, move it to the location and drop it there
				self.grab_tile(moved[moving].get_position())
				moved[moving].set_position(pos)
				self.drop_tile(moved[moving])
				#go to the next tile that needs to be moved
				moving += 1
			else:
				#return the grabbed tile to its place
				self.drop_tile(t)
			#all tiles have been moved
			if moving == len(moved):
				break
		return len(moved)
	
	def __play(self):
		if self.menu != self.GAME:
			print("[qwirkle.py]Menu.__play:\x1b[91m Internal error. Called with wrong menu set.\x1b[00m")
			return
		#search for the tiles that are on the playing field
		played = []
		positions = []
		for tile in self.data["tiles"]:
			#the current tile is on the playing field
			if tile.get_rect().colliderect(self.data["field"]):
				#add the tile to the list with played tiles
				played.append(tile)
				#add the tile position to the list with its positions
				positions.append([(tile.get_position()[0] - self.data["field"].left) // 35, (tile.get_position()[1] - self.data["field"].top) // 35])
		#play the tiles
		failed = self.data["game"].play_tiles(played, positions)
		#test if game is over
		if self.data["game"].get_game_over():
			self.select_menu(self.GAME_OVER)
		#play was correct
		elif not failed:
			#update the tiles
			self.data["tiles"] = self.data["game"].get_player_on_hand().get_hand()
			#go to the wait for player menu
			self.select_menu(self.WAIT_PLAYER)
		else:
			#calculate a pygame.Rect area that always covers the error messages
			fieldRect = self.data["field"].copy()
			rect = pygame.Rect(list(fieldRect.bottomleft) + [fieldRect.width, (self.size[1]-fieldRect.height)//2])
			rect.top += 1
			#redraw the background where the error message will go
			if gui.is_rgb(color.background_game):
				self.background.fill(color.background_game, rect)
			else:
				bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_game), self.size)
				self.background.blit(bg.subsurface(rect), rect.topleft)
			#render the error message
			gui.rendertext(self.background, lang.error_play, 16, None, [fieldRect.centerx, self.size[1]-16], "center", color.error)
		#return the amount of (not) played tiles
		return len(played)
	
	def __trade(self):
		if self.menu != self.GAME:
			print("[qwirkle.py]Menu.__trade:\x1b[91m Internal error. Called with wrong menu set.\x1b[00m")
			return
		#search for the tiles that are on the bag
		trades = []
		for tile in self.data["tiles"]:
			#the current tile is on the bag
			if tile.get_rect().colliderect(self.data["bag"]):
				#add the tile to the list of tiles to trade
				trades.append(tile)
		#trade the tiles
		failed = self.data["game"].switch_tiles(trades)
		#test if game is over
		if self.data["game"].get_game_over():
			self.select_menu(self.GAME_OVER)
		#trade was correct
		elif not failed:
			#update the tiles
			self.data["tiles"] = self.data["game"].get_player_on_hand().get_hand()
			#go to the wait for player menu
			self.select_menu(self.WAIT_PLAYER)
		else:
			#calculate a pygame.Rect area that always covers the error messages
			fieldRect = self.data["field"].copy()
			rect = pygame.Rect(list(fieldRect.bottomleft) + [fieldRect.width, (self.size[1]-fieldRect.height)//2])
			rect.top += 1
			#redraw the background where the error message will go
			if gui.is_rgb(color.background_game):
				self.background.fill(color.background_game, rect)
			else:
				bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_game), self.size)
				self.background.blit(bg.subsurface(rect), rect.topleft)
			#render the error message
			gui.rendertext(self.background, lang.error_trade, 16, None, [fieldRect.centerx, self.size[1]-16], "center", color.error)
		#return the amount of (not) traded tiles
		return len(trades)
	
	def __skip(self):
		if self.menu != self.GAME:
			print("[qwirkle.py]Menu.__skip:\x1b[91m Internal error. Called with wrong menu set.\x1b[00m")
			return
		#go to the next player
		self.data["game"].next_player(True)
		#test if game is over
		if self.data["game"].get_game_over():
			self.select_menu(self.GAME_OVER)
		else:
			#update the tiles
			self.data["tiles"] = self.data["game"].get_player_on_hand().get_hand()
			#go to the wait for player menu
			self.select_menu(self.WAIT_PLAYER)
		#return with code 0
		return 0

# Container for tilesets #
class Tileset:
	"""
	Store and manage tilesets
	"""
	def __init__(self, image, tilesize, use_tilemap=False):
		#Load the tileset image file
		self.tileset = pygame.image.load(image)
		#Set the tile size
		self.tilesize = tilesize
		
		#Load the tilemap
		if use_tilemap:
			#Open the tilemap
			file = open(image[:image.rfind('.')] + ".map", 'r')
			#Interpret the tilemap
			self.tilemap = json.loads(file.read())
			#Close the tilemap
			file.close()
		else:
			self.tilemap = None
		
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
		#Map the tile
		if self.tilemap != None:
			tile = self.tilemap.index(tile)
		
		if tile > 0 and tile < self.tilecount:
			#Return a surface containing the given tile
			return self.tileset.subsurface([(tile % self.tilewidth) * self.tilesize, (tile // self.tilewidth) * self.tilesize, self.tilesize, self.tilesize])
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
		#Map the tile
		if self.tilemap != None:
			tile = self.tilemap.index(tile)
		
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

def selector_builder(rect, states, selections, pre_select=None, rotate=True, updater=None):
	"""
	Returns a fully set up selector object
	"""
	#define the selector object
	if pre_select != None:
		sltr = gui.Selector(selections, pre_select, rotate, updater)
	else:
		sltr = gui.Selector(selections, rotate=rotate, updater=updater)
	#move the selector in place
	sltr.place(rect.topleft)
	#define the selector's states (seperate list into individual arguments using '*')
	sltr.define_states(*states)
	#return the selector object
	return sltr



### Main program ###
if __name__ == "__main__":
	#globals
	global user, lang, color
	user = User()
	lang = Lang()
	color = Color()
	#set variables
	active = None
	background = pygame.Surface(user.winsize)
	clock = pygame.time.Clock()
	loop = True
	rtrn = None
	selected = None
	sprite = None
	sprite_offset = [0, 0]
	sprites_layer = pygame.Surface(user.winsize)
	update = []
	widgets = []
	widgets_layer = pygame.Surface(user.winsize)
	
	# window setup #
	window = pygame.display.set_mode(user.winsize)
	pygame.display.set_caption(lang.qwirkle)
	pygame.display.set_icon(pygame.image.load(GRAPHICSDIR + "icon.png"))
	
	# menu setup #
	menus = Menu(user.winsize)
	background = menus.get_background()
	widgets = menus.get_widgets()
	widgets_layer.fill(color.alpha)
	widgets_layer.set_colorkey(color.alpha)
	sprites_layer.fill(color.alpha)
	sprites_layer.set_colorkey(color.alpha)
	
	#add the surfaces, sprite and widgets to the update list
	update.append(background)
	update.append(sprite)
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
			elif event.type == pygame.KEYDOWN:
				#pause the game
				if event.key == pygame.K_ESCAPE and menus.get_menu() == Menu.GAME:
					#select the pause menu
					menus.select_menu(Menu.PAUSE, menus.get_menu())
					#clear the update list of old updates
					update = []
					#reset the active, selected and sprite
					active = None
					selected = None
					sprite = None
					#get the new menu info
					background = menus.get_background()
					widgets = menus.get_widgets()
					#clear the widgets and sprites layer
					widgets_layer.fill(color.alpha)
					sprites_layer.fill(color.alpha)
					#add the surfaces, sprite and widgets to the update list
					update.append(background)
					update.append(sprite)
					update.extend(widgets)
					update.extend([widgets_layer, sprites_layer])
				#sent pressed keys to input widget
				if type(active) == gui.Input:
					active.type(event)
					update.append(active)
			#check mouse button events
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
				if menus.get_menu() == Menu.GAME:
					sprite = menus.grab_tile(pygame.mouse.get_pos())
				if type(selected) in [gui.Widget, gui.Button, gui.Input]:
					#reset the previously active widget
					if active != None:
						active.set_current_state(gui.Widget.IDLE)
						update.append(active)
					#update the widget state
					selected.set_current_state(gui.Widget.ACTIVE)
					#the selected widget becomes the active widget
					active = selected
					selected = None
					#add the widget to the update list
					update.append(active)
				#deactivate the active widget
				elif type(active) == gui.Input:
					#update the widget state
					active.set_current_state(gui.Widget.IDLE)
					#add the widget to the update list
					update.append(active)
					#reset the active widget
					active = None
				#grab a tile
				elif type(sprite) == Tile:
					sprite_offset = [pygame.mouse.get_pos()[0] - sprite.get_position()[0], pygame.mouse.get_pos()[1] - sprite.get_position()[1]]
			elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
				#deselect a tile
				if type(sprite) == Tile:
					menus.drop_tile(sprite)
					sprite = None
					sprites_layer.fill(color.alpha)
					update.append(sprites_layer)
					#add the widgets to the update list
					update.extend(widgets)
				#deactivate a widget (not inputs)
				if type(active) in [gui.Widget, gui.Button]:
					#run button function
					if type(active) == gui.Button:
						rtrn = active.run_function()
						#set the widget to hover (if it was not set to unavailable)
						if active.get_current_state() != gui.Widget.UNAVAILABLE:
							#update the widget state
							active.set_current_state(gui.Widget.HOVER)
							#the active widget becomes the selected widget
							selected = active
							active = None
							#add the widget to the update list
							update.append(selected)
						else:
							active = None
					else:
						rtrn = None
					#a menu was selected
					if rtrn != None:
						#clear the update list of old updates
						update = []
						#get the new menu info
						background = menus.get_background()
						widgets = menus.get_widgets()
						#clear the widgets and sprites layer
						widgets_layer.fill(color.alpha)
						sprites_layer.fill(color.alpha)
						#add the surfaces, sprite and widgets to the update list
						update.append(background)
						update.append(sprite)
						update.extend(widgets)
						update.extend([widgets_layer, sprites_layer])
					#reset the active widget
					if not active in widgets:
						active = None
					#reset the selected widget
					if not selected in widgets:
						selected = None
		
		#look whether the mouse was moved
		mouse_move = pygame.mouse.get_rel()
		if mouse_move != (0, 0):
			#move the sprite to the mouse cursor
			if type(sprite) == Tile:
				sprite.set_position([pygame.mouse.get_pos()[0] - sprite_offset[0], pygame.mouse.get_pos()[1] - sprite_offset[1]])
				update.append(sprite)
			for w in widgets:
				#check whether the widget is being hovered over (and the widget is set to idle)
				if w.get_rect().collidepoint(pygame.mouse.get_pos()) and w.get_current_state() == gui.Widget.IDLE:
					#make sure to deselect the previously selected widget
					if selected != None:
						selected.set_current_state(gui.Widget.IDLE)
						update.append(selected)
					selected = w
					w.set_current_state(gui.Widget.HOVER)
					update.append(w)
			#check whether the selected widget is not being hovered over (and this has not been set)
			if selected != None:
				if not selected.get_rect().collidepoint(pygame.mouse.get_pos()):
					selected.set_current_state(gui.Widget.IDLE)
					update.append(selected)
					selected = None
			#check whether the active widget is not being hovered over (and this has not been set)
			if active != None:
				#keep an input active when moved off of
				if type(active) != gui.Input:
					if not active.get_rect().collidepoint(pygame.mouse.get_pos()):
						active.set_current_state(gui.Widget.IDLE)
						update.append(active)
						active = None
		
		#update the display
		for u in update:
			#update a button, input or selector
			if type(u) in [gui.Button, gui.Input, gui.Selector]:
				u.blit_on(widgets_layer)
			#sprites
			elif type(u) == Tile:
				sprites_layer.fill(color.alpha)
				sprites_layer.blit(u.get_image(), u.get_rect())
		if len(update) > 0:
			update = []
			window.blit(background, [0, 0])
			window.blit(widgets_layer, [0, 0])
			window.blit(sprites_layer, [0, 0])
			pygame.display.update()
	
	#quit the program
	full_quit()
