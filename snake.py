#import pywin32 #Painting pixels
#import pyPNG #Painting bitmaps

import pygame, time
from random import randint

class GridPoint:
	def __init__(self, x, y):
		self.x = x
		self.y = y

AREA_WIDTH = 640
AREA_HEIGHT = 480
SPEED_DELAY = 0.1
STEP_SIZE = 20 		#Needs to be the same as sprite size
BG_COLOR = (0,0,0)

pygame.init()
game_screen = pygame.display.set_mode((AREA_WIDTH, AREA_HEIGHT))
continue_game = True

snake_head = pygame.sprite.Sprite()
snake_head.tail = []
snake_head.image = pygame.image.load("snake_seg.gif") ##TODO get a snake image
snake_head.rect = snake_head.image.get_rect()
snake_group = pygame.sprite.GroupSingle(snake_head)

apple = pygame.sprite.Sprite()
apple.live = False
apple.image = pygame.image.load("apple.gif") ##TODO get a snake image
apple.rect = apple.image.get_rect()
apple_group = pygame.sprite.GroupSingle(apple)

if snake_head.rect.width != apple.rect.width and snake_head.rect.height != apple.rect.height:
	print "ERROR: Sprites are not a common size"
else:
	STEP_SIZE = snake_head.rect.width

def isExitGameEvent(event):
	return event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)

def moveSprite(sprite):
	if sprite.direction == "U":
		sprite.rect.top -= STEP_SIZE
	elif sprite.direction == "D":
		sprite.rect.top += STEP_SIZE
	elif sprite.direction == "L":
		sprite.rect.left -= STEP_SIZE
	elif sprite.direction == "R":
		sprite.rect.left += STEP_SIZE

	if sprite.rect.left < 0:
		sprite.rect.left = 0
	if sprite.rect.top < 0:
		sprite.rect.top = 0
	if sprite.rect.bottom > AREA_HEIGHT:
		sprite.rect.bottom = AREA_HEIGHT
	if sprite.rect.right > AREA_WIDTH:
		sprite.rect.right = AREA_WIDTH

def handleEvents():
	"""Handle any events and return False if the game should end, True otherwise"""
	for event in pygame.event.get():
		if isExitGameEvent(event):
			return False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				snake_head.direction = "U"
			if event.key == pygame.K_DOWN:
				snake_head.direction = "D"
			if event.key == pygame.K_LEFT:
				snake_head.direction = "L"
			if event.key == pygame.K_RIGHT:
				snake_head.direction = "R"
			if event.key == pygame.K_p:
				print "P Pressed"
		elif event.type == pygame.KEYUP:
			pass
	return True

def createApples():
	"""If there are no apples, places one at a random location"""
	if not apple.live:
		apple.rect.top = randint(0, AREA_HEIGHT - STEP_SIZE) 
		apple.rect.top -= apple.rect.top % STEP_SIZE
		apple.rect.left = randint(0, AREA_WIDTH - STEP_SIZE) 
		apple.rect.left -= apple.rect.left % STEP_SIZE
		apple.live = True

def clearApples():
	apple.live = False

def eatAvailiableApples(eater):
	"""Check if eater is one an apple, if so, eat it"""
	if (eater.rect.left == apple.rect.left) & (eater.rect.top == apple.rect.top):
	 	return True
	else:
		return False

snake_head.direction = ""
halfStep = STEP_SIZE/2
while continue_game:
	time.sleep(SPEED_DELAY)
	continue_game = handleEvents()

	snake_head.tail.append(GridPoint(snake_head.rect.left+halfStep, snake_head.rect.top+halfStep))
	if eatAvailiableApples(snake_head):
		clearApples()
	elif len(snake_head.tail) > 0:
		snake_head.tail.pop(0)

	game_screen.fill(BG_COLOR)
	moveSprite(snake_head)
	snake_group.draw(game_screen)

	for tailSeg in snake_head.tail:
		pygame.draw.circle(game_screen, (10,200,10), (tailSeg.x,tailSeg.y), STEP_SIZE/3, 2)	

	createApples()
#	pygame.draw.circle(game_screen, (200,10,20), (100,130), 10, 10)
	apple_group.draw(game_screen)

	pygame.display.update()

pygame.quit()

