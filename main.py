import pygame
import math
import random
import numpy as np
from decimal import *

# pygame.init()
# screen = pygame.display.set_mode((700,700))
# clock = pygame.time.Clock()

class Environment:
    def __init__(self):
        self.windspeed = 20
        self.winddirection = 90

class Para:
    def __init__(self):
        self.startx = 150
        self.starty = 150
        self.startz = 250

        self.rightToggleDepth = 0
        self.leftToggleDepth = 0

        self.x = self.startx
        self.y = self.starty
        self.z = self.startz

        self.pitch = 8
        self.yaw = 0
        self.roll = 0

        # 10 meters a second forward
        self.velocity = 10
        # 1 meter a second down
        self.fallrate = 1

        self.angularVelocity = 0

        self.orientation = 0

        #milliseconds between ticks
        self.tickspeed = 50

    def forward(self,env, deltaTime):

        self.tickspeed = int(math.floor(deltaTime * 1000))

        self.angularVelocity = 2 * math.pi * 0.05 * abs(self.leftToggleDepth - self.rightToggleDepth)
        self.roll+= self.angularVelocity
        self.x += (self.angularVelocity * math.sin(math.radians(self.orientation)))
        self.y -= (self.angularVelocity * math.cos(math.radians(self.orientation)))

        self.orientation += (self.rightToggleDepth - self.leftToggleDepth) * 4

        distanceforward = float(Decimal(self.velocity)/1000 * self.tickspeed)
        self.x += (distanceforward * math.sin(math.radians(self.orientation)))
        self.y -= (distanceforward * math.cos(math.radians(self.orientation)))

        winddisplacement = float(Decimal(env.windspeed)*1000/60/60/1000 * self.tickspeed)
        self.x += (winddisplacement * math.sin(math.radians(env.winddirection)))
        self.y -= (winddisplacement * math.cos(math.radians(env.winddirection)))

        self.stabalise()
        self.calculatefall()

        self.z -= float(Decimal(self.fallrate)/1000 * self.tickspeed)

    def calculatefall(self):
        if self.angularVelocity > 0:
            if (self.fallrate < 54):
                self.fallrate += (54 - self.fallrate)/15 * abs(self.rightToggleDepth - self.leftToggleDepth) * 2

        self.roll += (self.rightToggleDepth - self.leftToggleDepth)*5
        if abs(self.roll) > 20:
            self.pitch = (self.fallrate -1)/54 * abs(self.rightToggleDepth - self.leftToggleDepth) * -98 + 8

    def stabalise(self):
        if self.angularVelocity == 0:
            if self.fallrate > 2:
                self.fallrate -= self.fallrate/8
            else:
                self.fallrate = 1

            if abs(self.roll) > 1:
                self.roll -= self.roll/8
            else:
                self.roll = 0


    def leftToggleDown(self):
        self.pitch -= 4
        self.leftToggleDepth += 0.125
        if(self.leftToggleDepth > 1): self.leftToggleDepth = 1
    def rightToggleDown(self):
        self.pitch += 4
        self.rightToggleDepth += 0.125
        if(self.rightToggleDepth > 1): self.rightToggleDepth = 1
    def leftToggleUp(self):
        self.leftToggleDepth -= 0.125
        if(self.leftToggleDepth < 0): self.leftToggleDepth = 0
    def rightToggleUp(self):
        self.rightToggleDepth -= 0.125
        if(self.rightToggleDepth < 0): self.rightToggleDepth = 0



def draw_para(para):
    color = (0, 128, 255)
    # pygame.draw.rect(screen, color, pygame.Rect(para.x,para.y,60,60))

    topPointx = para.x
    topPointy = para.y

    bottomLeftPointx = -10
    bottomLeftPointy = 15

    bottomRightPointx = 10
    bottomRightPointy = 15

    s = math.sin(math.radians(para.orientation))
    c = math.cos(math.radians(para.orientation))

    #rotate bottom left
    xnew = bottomLeftPointx * c - bottomLeftPointy * s
    ynew = bottomLeftPointx * s + bottomLeftPointy * c
    bottomLeftPointx = xnew + para.x
    bottomLeftPointy = ynew + para.y

    #rotate bottom right
    xnew = bottomRightPointx * c - bottomRightPointy * s
    ynew = bottomRightPointx * s + bottomRightPointy * c
    bottomRightPointx = xnew + para.x
    bottomRightPointy = ynew + para.y

    #backpoint
    backx = bottomLeftPointx + (bottomRightPointx - bottomLeftPointx) / 2
    backy = bottomLeftPointy + (bottomRightPointy- bottomLeftPointy) / 2
    backvx = topPointx - (topPointx - backx) *1.5
    backvy = topPointy - (topPointy - backy) *1.5


    pygame.draw.polygon(screen, color, [[para.x, para.y], [bottomLeftPointx, bottomLeftPointy], [bottomRightPointx, bottomRightPointy]], 2)
    pygame.draw.line(screen, color, [para.x, para.y], [backvx, backvy], 2)

