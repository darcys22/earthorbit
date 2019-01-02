import pygame
import math
import random
import numpy as np
from decimal import *

pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

GRAVITATIONALCONSTANT = 6.67408e-11
EARTHSUNDISTANCEMETERS = 1.496e11
EARTHANGULARVELOCITYMETERSPERSECOND= 1.990986e-7
MASSOFTHESUNKG = 1.98855e30

# The length of one AU (Earth-Sun distance) in pixels.
PIXELSINONEEARTHSUNDISTANCEPERPIXEL = 150

# A factor by which we scale the distance between the sun and the earth in order to show it on screen
SCALEFACTOR = EARTHSUNDISTANCEMETERS / PIXELSINONEEARTHSUNDISTANCEPERPIXEL

# The number of calculations of orbital path done in one 16 millisecond frame
# The higher the number, the more precise are the calculations and the slower the simulation
NUMBEROFCALCULATIONSPERFRAME = 1000

DELTAT = 3600 * 24 / NUMBEROFCALCULATIONSPERFRAME

class Physics:
    def __init__(self):

        self.initialdistancevalue = EARTHSUNDISTANCEMETERS
        self.initialdistancespeed = 0.0
        self.initialanglevalue = math.pi / 6
        self.initialanglespeed = EARTHANGULARVELOCITYMETERSPERSECOND

        self.statedistancevalue = 0
        self.statedistancespeed = 0
        self.stateanglevalue = 0
        self.stateanglespeed = 0
        self.statemassofthesunkg = MASSOFTHESUNKG

    def calculateDistanceAcceleration(self):
        # [acceleration of distance] = [distance][angular velocity]^2 -G * M / [distance]^2
        return self.statedistancevalue * self.stateanglespeed**2 - (GRAVITATIONALCONSTANT * MASSOFTHESUNKG) / self.statedistancevalue**2

    def calculateAngleAcceleration(state):
        # [acceleration of angle] = -2[speed][angular velocity] / distance
        return -2.0 * self.statedistancespeed * self.stateanglespeed / self.statedistancevalue


def draw_circle(pointx, pointy, radius):
    color = (0, 128, 255)

    pygame.draw.circle(screen, color, [pointx, pointy],radius, 2)

def draw():
    done = False


    # getTicksLastFrame = pygame.time.get_ticks()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # t = pygame.time.get_ticks()
        # deltaTime = (t - getTicksLastFrame) / 1000.0
        # getTicksLastFrame = t
        # RollForward simulator

        deltaTime = 0.050

        screen.fill((0,0,0))

        draw_circle(250,250,20)

        pygame.display.flip()
        clock.tick(20)


draw()

