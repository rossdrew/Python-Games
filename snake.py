#import pywin32 #Painting pixels
#import pyPNG #Painting bitmaps

import pygame, time
from random import randint

class GridPoint:
	def __init__(self, x, y):
		self.x = x
		self.y = y

AREA = GridPoint(640,480)
SPEED_DELAY = 0.1
STEP_SIZE = 20 		#Needs to be the same as sprite size
BG_COLOR = (0,0,0)

pygame.init()
game_screen = pygame.display.set_mode((AREA.x, AREA.y))
continue_game = True

snake_head = pygame.sprite.Sprite()
snake_head.tail = []
snake_head.image = pygame.image.load("snake_seg.gif") ##TODO get a snake image
snake_head.rect = snake_head.image.get_rect()
snake_group = pygame.sprite.GroupSingle(snake_head)

apple = pygame.sprite.Sprite()
apple.live = False
apple.image = pygame.image.load("apple.gif") 
apple.rect = apple.image.get_rect()
apple_group = pygame.sprite.GroupSingle(apple)

if snake_head.rect.width != apple.rect.width and snake_head.rect.height != apple.rect.height:
	print "ERROR: Sprites are not a common size"
elif snake_head.rect.width != snake_head.rect.height:
	print "ERROR: Snake sprite is not square"
elif apple.rect.width != apple.rect.height:
	print "ERROR: Apple sprite is not square"
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
	if sprite.rect.bottom > AREA.y:
		sprite.rect.bottom = AREA.y
	if sprite.rect.right > AREA.x:
		sprite.rect.right = AREA.x

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
		apple.rect.top = randint(0, AREA.y - STEP_SIZE) 
		apple.rect.top -= apple.rect.top % STEP_SIZE
		apple.rect.left = randint(0, AREA.x - STEP_SIZE) 
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

def snakeIsTangled(snake):
	y = snake.rect.top
	x = snake.rect.left
	for tailSeg in snake.tail:
		if y == tailSeg.y and x == tailSeg.x:
			return True
	return False

def updateSnake():
	"""Update snake and tail positions, return False if snake is tangled"""
	snake_head.tail.append(GridPoint(snake_head.rect.left, snake_head.rect.top))
	moveSprite(snake_head)
	if eatAvailiableApples(snake_head):
		clearApples()
		#dont clip tail which -in effect- grows the tail by one
	elif snakeIsTangled(snake_head):
		return False
	else:
		snake_head.tail.pop(0)

	return True

def drawSnake():
	halfStep = STEP_SIZE/2
	snake_group.draw(game_screen)
	for tailSeg in snake_head.tail:
		pygame.draw.circle(game_screen, (10,200,10), (tailSeg.x+halfStep,tailSeg.y+halfStep), STEP_SIZE/3, 2)	

snake_head.direction = "D"
while continue_game:
	time.sleep(SPEED_DELAY)
	continue_game = handleEvents()
	continue_game = updateSnake()

	game_screen.fill(BG_COLOR)
	drawSnake()

	createApples()
	apple_group.draw(game_screen)

	pygame.display.update()

pygame.quit()

