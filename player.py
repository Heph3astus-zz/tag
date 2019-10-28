import random
import pygame
import tensorflow as tf
import math
import tensorflow as tf
import os
from raycaster import distances

class Player:
    #values for input into the network
    x = 0
    y = 0
    closestHoleX = 0
    closestHoleY = 0
    isInHole = False

    walls = None
    traces = [0] * 16

    rect = None

    captured = False

    fitness = 2000

    #### IMPORTANT NOTICE. Since I'm too lazy to figure out how to do variable
    #### input node count so that the number of hunters and players can be
    #### changed, instead I am saving weight data to a file which is named the
    #### number of players , the number of hunters.
    #### THEREFORE WHENEVER THE NUMBER OF PLAYERS OR HUNTERS IS CHANGED
    #### IT WILL START BLANK AND WILL HAVE TO COMPLETELY RELEARN EVERYTHING
    #### side note this is actually probably not a bad idea because I can then
    #### experiment with different counts and they may develop completely
    #### different strategies

    #### note to self: fitness for the player will be measured in 50*seconds alive


    speed = 3
    visRad = 50

    def __init__(self,walls,hunterCount,playerCount,seed):
        self.walls = walls
        random.seed(seed)
        x = 0
        y = 0
        rect = None
        good = False
        while not good:
            x = random.randrange(850)+75
            y = random.randrange(850)+75
            rect = pygame.Rect(x-5,y-5,10,10)
            hit = False
            for w in walls:
                try:
                    s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
                except:
                    s = 10000
                if s == 0:
                    s = 0.000001
                if ((s * rect.x + w[0][1] >= rect.y and s * rect.x + w[0][1] <= rect.y+rect.h)
                    or (s * (rect.x+rect.w) + w[0][1] >= rect.y and s * (rect.x+rect.w) + w[0][1] <= rect.y+rect.h)
                    or (rect.y/s >= rect.x and rect.y/s <= rect.x + rect.w)
                    or ((rect.y+rect.h)/s >= rect.x and (rect.y+rect.h) <= rect.x+rect.w)
                ):
                    hit = True
            if not hit:
                good = True
        self.x = x
        self.y = y
        self.rect = rect





    def getFitness(self,frames):
        return math.sqrt(frames)

    def upX(self):
        self.x+= self.speed
        self.rect.move_ip(self.speed,0)
        hit = False
        for w in self.walls:
            try:
                s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
            except:
                s = 10000
            if s == 0:
                s = 0.000001
            if ((s * self.rect.x + w[0][1] >= self.rect.y and s * self.rect.x + w[0][1] <= self.rect.y+self.rect.h)
                or (s * (self.rect.x+self.rect.w) + w[0][1] >= self.rect.y and s * (self.rect.x+self.rect.w) + w[0][1] <= self.rect.y+self.rect.h)
                or (self.rect.y/s >= self.rect.x and self.rect.y/s <= self.rect.x + self.rect.w)
                or ((self.rect.y+self.rect.h)/s >= self.rect.x and (self.rect.y+self.rect.h) <= self.rect.x+self.rect.w)
            ):
                hit = True
        if hit:
            self.x-= self.speed
            self.rect.move_ip(-self.speed,0)

    def downX(self):
        self.x-= self.speed
        self.rect.move_ip(-self.speed,0)
        hit = False
        for w in self.walls:
            try:
                s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
            except:
                s = 10000
            if s == 0:
                s = 0.000001
            if ((s * self.rect.x + w[0][1] >= self.rect.y and s * self.rect.x + w[0][1] <= self.rect.y+self.rect.h)
                or (s * (self.rect.x+self.rect.w) + w[0][1] >= self.rect.y and s * (self.rect.x+self.rect.w) + w[0][1] <= self.rect.y+self.rect.h)
                or (self.rect.y/s >= self.rect.x and self.rect.y/s <= self.rect.x + self.rect.w)
                or ((self.rect.y+self.rect.h)/s >= self.rect.x and (self.rect.y+self.rect.h) <= self.rect.x+self.rect.w)
            ):
                hit = True
        if hit:
            self.x+= self.speed
            self.rect.move_ip(self.speed,0)

    def upY(self):
        self.y+= self.speed
        self.rect.move_ip(0,self.speed)
        hit = False
        for w in self.walls:
            try:
                s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
            except:
                s = 10000
            if s == 0:
                s = 0.000001
            if ((s * self.rect.x + w[0][1] >= self.rect.y and s * self.rect.x + w[0][1] <= self.rect.y+self.rect.h)
                or (s * (self.rect.x+self.rect.w) + w[0][1] >= self.rect.y and s * (self.rect.x+self.rect.w) + w[0][1] <= self.rect.y+self.rect.h)
                or (self.rect.y/s >= self.rect.x and self.rect.y/s <= self.rect.x + self.rect.w)
                or ((self.rect.y+self.rect.h)/s >= self.rect.x and (self.rect.y+self.rect.h) <= self.rect.x+self.rect.w)
            ):
                hit = True
        if hit:
            self.y-= self.speed
            self.rect.move_ip(0,-self.speed)

    def downY(self):
        self.y-= self.speed
        self.rect.move_ip(0,-self.speed)
        hit = False
        for w in self.walls:
            try:
                s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
            except:
                s = 10000
            if s == 0:
                s = 0.000001
            if ((s * self.rect.x + w[0][1] >= self.rect.y and s * self.rect.x + w[0][1] <= self.rect.y+self.rect.h)
                or (s * (self.rect.x+self.rect.w) + w[0][1] >= self.rect.y and s * (self.rect.x+self.rect.w) + w[0][1] <= self.rect.y+self.rect.h)
                or (self.rect.y/s >= self.rect.x and self.rect.y/s <= self.rect.x + self.rect.w)
                or ((self.rect.y+self.rect.h)/s >= self.rect.x and (self.rect.y+self.rect.h) <= self.rect.x+self.rect.w)
            ):
                hit = True
        if hit:
            self.y+= self.speed
            self.rect.move_ip(0,self.speed)

    def Hole(self):
        if self.isInHole == 0:
            distance = math.sqrt((self.x-self.closestHoleX)**2 + (self.y-self.closestHoleY)**2)
            if distance < 20:
                self.x = self.closestHoleX
                self.y = self.closestHoleY
                self.isInHole = 1
                self.rect.x = self.closestHoleX - self.rect.w/2
                self.rect.y = self.closestHoleY - self.rect.h/2
        else:
            self.isInHole = 0

    def Capture():
        self.captured = True
        self.x = -100
        self.y = -100
        self.rect.x = -100
        self.rect.y = -100


    def getInputs(self,players,hunters,walls,holes,screen):

        d = 5000
        for h in holes:
            distance = math.sqrt((self.x-(h.x+h.w/2))**2 + (self.y-(h.x+h.h/2))**2)
            if distance < d:
                d = distance
                self.closestHoleX = h.x+h.w/2
                self.closestHoleY = h.y+h.h/2

        nnInputArray = [self.x,self.y,self.closestHoleX,self.closestHoleY]

        for h in hunters:
            nnInputArray.append(h.x)
            nnInputArray.append(h.y)
        for p in players:
            if p.x == self.x and p.y == self.y:
                continue
            nnInputArray.append(p.x)
            nnInputArray.append(p.y)

        nnInputArray.append(self.isInHole)

        wDistances = distances(walls,self,screen)

        nnInputArray.extend(wDistances)

        return nnInputArray







