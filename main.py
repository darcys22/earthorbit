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
NUMBEROFCALCULATIONSPERFRAME = 1

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

    def calculateAngleAcceleration(self):
        # [acceleration of angle] = -2[speed][angular velocity] / distance
        return -2.0 * self.statedistancespeed * self.stateanglespeed / self.statedistancevalue

    # Calculates a new value based on the time change and its derivative
    # For example it calculates the new distance based on the distance derivative (velocity) and the elapsed time interval
    def newValue(self,currentValue, deltaT, derivative):
        return currentValue + deltaT * derivative

    def resetStateToInitialConditions(self):
        self.statedistancevalue = self.initialdistancevalue
        self.statedistancespeed = self.initialdistancespeed

        self.stateanglevalue = self.initialanglevalue
        self.stateanglespeed = self.initialanglespeed

    def scaledDistance(self):
        return self.statedistancevalue / SCALEFACTOR

    # Calculates the position of the Earth
    def calculateNewPosition(self):
        # Calculate New Distance
        distanceAcceleration = self.calculateDistanceAcceleration()
        self.statedistancespeed = self.newValue(self.statedistancespeed, DELTAT, distanceAcceleration)
        self.statedistancevalue = self.newValue(self.statedistancevalue, DELTAT, self.statedistancespeed)

        # Calculate New Angle
        angleAcceleration = self.calculateAngleAcceleration()
        self.stateanglespeed = self.newValue(self.stateanglespeed, DELTAT, angleAcceleration)
        self.stateanglevalue = self.newValue(self.stateanglevalue, DELTAT, self.stateanglespeed)

        if (self.stateanglevalue > 2 * math.pi):
            self.stateanglevalue = self.stateanglevalue % (2 * math.pi)

    def updateFromUserInput(self,solarMassMultiplier):
        self.statemassofthesunkg = MASSOFTHESUNKG * solarMassMultiplier

def calculateEarthPosition(distance, angle):
    w, h = screen.get_size()
    middleX = math.floor(w / 2)
    middleY = math.floor(h / 2)
    centreX = math.cos(angle) * distance + middleX
    centreY = math.sin(-angle) * distance + middleY

    return (centreX, centreY)

def drawScene(distance, angle):
    earthPositionX, earthPositionY = calculateEarthPosition(distance, angle)

    color = (0, 128, 255)
    pygame.draw.circle(screen, color, [int(earthPositionX), int(earthPositionY)],25, 2)



def draw():
    done = False

    physics = Physics()
    physics.resetStateToInitialConditions()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0,0,0))
        pygame.draw.circle(screen, (255,200,0), [250, 250],60, 2)

        physics.calculateNewPosition();
        drawScene(physics.scaledDistance(), physics.stateanglevalue)

        pygame.display.flip()


draw()

