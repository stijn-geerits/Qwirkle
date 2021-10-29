#!/usr/bin/env python3

import pygame

if __name__ == "__main__":
	window = pygame.display.set_mode([800, 600])
	
	#set constants
	FPS = 60
	#set variables
	clock = pygame.time.Clock()
	loop = True
	
	### main game loop ###
	while loop == True:
		#set the frame-rate
		clock.tick(FPS)
		#get window events
		for event in pygame.event.get():
			#close window event
			if event.type == pygame.QUIT:
				loop = False
	
	#quit the program
	pygame.quit()
	exit()
