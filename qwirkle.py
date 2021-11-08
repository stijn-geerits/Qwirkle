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
	update = []
	widgets = []
	
	# window setup #
	window = pygame.display.set_mode(user.winsize)
	pygame.display.set_caption(lang.qwirkle)
	
	#change window background
	window.fill((200, 200, 200))
	#show qwirkle title graphic
	gui.renderimage(window, GRAPHICSDIR + "qwirkle.png", [int(user.winsize[0]*.5), int(user.winsize[1]*.05)], "midtop")
	#show the copyright notice
	gui.rendertext(window, lang.copyright, int(user.winsize[1]*.03), None, [int(user.winsize[0]*.5), int(user.winsize[1]*.97)], "midbottom")
	
	# widgets setup #
	#define button dimensions
	button_size = [int(user.winsize[0] * .24), int(user.winsize[1] * .08)]
	button_edge_size = int(min(user.winsize) * .004)
	#create button templates
	button_unavailable = gui.rectangle((102, 102, 102), button_size, button_edge_size, (61, 61, 61))
	button_idle = gui.rectangle((34, 85, 170), button_size, button_edge_size, (0, 44, 121))
	button_hover = gui.rectangle((146, 178, 255), button_size, button_edge_size, (34, 85, 170))
	button_active = gui.rectangle((0, 44, 121), button_size, button_edge_size, (34, 85, 170))
	
	# create the menu buttons #
	#new game button
	bRect = gui.set_relpos(pygame.Rect([0, 0]+button_size), [int(user.winsize[0]*.5), int(user.winsize[1]*.4)], "center")
	b = button_builder(bRect, [button_unavailable.copy(), button_idle.copy(), button_hover.copy(), button_active.copy()], None, lang.new_game)
	b.set_current_state(gui.Widget.UNAVAILABLE)
	widgets.append(b)
	#settings button
	bRect = gui.set_relpos(pygame.Rect([0, 0]+button_size), [int(user.winsize[0]*.5), int(user.winsize[1]*.5)], "center")
	b = button_builder(bRect, [button_unavailable.copy(), button_idle.copy(), button_hover.copy(), button_active.copy()], None, lang.settings)
	b.set_current_state(gui.Widget.UNAVAILABLE)
	widgets.append(b)
	#exit button
	bRect = gui.set_relpos(pygame.Rect([0, 0]+button_size), [int(user.winsize[0]*.5), int(user.winsize[1]*.6)], "center")
	b = button_builder(bRect, [button_unavailable.copy(), button_idle.copy(), button_hover.copy(), button_active.copy()], full_quit, lang.exit)
	widgets.append(b)
	
	#add the widgets to the update list
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
			u.blit_on(window)
		if len(update) > 0:
			update = []
			pygame.display.update()
	
	#quit the program
	full_quit()
