import pygame as p
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


class spaceShip:

    def __init__(self, x0, y0, heading0, scaleFactor0, points, screenWidth, screenHeight):
      self.x = x0
      self.y = y0
      self.screenX = x0
      self.screenY = y0
      self.heading = heading0
      self.scaleFactor = scaleFactor0
      self.shieldCharge = 100
      self.shieldActive = False
    
      # This is passed from main
      self.screenWidth = screenWidth
      self.screenHeight = screenHeight
      
    
      # Find center of rotation.
      xSum = ySum = 0
      for myPoint in points:
        xSum = xSum + myPoint[0]
        ySum = ySum + myPoint[1]
    
      self.xc = xSum / len(points)
      self.yc = ySum / len(points)
    
      self.gunSpot = []
      self.gunX = 0
      self.gunY = 0
    
      return

    def setGunSpot(self, gunSpot):
      self.gunSpot = gunSpot
      return
    
    def getGunSpot(self):
      return self.gunX, self.gunY
    
    def moveMe(self, inc):
      # Move ship along current course.
      radAng = deg2Rad(self.heading)
      self.x = self.x + inc * math.cos(radAng)
      self.y = self.y + inc * math.sin(radAng)
      # If ship goes out of screen, wrap it other side.
      if (self.x < 0):
        self.x = self.screenWidth - 1
      elif (self.x > self.screenWidth):
        self.x = 0
    
      if (self.y < 0):
        self.y = self.screenHeight - 1
      elif (self.y > self.screenHeight):
        self.y = 0
    
      return
    
    def drawMe(self, screen, color, myShip):
      points = []
      isTheGunSpot = False
      for myPoint in myShip:
        if (myPoint == self.gunSpot):
          isTheGunSpot = True
    
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
        xs = xr * self.scaleFactor
        ys = yr * self.scaleFactor
    
        # Translate.
        xt = xs + self.x
        yt = ys + self.y
    
        # Save gun position.
        if (isTheGunSpot is True):
          self.gunX = xt
          self.gunY = yt
          isTheGunSpot = False
    
        # Put point into polygon point list.
        points.append([xt, yt])
    
      p.draw.polygon(screen, color, points, width=2)
      return
    
    def turn(self, inc):
      self.heading = self.heading + inc
    
      if (self.heading > 359):
        self.heading = 0
      elif (self.heading < 0):
        self.heading = 359
    
      return