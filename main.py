# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:00:54 2023

base asteroid code by Dr. Patrick McDowell
modified by Brady Landry
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
gameWidth = 5000
gameHeight = 3500

gameMidX = screenWidth / 2
gameMidY = screenHeight / 2

# General constants and variables defined.

nAsteroids = 150
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
      
  
  def moveCam(self, speed, heading):
    radAng = deg2Rad(heading)

    incX = (speed * math.cos(radAng))
    incY = (speed * math.sin(radAng))
    self.topLeftX += incX
    self.topLeftY += incY

    # If ship goes out of screen, wrap it other side.
    """
    if (self.topLeftX < 0):
      self.topLeftX = gameWidth - 1
    elif (self.topLeftX > gameWidth):
      self.topLeftX = 0
    """
  
    return incX, incY

  # offset object positions. One method for single objects, one method for a list of them
  # called by moveCam
  def offsetObjects(self, obj, incX, incY):

    if type(obj) == list or type(obj) == set:
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

  # Make some asteroids - that is space rocks.
  myAsteroids = set()
  # sprite group, use in collisions
  astGroup = p.sprite.Group()

  for j in range(nAsteroids):
    newAst = spaceRock(gameWidth, gameHeight)
    myAsteroids.add(newAst)
    astGroup.add(newAst)

  # Clock/game frame things.
  tickTock = 0

  # -------- Main Program Loop -----------
  while running:
    # --- Main event loop
    for event in p.event.get():
      if event.type == p.QUIT:
        running = False
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
      ship.turn(-3)

    if (key[p.K_d] == True):
      ship.turn(3)

    if (key[p.K_LSHIFT] == True):
      print("Shield is Active(WIP)")

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

    for a in myAsteroids:
      a.moveMe()

      # collisions
      for aa in myAsteroids:
        if (a != aa):
          if p.sprite.collide_rect(a, aa):
            a.reverseDir()
            aa.reverseDir()


    # Check to see if a bullet hit an asteroid.
    for a in myAsteroids:
      for b in bullets:
        if (a.isActive and b.isActive):
          smacked = a.checkCollision(b.x, b.y)
          if (smacked == True):
            b.setExplosion()
            a.isActive = False

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
