#!/usr/bin/env python3

import pygame

if __name__ == "__main__":
	#set constants
	FPS = 60
	WINSIZE = [800, 600]
	#set variables
	clock = pygame.time.Clock()
	loop = True
	
	#window setup
	window = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption("Qwirkle")
	#change window background
	window.fill((200, 200, 200))
	#show qwirkle title graphic
	qwirkle = pygame.image.load("Graphics/qwirkle.png")
	qwirkleRect = qwirkle.get_rect()
	qwirkleRect.midtop = [int(WINSIZE[0] * .5), int(WINSIZE[1] * .05)]
	window.blit(qwirkle, qwirkleRect);
	#update the display
	pygame.display.update()
	
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
