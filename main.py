import pygame, sys, time, random, keyboard

# Pygame stuff
SCREEN_RES = (800, 624)
pygame.init()
pygame.mixer.pre_init()
SCREEN = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("A game that doesn't work")
CLOCK = pygame.time.Clock()

# Defining colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WALLS_COLOR = (60, 66, 196)
GREY = (171, 173, 189)

# Globals
GRAVITY = 9.8
HorizantalSpeed = 10
VerticalSpeed = -10

class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.PrevX = x
		self.PrevY = y

		self.image1 = pygame.image.load('Resources/bird1.png') 
		self.image2 = pygame.image.load('Resources/bird2.png')
		self.image3 = pygame.image.load('Resources/bird3.png')

		# This var changes the image accoriding to the stage of the animation 
		self.image = self.image2 

		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self, pipes):
		self.CurrentX = self.rect.left
		self.CurrentY = self.rect.top

		# Changing the positions and making a backup of the coordinates
		NewX = self.CurrentX
		NewY = self.CurrentY + VerticalSpeed

		# Check for collision
		xCollision = pygame.sprite.spritecollide(self, pipes, False)

		self.rect.left = NewX

		if xCollision:
			# reset the x value
			self.rect.left = self.currentX
		else:
			self.rect.top = NewY
			yCollision = pygame.sprite.spritecollide(self, pipes, False)

			if yCollision:
				# reset value
				self.rect.top = self.currentY
				print('collision')

	def fall(self, pipes):
		self.CurrentX = self.rect.left
		self.CurrentY = self.rect.top

		# Changing the positions and making a backup of the coordinates
		NewX = self.CurrentX
		NewY = self.CurrentY - VerticalSpeed

		# Check for collision
		xCollision = pygame.sprite.spritecollide(self, pipes, False)

		self.rect.left = NewX

		if xCollision:
			# reset the x value
			self.rect.left = self.currentX
		else:
			self.rect.top = NewY
			yCollision = pygame.sprite.spritecollide(self, pipes, False)

			if yCollision:
				# reset value
				self.rect.top = self.currentY

	def animate(self, frame):
		if frame >= 0 and frame <=2:
			self.image = self.image1
		elif frame >= 3 and frame <=4:
			self.image = self.image2
		elif frame >= 5 and frame <=6:
			self.image = self.image3
			if frame == 6:
				frame = 0 

		
		return frame


		
class Base(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('Resources/NewBase.jpg')
		self.x = x
		self.y = y

		self.rect = self.image.get_rect()
		self.rect.top = self.y
		self.rect.left = self.x

		self.VEL = 5
		self.WIDTH = self.image.get_width()
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		"""
		move floor so it looks like its scrolling
		:return: None
		"""
		self.x1 -= self.VEL
		self.x2 -= self.VEL
		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		"""
		Draw the floor. This is two images that move together.
		:param win: the pygame surface/window
		:return: None
		"""
		win.blit(self.image, (self.x1, self.y))
		win.blit(self.image, (self.x2, self.y))

class Background(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('Resources/NewBg.jpg')
		self.x = x
		self.y = y

		self.rect = self.image.get_rect()
		self.rect.top = self.y
		self.rect.left = self.x


class Pipe(pygame.sprite.Sprite):
	
	# The rotation var is used to switch between the upper and lower pipe
	def __init__(self, x, y, height):
		pygame.sprite.Sprite.__init__(self)

		self.x = x
		self.y = y 
		self.VEL = 5

		self.image = pygame.image.load('Resources/pipe.png')
		self.LowerX1 = x
		self.LowerY1 = y

		self.rect = self.image.get_rect()

		self.UpperImage = self.image
		self.UpperImage = pygame.transform.rotate(self.UpperImage, 180)
		self.UpperX1 = x
		self.UpperY1 = self.LowerY1 - height - 320
		self.rect2 = self.UpperImage.get_rect()

	def move(self):
		self.LowerX1 -= self.VEL
		self.UpperX1 -= self.VEL

	def draw(self, win):
		win.blit(self.image, (self.LowerX1, self.LowerY1))
		win.blit(self.UpperImage, (self.UpperX1, self.UpperY1))

def GeneratePipe(x, PipeSprite, AllSprites):
	xCoord = x 
	height = 100
	yCoord = random.randint(204, 432)
	print(xCoord, yCoord, height)
	pipe = Pipe(xCoord, yCoord, height)
	PipeSprite.add(pipe)
	#AllSprites.add(pipe)
	return pipe, PipeSprite

def CheckCollision(BirdSprite, PipeSprite, BaseSprite):
	PipeCollision = pygame.sprite.spritecollide(BirdSprite, PipeSprite, False)
	BaseCollision = pygame.sprite.spritecollide(BirdSprite, PipeSprite, False)
	if PipeCollision:
		print('collision pipe')
	elif BaseCollision:
		print('collision base')

def CheckIfBirdPassedPipe(BirdX, PipeX):
	if PipeX < BirdX - 52:
		print('passed')
		return True
	else:
		return False


def main():
	AllSprites = pygame.sprite.RenderPlain()
	PlayerSprite = pygame.sprite.RenderPlain()

	player = Bird(250, 312)	
	PlayerSprite.add(player)

	BaseSprite = pygame.sprite.RenderPlain()
	base1 = Base(0, 512)
	base1.draw(SCREEN)
	BaseSprite.add(base1)

	BackgroundSprite = pygame.sprite.RenderPlain()
	background1 = Background(0, 0)
	BackgroundSprite.add(background1)

	PipeSprite = pygame.sprite.RenderPlain()

	AllSprites.add(background1)
	AllSprites.add(player)

	running = True
	# Initial pipe
	CurrentPipe, PipeSprite = GeneratePipe(500, PipeSprite, AllSprites)
	Pipes = []
	Pipes.append(CurrentPipe)

	frame = 0 

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()

		event = pygame.event.get()
		if keyboard.is_pressed(' '):
			player.update(PipeSprite)
		else:
			player.fall(PipeSprite)

		CheckCollision(PlayerSprite, PipeSprite, BaseSprite)

		if CheckIfBirdPassedPipe(player.PrevX, CurrentPipe.LowerX1):
			CurrentPipe, PipeSprite = GeneratePipe(350, PipeSprite, AllSprites)
			Pipes.append(CurrentPipe)

		# Animation
		frame += 1
		frame = player.animate(frame)

		# Drawing & Updating
		SCREEN.fill(BLACK)
		AllSprites.draw(SCREEN)
		for i in Pipes:
			i.move()
			i.draw(SCREEN)
		base1.move()
		base1.draw(SCREEN)
		pygame.display.flip()
		CLOCK.tick(10)


if __name__ == '__main__':
	main()