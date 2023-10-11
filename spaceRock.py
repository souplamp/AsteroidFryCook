import pygame as p
import random
import math
from util import deg2Rad, getDist, rotatePoint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

colorPalette = [WHITE, GREEN, RED, ORANGE, YELLOW, CYAN, MAGENTA]
nColors = len(colorPalette)


# Space rock variables.
maxRockVelocity = 2
maxRockScaleFactor = 3



class spaceRock(p.sprite.Sprite):

  def __init__(self, gameWidth, gameHeight):
    super().__init__()

    self.x = random.randint(0, gameWidth - 1)
    self.y = random.randint(0, gameHeight - 1)
    self.heading = random.randint(0, 359)
    self.xVel = random.randint(-maxRockVelocity, maxRockVelocity)
    self.yVel = random.randint(-maxRockVelocity, maxRockVelocity)
    self.scaleFactorX = random.randint(2, maxRockScaleFactor)
    self.scaleFactorY = random.randint(2, maxRockScaleFactor)

    # rock image
    self.image = p.image.load("./sprites/rocks/rock0.png").convert_alpha()
    #self.image = p.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))

    # rect obj for sprite
    self.rect = self.image.get_rect()

    # This is passed from main
    self.screenWidth = gameWidth
    self.screenHeight = gameHeight

    index = random.randint(0, nColors - 1)
    self.color = colorPalette[index]

    self.isActive = True
  

  def moveMe(self):

    # Calculate new positon of space rock based on it's velocity.
    self.x = self.x + self.xVel
    self.y = self.y + self.yVel

    # If rock is outside of game space wrap it to other side.
    if (self.x < 0):
      self.x = self.screenWidth - 1
    elif (self.x > self.screenWidth):
      self.x = 0

    if (self.y < 0):
      self.y = self.screenHeight - 1
    elif (self.y > self.screenHeight):
      self.y = 0
    
    self.rect.x = self.x
    self.rect.y = self.y

    return


# :O

#if key input == m active turret
# if key input == s active shield
#
#  ship.shieldactive = true
# if ship.shield == true:
#  ship.shieldCharge = ship.ShieldCharge - 1
#  savespeed=  ship.speed  -- Make it so that any speed increases apply to this
#  ship.speed = ship.speed/2
#  if ship.shieldCharge<= 0:
#     ship.shield = false
#     ship.speed = savespeed
# PS, I don't know how to do any of this in python
# lol ok, this is a good outline tho!

  def drawMe(self, screen):
    if (self.isActive):
      
      colorImage = p.Surface(self.image.get_size()).convert_alpha()
      colorImage.fill(self.color)
      self.image.blit(colorImage, (0,0), special_flags = p.BLEND_RGBA_MULT)
      screen.blit(self.image, p.Rect(self.x, self.y, 32, 22))

    return

  def checkCollision(self, x, y):
    smack = False

    # i turned these into one check :)
    x_min_check = ((x >= self.x) and (x <= self.x + self.image.get_width()))
    y_min_check = ((y >= self.y) and (y <= self.y + self.image.get_height()))

    if x_min_check and y_min_check:
      smack = True

    return smack
  
  def reverseDir(self):
    self.xVel = -self.xVel
    self.yVel = -self.yVel