def draw_HUD(para):
    color = (0, 128, 255)
    myfont = pygame.font.SysFont("monospace", 15)

    # height = myfont.render("Height: {0:.2f} ft".format(para.z/0.3048), 1, (255,255,0))
    height = myfont.render("Height: {0:.2f} ft".format(para.z/0.3048), 1, color)
    screen.blit(height, (520, 10))
    fallrate = myfont.render("fallrate: {0:.2f} m/s".format(para.fallrate), 1, (255,255,0))
    screen.blit(fallrate, (520, 25))

    # Draw Pitch
    pitchwording= myfont.render("Pitch", 1, color)
    screen.blit(pitchwording, (520, 60))
    pygame.draw.polygon(screen, color, calculateRollPoints(para), 4)

    # Draw Roll
    rollwording= myfont.render("Roll", 1, color)
    screen.blit(rollwording, (520, 160))
    pygame.draw.lines(screen, color, False, calculatePitchPoints(para) , 4)

def calculatePitchPoints(para):
    points = [(620,140),(620,90),(640,90),(600,90)]
    s = math.sin(math.radians(-para.pitch))
    c = math.cos(math.radians(-para.pitch))
    origin = points[0]

    newpoints = []

    for point in points:
        x = point[0] - origin[0]
        y = point[1] - origin[1]
        xnew = x * c - y * s
        ynew = x * s + y * c
        newpoints.append( (xnew + origin[0], ynew + origin[1]) )

    return newpoints

def calculateRollPoints(para):
    points = [(620,230),(640,180),(600,180)]
    s = math.sin(math.radians(para.roll))
    c = math.cos(math.radians(para.roll))
    origin = points[0]

    newpoints = []

    for point in points:
        x = point[0] - origin[0]
        y = point[1] - origin[1]
        xnew = x * c - y * s
        ynew = x * s + y * c
        newpoints.append( (xnew + origin[0], ynew + origin[1]) )

    return newpoints

def randomFlyer(x):
    choices = [
            [0,0,0,1],
            [0,0,1,0],
            [0,1,0,0],
            [1,0,0,0]
            ]

    return random.choice(choices)


def draw():
    done = False

    goal = [250, 250]

    pz = Para()
    env = Environment()
    # getTicksLastFrame = pygame.time.get_ticks()
    moves = []

    while not done:
        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
                # done = True

        #Key Pressed
        # pressed = pygame.key.get_pressed()
        # y = [0,0,0,1]

        # if pressed[pygame.K_j]:
            # if pressed[pygame.K_f]:
                # y[2] = 1
                # y[3] = 0
            # else:
                # y[1] = 1
                # y[3] = 0

        # if pressed[pygame.K_f]:
            # if pressed[pygame.K_j]:
                # y[2] = 1
                # y[3] = 0
            # else:
                # y[0] = 1
                # y[3] = 0
        x = [
            pz.x,
            pz.y ,
            pz.z,
            pz.orientation,
            pz.fallrate,
            pz.velocity,
            pz.angularVelocity,
            pz.pitch,
            pz.roll,
            pz.yaw,
            pz.rightToggleDepth,
            pz.leftToggleDepth,
            env.windspeed,
            env.winddirection,
            goal[0],
            goal[1]
        ]

        y = randomFlyer(x)
        moves.append([x,y])

        if y[0]:
            pz.leftToggleDown()
            pz.rightToggleUp()
        if y[1]:
            pz.leftToggleUp()
            pz.rightToggleDown()
        if y[2]:
            pz.leftToggleDown()
            pz.rightToggleDown()
        if y[3]:
            pz.leftToggleUp()
            pz.rightToggleUp()

        # t = pygame.time.get_ticks()
        # deltaTime = (t - getTicksLastFrame) / 1000.0
        # getTicksLastFrame = t
        # RollForward simulator

        deltaTime = 0.050
        pz.forward(env, deltaTime)

        # Putting Stuff on screen
        # screen.fill((0,0,0))

        # draw_para(pz)
        # draw_HUD(pz)

        # pygame.display.flip()
        # clock.tick(20)

        if pz.z <=0:
            finalScore = abs(goal[0] - pz.x)**pz.fallrate + abs(goal[1] - pz.y)**pz.fallrate
            print(finalScore)
            filename = "./games/{}.npy".format(finalScore)
            np.save(filename, moves)
            break


draw()

