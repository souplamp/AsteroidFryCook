# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:29:28 2023

@author: patrick

Here we will make a basic shooting game.  Asteroids like.

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

screenWidth = 500
screenHeight = 500

gameMidX = screenWidth / 2
gameMidY = screenHeight / 2

# General constants and variables defined.

nAsteroids = 20
maxShootingDelay = 30

basicShip = [[3, 0], [0, 3], [6, 0], [0, -3], [3, 0]]


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

  # Set up some game objects.
  # Space ship stuff.
  initialHeading = 90
  scaleFactor = 6
  ship = spaceShip(gameMidX, gameMidY, initialHeading, scaleFactor, basicShip, screenWidth, screenHeight)
  shipSpeed = 3
  ship.setGunSpot([6, 0])

  # Bullet stuff
  bullets = []
  bulletSize = int(0.5 * scaleFactor)
  bulletSpeed = 3 * shipSpeed
  shotCount = 0

  # Make some asteroids - that is space rocks.
  myAsteroids = []
  for j in range(nAsteroids):
    myAsteroids.append(spaceRock(screenWidth, screenHeight))

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
      ship.moveMe(shipSpeed)
    if (key[p.K_s] == True):
      ship.moveMe(-1 * shipSpeed)
    if (key[p.K_a] == True):
      ship.turn(-2)
    if (key[p.K_d] == True):
      ship.turn(2)
    if (key[p.K_LSHIFT] == True):
      print("Shield is Active(WIP)")
    if (key[p.K_SPACE] == True):
      if (shotCount == 0):
        gunX, gunY = ship.getGunSpot()
        myBullet = bullet(gunX, gunY, ship.heading, bulletSize, bulletSpeed, screenWidth, screenHeight)
        bullets.append(myBullet)
        shotCount = maxShootingDelay
    # --- Game logic should go here
    # Move bullets and asteroids.
    for b in bullets:
      b.moveMe()

    for a in myAsteroids:
      a.moveMe()

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

  # Close the window and quit.
  p.quit()

  return


asteroidMe()