#######################################################
#######################################################
###################HUNTER CLASS########################
#######################################################
#######################################################





class Hunter:

    fitness = 0
    x = 0
    y = 0

    closestHoleX = 0
    closestHoleY = 0

    wallTraces = [0] * 16
    playerTraces = [0] * 16

    walls = None

    speed = 5

    checkLength = 0

    visRad = 100

    checkingHole = 0

    def __init__(self,walls,hunterCount,playerCount,seed):
        random.seed(seed)
        self.walls = walls
        x = 0
        y = 0
        rect = None
        good = False
        while not good:
            x = random.randrange(850)+75
            y = random.randrange(850)+75
            rect = pygame.Rect(x-5,y-5,10,10)
            hit = False
            for w in walls:
                if rect.colliderect(w):
                    hit = True
            if not hit:
                good = True
        self.x = x
        self.y = y
        self.rect = rect



    #### note to self. hunter fitness is calc'd by (30^2) - (time taken after last find)^2)/number of player found
    #### a 500 bonus is added if the last player is caught. This incentivises completion of the find
    #### the power of the time is there so that it will incentivise self.speed at the beginning more than when it is closer to 0
    #### this is in the hopes that as the hunter gets faster it will focus on finding all players instead of just being fast finding the first
    def getFitness(self,times):
        prevTime = 0
        for i,t in enumerate(times):
            self.fitness += 100/(t-prevTime-i)
            prevTime += t

        if times[len(times)-1] < 1500:
            self.fitness += 500

        return self.fitness

    def upX(self):
        self.x+= self.speed
        self.rect.move_ip(self.speed,0)
        hit = False
        for w in self.walls:
            try:
                s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
            except:
                s = 10000
            if s == 0:
                s = 0.000001
            if ((s * self.rect.x + w[0][1] >= self.rect.y and s * self.rect.x + w[0][1] <= self.rect.y+self.rect.h)
                or (s * (self.rect.x+self.rect.w) + w[0][1] >= self.rect.y and s * (self.rect.x+self.rect.w) + w[0][1] <= self.rect.y+self.rect.h)
                or (self.rect.y/s >= self.rect.x and self.rect.y/s <= self.rect.x + self.rect.w)
                or ((self.rect.y+self.rect.h)/s >= self.rect.x and (self.rect.y+self.rect.h) <= self.rect.x+self.rect.w)
            ):
                hit = True

        if hit:
            self.x-= self.speed
            self.rect.move_ip(-self.speed,0)

    def downX(self):
        self.x-= self.speed
        self.rect.move_ip(-self.speed,0)
        hit = False
        for w in self.walls:
            try:
                s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
            except:
                s = 10000
            if s == 0:
                s = 0.000001
            if ((s * self.rect.x + w[0][1] >= self.rect.y and s * self.rect.x + w[0][1] <= self.rect.y+self.rect.h)
                or (s * (self.rect.x+self.rect.w) + w[0][1] >= self.rect.y and s * (self.rect.x+self.rect.w) + w[0][1] <= self.rect.y+self.rect.h)
                or (self.rect.y/s >= self.rect.x and self.rect.y/s <= self.rect.x + self.rect.w)
                or ((self.rect.y+self.rect.h)/s >= self.rect.x and (self.rect.y+self.rect.h) <= self.rect.x+self.rect.w)
            ):
                hit = True
        if hit:
            self.x+= self.speed
            self.rect.move_ip(self.speed,0)

    def upY(self):
        self.y+= self.speed
        self.rect.move_ip(0,self.speed)
        hit = False
        for w in self.walls:
            try:
                s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
            except:
                s = 10000
            if s == 0:
                s = 0.000001
            if ((s * self.rect.x + w[0][1] >= self.rect.y and s * self.rect.x + w[0][1] <= self.rect.y+self.rect.h)
                or (s * (self.rect.x+self.rect.w) + w[0][1] >= self.rect.y and s * (self.rect.x+self.rect.w) + w[0][1] <= self.rect.y+self.rect.h)
                or (self.rect.y/s >= self.rect.x and self.rect.y/s <= self.rect.x + self.rect.w)
                or ((self.rect.y+self.rect.h)/s >= self.rect.x and (self.rect.y+self.rect.h) <= self.rect.x+self.rect.w)
            ):
                hit = True
        if hit:
            self.y-= self.speed
            self.rect.move_ip(0,-self.speed)

    def downY(self):
        self.y-= self.speed
        self.rect.move_ip(0,-self.speed)
        hit = False
        for w in self.walls:
            try:
                s = (w[0][1]-w[1][1])/(w[0][0]-w[1][0])
            except:
                s = 10000
            if s == 0:
                s = 0.000001
            if ((s * self.rect.x + w[0][1] >= self.rect.y and s * self.rect.x + w[0][1] <= self.rect.y+self.rect.h)
                or (s * (self.rect.x+self.rect.w) + w[0][1] >= self.rect.y and s * (self.rect.x+self.rect.w) + w[0][1] <= self.rect.y+self.rect.h)
                or (self.rect.y/s >= self.rect.x and self.rect.y/s <= self.rect.x + self.rect.w)
                or ((self.rect.y+self.rect.h)/s >= self.rect.x and (self.rect.y+self.rect.h) <= self.rect.x+self.rect.w)
            ):
                hit = True
        if hit:
            self.y+= self.speed
            self.rect.move_ip(0,self.speed)

    def Hole(self):
        distance = math.sqrt((self.x-self.closestHoleX)**2 + (self.y-self.closestHoleY)**2)
        if distance < 20:
            self.checkingHole = True


    def getInputs(self, players,walls,holes,screen):

        d = 5000
        for h in holes:
            distance = math.sqrt((self.x-(h.x+h.w/2))**2 + (self.y-(h.x+h.h/2))**2)
            if distance < d:
                d = distance
                self.closestHoleX = h.x+h.w/2
                self.closestHoleY = h.y+h.h/2


        nnInputArray = [self.x,self.y,self.closestHoleX,self.closestHoleY]

        wDistances = distances(walls,self,screen)

        playerLines = []
        for p in players:
            if p.isInHole == 0:
                playerLines.append([(p.rect.x,p.rect.y),(p.rect.x+p.rect.w,p.rect.y)])
                playerLines.append([(p.rect.x,p.rect.y+p.rect.h),(p.rect.x+p.rect.w,p.rect.y+p.rect.h)])
                playerLines.append([(p.rect.x,p.rect.y),(p.rect.x,p.rect.y+p.rect.h)])
                playerLines.append([(p.rect.x+p.rect.w,p.rect.y),(p.rect.x+p.rect.w,p.rect.y+p.rect.h)])
        pDistances = distances(playerLines,self,screen)

        for i in range (len(pDistances)):
            if wDistances[i] < pDistances[i]:
                pDistances[i] == 10000

        for d in pDistances:
            #tiny incentive to get closer to players so that the hunter can more easily stumble into points
            if d != 10000:
                self.fitness += math.sqrt(visRad/d*10)

        nnInputArray.extend(wDistances)
        nnInputArray.extend(pDistances)

        return nnInputArray
