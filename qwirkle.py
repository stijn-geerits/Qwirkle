#!/usr/bin/env python3

#import classes
import inspect, pygame
#initialize pygame (necessary for fonts)
pygame.init()

### Global variables ###
# global constants #
LANGDIR = "Lang/"

### Classes ###
# Container for storing and retreiving user config files #
class user:
	exec(open("user.conf", 'r').read())
	def get_config(self):
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
	exec(open(LANGDIR + user.lang + ".lang", 'r').read())

### Functions ###
def rendertext(surface, text, size=32, font=None, location=[0, 0], relpos="topleft", color=(32, 32, 32)):
	"""
	This function displays the given text on the surface, with the given font and size, at the given location
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
		textpos.append(text[line].get_rect())
		#update the position according to the relpos variable
		if relpos == "bottomleft":
			textpos[line].bottomleft = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "bottomright":
			textpos[line].bottomright = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "center":
			textpos[line].center = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "centerx":
			textpos[line].centerx = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "centery":
			textpos[line].centery = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "midbottom":
			textpos[line].midbottom = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "midleft":
			textpos[line].midleft = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "midright":
			textpos[line].midright = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "midtop":
			textpos[line].midtop = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "topleft":
			textpos[line].topleft = [location[0], location[1]+int(1.25*size*line)]
		elif relpos == "topright":
			textpos[line].topright = [location[0], location[1]+int(1.25*size*line)]
		else:
			#invalid relpos value given, go with standard setting
			print("\x1b[91m[Qwirkle]rendertext: Invalid relpos value:\x1b[97m %s\x1b[91m.\x1b[97m" % relpos)
			textpos[line].topleft = [location[0], location[1]+int(1.25*size*line)]
	
	#show the text on the surface
	for line in range(0, lines):
		surface.blit(text[line], textpos[line])
	return

### Main program ###
if __name__ == "__main__":
	#set variables
	clock = pygame.time.Clock()
	loop = True
	
	#window setup
	window = pygame.display.set_mode(user.winsize)
	pygame.display.set_caption(lang.qwirkle)
	#change window background
	window.fill((200, 200, 200))
	#show qwirkle title graphic
	qwirkle = pygame.image.load("Graphics/qwirkle.png")
	qwirkleRect = qwirkle.get_rect()
	qwirkleRect.midtop = [int(user.winsize[0]*.5), int(user.winsize[1]*.05)]
	window.blit(qwirkle, qwirkleRect)
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
