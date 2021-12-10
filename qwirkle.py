#!/usr/bin/env python3

# import classes #
import inspect, json, pygame, sys



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

# Container for storing color theme data #
class color:
	exec(open(THEMESDIR + user.theme + ".theme", 'r').read())

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
	WAIT_PLAYER = 4
	GAME = 5
	
	def __init__(self, window_size):
		self.size = window_size
		
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
		
		#initialize the main menu
		self.select_menu(self.MAIN)
		#initialize a variable for the data and game object
		self.data = {}
		self.game = None
		self.tiles = []
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
		elif menu == self.WAIT_PLAYER:
			self.background = self.__get_menu_wait_player()
			self.widgets = self.__get_widgets_wait_player()
		elif menu == self.GAME:
			self.background = self.__get_menu_game()
			self.widgets = self.__get_widgets_game()
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
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_main), user.winsize)
			surf.blit(bg, [0, 0])
		#place the qwirkle title graphic
		gui.renderimage(surf, GRAPHICSDIR + "qwirkle.png", [int(self.size[0]*.5), int(self.size[1]*.05)], "midtop")
		#place the copyright notice
		gui.rendertext(surf, lang.copyright, int(self.size[1]*.03), None, [int(self.size[0]*.5), int(self.size[1]*.97)], "midbottom", color.text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_rules(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		if gui.is_rgb(color.background_rules):
			surf.fill(color.background_rules)
		else:
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_rules), user.winsize)
			surf.blit(bg, [0, 0])
		#place the menu title
		gui.rendertext(surf, lang.rules, int(self.size[1]*.1), None, [int(self.size[0]*.5), int(self.size[1]*.02)], "midtop", color.text)
		#place the rules text
		gui.rendertext(surf, lang.rules_text, int(self.size[1]*.04), None, [int(self.size[0]*.02), int(self.size[1]*.11)], color=color.text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_new_game(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		if gui.is_rgb(color.background_new_game):
			surf.fill(color.background_new_game)
		else:
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_new_game), user.winsize)
			surf.blit(bg, [0, 0])
		#place the menu title
		gui.rendertext(surf, lang.player_selection, int(self.size[1]*.1), None, [int(self.size[0]*.5), int(self.size[1]*.02)], "midtop", color.text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_wait_player(self):
		#get the surface for the game menu
		surf = self.__get_menu_game()
		#draw the game menu widgets on the surface
		widgets = self.__get_widgets_game()
		for w in widgets:
			w.blit_on(surf)
		
		#create a semi transparent black overlay
		overlay = pygame.Surface(surf.get_size())
		overlay.set_alpha(204)
		#draw the overlay
		surf.blit(overlay, [0, 0])
		#render the text announcing the next player
		gui.rendertext(surf, lang.player_on_hand %(self.game.get_player_on_hand().get_name()), int(self.size[1]*.1), None, [self.size[0]//2, self.size[1]//2], "center", color.player_text)
		
		#return the pygame.Surface object
		return surf
	
	def __get_menu_game(self):
		#initialize the surface
		surf = pygame.Surface(self.size)
		
		#set the background color for the menu
		if gui.is_rgb(color.background_game):
			surf.fill(color.background_game)
		else:
			bg = pygame.transform.smoothscale(pygame.image.load(GRAPHICSDIR + color.background_game), user.winsize)
			surf.blit(bg, [0, 0])
		
		#reset the data variable
		data = {}
		#get the player data
		players = self.game.get_players()
		player_count = len(players)
		active_player = players.index(self.game.get_player_on_hand())
		
		#draw a grid for the playing field
		field_size = [(self.size[0]-int(self.btn_game_size[0]*2.3)-32)//36, (self.size[1]-32)//36]
		grid = gui.grid([36]*field_size[1], [36]*field_size[0], color.grid_edge, color.grid_fill)
		surf.blit(grid, gui.set_relpos(grid.get_rect(), [(self.size[0]-int(self.btn_game_size[0]*2.3))//2, self.size[1]//2], "center"))
		#draw the game field
		gridRect = gui.set_relpos(grid.get_rect(), [(self.size[0]-int(self.btn_game_size[0]*2.3))//2, self.size[1]//2], "center")
		for y in range(field_size[1]):
			for x in range(field_size[0]):
				surf.blit(self.game.get_field([x, y]).get_image(), [gridRect.left + (x * 35) + 2, gridRect.top + (x * 35) + 2])
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
			gui.rendertext(surf, str(self.game.get_player_score(players[p].get_id())), 24, None, [gridpos[0]+grid.get_width()-2, gridpos[1]+(p*31)+16], "midright", color.text)
		
		#render the amount of tiles in the bag
		gui.rendertext(surf, lang.tiles_in_bag %(self.game.get_tiles_left()), 24, None, [self.size[0]-int(self.btn_game_size[0]*1.15), int(self.size[1]*.55)], "center", color.text)
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
		for tile in range(len(self.tiles)):
			surf.blit(self.tiles[tile].get_image(), [gridRect.left + (tile * 35) + 2, gridRect.top + 2])
			#also set the location of the tiles
			self.tiles[tile].set_position([gridRect.left + (tile * 35) + 2, gridRect.top + 2])
		#store the pygame.Rect object of the hand grid for future reference
		self.data["hand"] = gridRect
		
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
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], None, lang.settings, color.text)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#exit button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.7)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], full_quit, lang.exit, color.text)
		widgets.append(btn)
		
		#return the Widget objects
		return widgets
	
	def __get_widgets_rules(self):
		#initialize a list of widgets
		widgets = []
		
		# button objects #
		#back button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_size), [int(self.size[0]*.5), int(self.size[1]*.95)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_template], lambda:self.select_menu(self.MAIN), lang.back, color.text)
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
		btn = button_builder(btnRect, [t.copy() for t in self.button_game_template], None, lang.cancel, color.text)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#play button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_game_size), [self.size[0]-int(self.btn_game_size[0]*1.7), self.size[1]-78], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_game_template], None, lang.play, color.text)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		#trade/skip button
		btnRect = gui.set_relpos(pygame.Rect([0, 0]+self.btn_game_size), [self.size[0]-int(self.btn_game_size[0]*1.15), int(self.size[1]*.6+self.btn_game_size[1]*2.4)], "center")
		btn = button_builder(btnRect, [t.copy() for t in self.button_game_template], None, lang.trade, color.text)
		btn.set_current_state(gui.Widget.UNAVAILABLE)
		widgets.append(btn)
		
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
		self.game = Game(players, Tileset(GRAPHICSDIR + "tiles.png", 32, True))
		
		# tile objects #
		#get the tiles for the player on hand
		self.tiles = self.game.get_player_on_hand().get_hand()
		
		#switch the menu to wait for player
		return self.select_menu(self.WAIT_PLAYER)
	
	def grab_tile(self, mouse_pos):
		"""
		Grab an available tile object on the surface
		
		Returns None if the mouse does not select a tile
		"""
		#check all player tiles
		for tile in self.tiles:
			#check whether the tile is selected
			if tile.get_rect().collidepoint(mouse_pos):
				#fill in the are where the tile was
				self.background.fill(color.grid_fill, tile.get_rect())
				#store the current position of the tile
				self.data["oldpos"] = tile.get_rect().topleft
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
			gridRect = self.data[grid]
			#the tile is on the grid
			if gridRect.collidepoint(tile.get_rect().center):
				#calculate the new position for the tile
				xTile = (tile.get_rect().centerx - gridRect.left) // 35
				yTile = (tile.get_rect().centery - gridRect.top) // 35
				#place the tile in the grid
				tile.set_position([gridRect.left + (xTile * 35) + 2, gridRect.top + (yTile * 35) + 2])
				self.background.blit(tile.get_image(), tile.get_rect())
				return
		#the tile is not on a grid
		tile.set_position(self.data["oldpos"])
		self.background.blit(tile.get_image(), tile.get_rect())
		return

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



### Main program ###
if __name__ == "__main__":
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
				#sent pressed keys to input widget
				if type(active) == gui.Input:
					active.type(event)
					update.append(active)
			#check mouse button events
			elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[pygame.BUTTON_LEFT - 1]:
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
			elif event.type == pygame.MOUSEBUTTONUP:
				#deselect a tile
				if type(sprite) == Tile:
					menus.drop_tile(sprite)
					sprite = None
					sprites_layer.fill(color.alpha)
					update.append(sprites_layer)
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
			#update a button or input
			if type(u) == gui.Button or type(u) == gui.Input:
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
