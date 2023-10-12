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
maxRockScaleFactor = 40

rock0 = [[[1, 1], [2, 0], [1, -1], [-1, -1], [-2, 0], [-1, 1], [1, 1]]]
rock1 = [[[1, 2], [3, 1], [3, -1], [1, -2], [-1, -2], [-3, -1], [-3, 1], [-1, 2], [1, 2]]]
rock2 = [[[1, 1], [1, -1], [-0.5, -0.5], [-2, 0], [-1, 1], [1, 1]]]

spaceRocks = rock0 + rock1 + rock2
nRockTypes = len(spaceRocks)


class spaceRock():
  def __init__(self, gameWidth, gameHeight):
    self.x = random.randint(0, gameWidth - 1)
    self.y = random.randint(0, gameHeight - 1)
    self.heading = random.randint(0, 359)
    self.xVel = random.randint(-maxRockVelocity, maxRockVelocity)
    self.yVel = random.randint(-maxRockVelocity, maxRockVelocity)
    self.scaleFactorX = random.randint(20, maxRockScaleFactor)
    self.scaleFactorY = random.randint(20, maxRockScaleFactor)
    index = random.randint(0, nRockTypes - 1)
    self.myPoints = spaceRocks[index]

    # This is passed from main
    self.screenWidth = gameWidth
    self.screenHeight = gameHeight

    # Find center of rotation.
    xSum = ySum = 0
    for myPoint in self.myPoints:
      xSum = xSum + myPoint[0]
      ySum = ySum + myPoint[1]

    self.xc = xSum / len(self.myPoints)
    self.yc = ySum / len(self.myPoints)

    # Find a bounding box for this asteroid.
    xs = []
    ys = []
    for myPoint in self.myPoints:
      x = myPoint[0]
      y = myPoint[1]

      # Rotate and scale these points.
      xr, yr = rotatePoint(self.xc, self.yc, x, y, self.heading)
      xScale = xr * self.scaleFactorX
      yScale = yr * self.scaleFactorY
      xs.append(xScale)
      ys.append(yScale)

    self.minX = min(xs)
    self.maxX = max(xs)
    self.minY = min(ys)
    self.maxY = max(ys)

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
    
    points = []
    for myPoint in self.myPoints:
      # Get coords of point.
      x0 = float(myPoint[0])
      y0 = float(myPoint[1])

      # Rotate the point.
      myRadius = getDist(self.xc, self.yc, x0, y0)
      theta = math.atan2(y0 - self.yc, x0 - self.xc)
      radAng = deg2Rad(self.heading)
      xr = self.xc + myRadius * math.cos(radAng + theta)
      yr = self.yc + myRadius * math.sin(radAng + theta)

      # Scale.
      xs = xr * self.scaleFactorX
      ys = yr * self.scaleFactorY

      # Translate.
      xt = xs + self.x
      yt = ys + self.y

      # Put point into polygon point list.
      points.append([xt, yt])

    p.draw.polygon(screen, self.color, points, width=2)

    return

  def checkCollision(self, x, y):
    smack = False

    # i turned these into one check :)
    x_min_check = ((x >= self.minX + self.x) and (x <= self.maxX + self.x))
    y_min_check = ((y >= self.minY + self.y) and (y <= self.maxY + self.y))

    if x_min_check and y_min_check:
      smack = True

    return smack
  
  def reverseDir(self):
    self.xVel = -self.xVel
    self.yVel = -self.yVel