#!/usr/bin/env python3

import inspect, pygame

### Container for storing and retreiving user config files ###
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

### Main program ###
if __name__ == "__main__":
	#set variables
	clock = pygame.time.Clock()
	loop = True
	
	#window setup
	window = pygame.display.set_mode(user.winsize)
	pygame.display.set_caption("Qwirkle")
	#change window background
	window.fill((200, 200, 200))
	#show qwirkle title graphic
	qwirkle = pygame.image.load("Graphics/qwirkle.png")
	qwirkleRect = qwirkle.get_rect()
	qwirkleRect.midtop = [int(user.winsize[0] * .5), int(user.winsize[1] * .05)]
	window.blit(qwirkle, qwirkleRect);
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
