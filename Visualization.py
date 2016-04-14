import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class PlayerHandSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def setup():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('Ticket to Ride')
	pygame.mouse.set_visible(0)

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	screen.blit(background, (0, 0))
	pygame.display.flip()

clock = pygame.time.Clock()

def event_handler():
	for event in pygame.event.get():
		if event.type == QUIT:
			return
		elif event.type == KEYDOWN and event.key == K_ESCAPE:
			return
		elif event.type == MOUSEBUTTONDOWN:
			if fist.punch(chimp):
				pass
				#punch_sound.play() #punch
				#chimp.punched()
			else:
				pass
				#whiff_sound.play() #miss
		elif event.type == MOUSEBUTTONUP:
			#fist.unpunch()
			pass

setup()

while 1:
	clock.tick(60)

	event_handler()