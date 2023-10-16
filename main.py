# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:00:54 2023

base asteroid code by Dr. Patrick McDowell
modified by Brady, Robert, and Cam
"""

import pygame as p
import random
import math
from util import deg2Rad, getDist, rotatePoint

# import game objects
from bullet import bullet
from spaceRock import spaceRock
from spaceShip import spaceShip

# Define some colors
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

# screen dimensions, for camera
screenWidth = 1000
screenHeight = 700

# game dimensions, for game world
gameWidth = 2000
gameHeight = 1400

gameMidX = screenWidth / 2
gameMidY = screenHeight / 2

# General constants and variables defined.
# Keep asteroid count low, they won't exist too far outside the camera
nAsteroids = 20
maxShootingDelay = 30

basicShip = [[3, 0], [0, 3], [6, 0], [0, -3], [3, 0]]

# append game objects to this list whenever they're instantiated, used for camera offset function to have the camera work
entities = []


class camera:
    
  def __init__(self, x, y, width, height):
    self.topLeftX = x
    self.topLeftY = y
    self.width = width
    self.height = height
    self.halfW = width / 2
    self.halfH = height / 2

  def moveCamSide(self, speed, heading):
    heading = heading + 90
    radAng = deg2Rad(heading)
    # x*pi/180

    incX = (speed * math.cos(radAng))
    incY = (speed * math.sin(radAng))
    self.topLeftX += incX
    self.topLeftY += incY

    # If center of camera goes out of screen, wrap it other side.
    if (self.topLeftX + (self.width / 2) < 0):
      self.topLeftX = gameWidth - (self.width / 2) - 1
    elif (self.topLeftX + (self.width / 2) > gameWidth):
      self.topLeftX = 0 - (self.width / 2)

    if (self.topLeftY + (self.height / 2) < 0):
      self.topLeftY = gameHeight - (self.height / 2) - 1
    elif (self.topLeftY + (self.height / 2) > gameHeight):
      self.topLeftY = 0 - (self.height / 2)

    return incX, incY
  def moveCam(self, speed, heading):
    radAng = deg2Rad(heading)

    incX = (speed * math.cos(radAng))
    incY = (speed * math.sin(radAng))
    self.topLeftX += incX
    self.topLeftY += incY

    # If center of camera goes out of screen, wrap it other side.
    if (self.topLeftX + (self.width / 2) < 0):
      self.topLeftX = gameWidth - (self.width / 2) - 1
    elif (self.topLeftX + (self.width / 2) > gameWidth):
      self.topLeftX = 0 - (self.width / 2)

    if (self.topLeftY + (self.height / 2) < 0):
      self.topLeftY = gameHeight - (self.height / 2) - 1
    elif (self.topLeftY + (self.height / 2) > gameHeight):
      self.topLeftY = 0 - (self.height / 2)
  
    return incX, incY

  # offset object positions. One method for single objects, one method for a list of them
  # called by moveCam
  def offsetObjects(self, obj, incX, incY):

    if type(obj) == list:
      for o in obj:
        o.x -= incX
        o.y -= incY
    
    else:
      obj.x -= incX
      obj.y -= incY



def asteroidMe():
  # Initialize pygame.
  p.init()

  # Set the width and height of the screen [width, height]
  size = (screenWidth, screenHeight)
  screen = p.display.set_mode(size)

  p.display.set_caption("asteroidMe()")

  # Set up random number generator.
  random.seed()

  # Loop until the user clicks the close button.
  running = True

  # Used to manage how fast the screen updates
  clock = p.time.Clock()
  
  # camera object
  c = camera(0, 0, screenWidth, screenHeight)

  # Set up some game objects.
  # Space ship stuff.
  initialHeading = 90
  scaleFactor = 6
  ship = spaceShip(gameMidX, gameMidY, initialHeading, scaleFactor, basicShip, gameWidth, gameHeight)
  shipSpeed = 5
  ship.setGunSpot([6, 0])

  # Bullet stuff
  bullets = []
  bulletSize = int(0.5 * scaleFactor)
  bulletSpeed = 3 * shipSpeed
  shotCount = 0
  act_count = 0

  # Make some asteroids - that is space rocks.
  myAsteroids = []

  def spawnAsteroid():
    myAsteroids.append(spaceRock(gameWidth, gameHeight))

  for j in range(nAsteroids):
    spawnAsteroid()

  # Clock/game frame things.
  tickTock = 0
  p.time.set_timer(1, 5000) # spawn rocks every x seconds, don't go over len nAsteroids

  # -------- Main Program Loop -----------
  while running:
    # --- Main event loop
    for event in p.event.get():
      if event.type == p.QUIT:
        running = False
    if act_count < 10:
      act_count = act_count + 1
      if (event.type == 1):
        if len(myAsteroids) < nAsteroids:
          spawnAsteroid()
          
    """ Check for keyboard presses. """
    key = p.key.get_pressed()

    # Handle keypresses.
    if (key[p.K_ESCAPE] == True):
      running = False

    if (key[p.K_w] == True):
      #ship.moveMe(shipSpeed)
      incX, incY = c.moveCam(shipSpeed, ship.heading)

      for e in entities:
        c.offsetObjects(e, incX, incY)

    if (key[p.K_s] == True):
      #ship.moveMe(-1 * shipSpeed)
      incX, incY = c.moveCam(-1 * shipSpeed, ship.heading)
      
      for e in entities:
        c.offsetObjects(e, incX, incY)
    if (key[p.K_a] == True):
      # ship.moveMe(shipSpeed)
      incX, incY = c.moveCamSide(shipSpeed, ship.heading)

      for e in entities:
        c.offsetObjects(e, incX, incY)

    if (key[p.K_d] == True):
      # ship.moveMe(-1 * shipSpeed)
      incX, incY = c.moveCamSide(-1 * shipSpeed, ship.heading)

      for e in entities:
        c.offsetObjects(e, incX, incY)
    if (key[p.K_q] == True):
      ship.turn(-3)

    if (key[p.K_e] == True):
      ship.turn(3)

    if (key[p.K_LSHIFT] == True):

      if ship.shieldActive == False and act_count>9:
        ship.shieldActive = True
        act_count = 0
        print("Shield is Active(WIP)")
      if ship.shieldActive == True and act_count>9:
        ship.shieldActive = False
        act_count = 0
        print("Shield is No Longer Active")

    if (key[p.K_SPACE] == True):
      if (shotCount == 0):
        gunX, gunY = ship.getGunSpot()
        myBullet = bullet(gunX, gunY, ship.heading, bulletSize, bulletSpeed, gameWidth, gameHeight)
        bullets.append(myBullet)
        shotCount = maxShootingDelay
        
        
    # --- Game logic should go here
    
    # camera function
    
    # Move bullets and asteroids.
    for b in bullets:
      b.moveMe()


    # make a gianter asteroid
    merge = False
    newAst = None
    # prevent "can't find x in list.remove(x)" error
    toRemove0, toRemove1 = False, False
    for a in myAsteroids:
      a.moveMe()

      # collisions
      for aa in myAsteroids:
        if (a != aa):
          smack, sameCol = a.checkCollision(aa.x, aa.y, aa.color)

          # only "merge" rocks if their scales are smallish. Make a bigger rock when they merge
          if sameCol and (a.scaleFactorX < 35 or a.scaleFactorY < 35) and (aa.scaleFactorX < 35 or aa.scaleFactorY < 35):
            newAst = spaceRock(gameWidth, gameHeight, 35, 35)
            merge = True
            newAst.x = a.x
            newAst.y = a.y
            newAst.color = a.color

            toRemove0 = a
            toRemove1 = aa

          elif smack:
            a.reverseDir()
            aa.reverseDir()
    
    if merge:
      myAsteroids.remove(toRemove0)
      myAsteroids.remove(toRemove1)

      myAsteroids.append(newAst)


    # Check to see if a bullet hit an asteroid.
    for a in myAsteroids:
      for b in bullets:
        if (a.isActive and b.isActive):
          smacked, _ = a.checkCollision(b.x, b.y)
          if (smacked == True):
            b.setExplosion()
            a.isActive = False
            myAsteroids.remove(a)

    # --- Screen-clearing code goes here

    # Here, we clear the screen to black. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)

    # --- Drawing code should go here
    # Spaceship
    ship.drawMe(screen, ORANGE, basicShip)

    # Bullets
    for b in bullets:
      b.drawMe(screen, RED)

    # Asteroids
    for a in myAsteroids:
      a.drawMe(screen)
      
     
    # remove later
    p.draw.rect(screen, GREEN, p.Rect(0 - c.topLeftX, 0 - c.topLeftY, gameWidth, gameHeight), width = 2)

    # --- Go ahead and update the screen with what we've drawn.
    p.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

    # Update frame count.
    tickTock = tickTock + 1

    # Implement shooting delay to keep bullet count lower.
    if (shotCount > 0):
      shotCount = shotCount - 1
    # Do some book keeping on arrays.
    # Remove inactive elements of bullets array.
    # Remove inactive elements of asteroids array.

    # replace objects in entities list
    entities.clear()
    # we don't want the ship in the list, else it will not stay centered
    # entities.append(ship)
    entities.append(myAsteroids)
    entities.append(bullets)

  # Close the window and quit.
  p.quit()

  return


asteroidMe()