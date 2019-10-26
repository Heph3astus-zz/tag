import random
import pygame
import tensorflow as tf
import math
import tensorflow as tf
import os

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

    #slopes for all of the traces

    #slopes for vertical and completely down are techincally undefined, therefore
    #they are set to 10000 because thats close enough. Thats moving 1 pixel from
    #bottom to top of play field

    #all other slopes are approximations calc'ed by doing tan(angle)
    #slopes are measured starting with up and going clockwise to down
    #reuse the slopes for opposite lines
    slopes = [0, -0.4142, -1, -2.4142, 10000, 2.4142, 1, 0.4142]


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
    visRad = 200

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
            rect = pygame.Rect(x-25,y-25,50,50)
            hit = False
            for w in walls:
                if rect.colliderect(w):
                    hit = True
            if not hit:
                good = True
        print("pos: " + str(x) + ", " +  str(y))
        self.x = x
        self.y = y
        self.rect = rect





    def getFitness(seconds):
        return seconds

    def upX(self):
        self.x+= self.speed
        self.rect.move_ip(self.speed,0)
        hit = False
        for w in self.walls:
            if self.rect.colliderect(w):
                hit = True
        if hit or self.x > 975:
            self.x-= self.speed
            self.rect.move_ip(-self.speed,0)

    def downX(self):
        self.x-= self.speed
        self.rect.move_ip(-self.speed,0)
        hit = False
        for w in self.walls:
            if self.rect.colliderect(w):
                hit = True
        if hit or self.x < 25:
            self.x+= self.speed
            self.rect.move_ip(self.speed,0)

    def upY(self):
        self.y+= self.speed
        self.rect.move_ip(0,self.speed)
        hit = False
        for w in self.walls:
            if self.rect.colliderect(w):
                hit = True
        if hit or self.y > 975:
            self.y-= self.speed
            self.rect.move_ip(0,-self.speed)

    def downY(self):
        self.y-= self.speed
        self.rect.move_ip(0,-self.speed)
        hit = False
        for w in self.walls:
            if self.rect.colliderect(w):
                hit = True
        if hit or self.y < 25:
            self.y+= self.speed
            self.rect.move_ip(0,self.speed)

    def Hole(self):
        return

    def getInputs(self,players,hunters,screen):


        #set to 10000 as the default value of distance, which will hopefully just get ignored by the net
        touching = [10000] * 16
        #get wall ray traces
        for index, w in enumerate(self.walls):


            ### terminology. hLineY is the y value of the bottom of a wall
            ### iPoint is the x value of the intersection point of the ray line and the wall bottom
            ### y is the y value of the side intercept

            hLineY = w.y-self.y

            for i, s in enumerate(self.slopes):

                if s != 0:
                    iPoint = int(hLineY/s)
                else:
                    iPoint = w.x-self.x


            #for intersecting the side wall. determines left or right wall closer
                if iPoint >= 0 and w.x >= iPoint:
                    y = int(self.slopes[i]*(w.x - self.x))
                    #determining if the point is within bounds of side
                    if y >= w.y-self.y and y <= w.y+w.h-self.y:
                        distance = math.sqrt((w.x-self.x)**2 + y**2)
                        if distance <= self.visRad and distance < touching[i]:
                            touching[i] = distance
                            pygame.draw.circle(screen, (16,74,122), (w.x,y+self.y),5)


                elif iPoint <= 0 and w.x + w.w <= iPoint:
                    y = int(self.slopes[i]*(w.x+w.w-self.x))
                    #determining if the point is within bounds of side
                    if y >= w.y-self.y and y <= w.y+w.h-self.y:
                        distance = math.sqrt((w.x-self.x)**2 + y**2)
                        if distance <= self.visRad and distance < touching[i]:
                            touching[i] = distance
                            pygame.draw.circle(screen, (16,74,122), (w.x+w.w,y+self.y),5)


            #if will be intersecting the wall bottom
                elif (w.x <= iPoint and w.x + w.w >= iPoint and iPoint >= 0) or (w.x <= iPoint and w.x+ w.w >= iPoint and iPoint <= 0):
                    distance = math.sqrt(hLineY**2 + iPoint**2)
                    if distance <= self.visRad and distance < touching[i]:
                        touching[i] = distance
                        pygame.draw.circle(screen, (16,74,122), (iPoint+self.x,hLineY+self.y),5)



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

        nnInputArray.extend(touching)

        return nnInputArray







#######################################################
#######################################################
###################HUNTER CLASS########################
#######################################################
#######################################################





class Hunter:

    x = 0
    y = 0

    closestHoleX = 0
    closestHoleY = 0

    wallTraces = [0] * 16
    playerTraces = [0] * 16

    walls = None

    speed = 5

    visRad = 200

    slopes = [0, -0.4142, -1, -2.4142, 10000, 2.4142, 1, 0.4142]

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
            rect = pygame.Rect(x-25,y-25,50,50)
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
    def getFitness(t):
        fitness = 0
        prevTime = 0
        for i, v in enumerate(t):
            fitness+=(900-(v-prevTime)**2)/(i+1)
            prevTime += v
        if t[len(t)] < 30:
            fitness += 500
        return fitness

    def upX(self):
        self.x+= self.speed
        self.rect.move_ip(self.speed,0)
        hit = False
        for w in self.walls:
            if self.rect.colliderect(w):
                hit = True
        if hit or self.x > 975:
            self.x-= self.speed
            self.rect.move_ip(-self.speed,0)

    def downX(self):
        self.x-= self.speed
        self.rect.move_ip(-self.speed,0)
        hit = False
        for w in self.walls:
            if self.rect.colliderect(w):
                hit = True
        if hit or self.x < 25:
            self.x+= self.speed
            self.rect.move_ip(self.speed,0)

    def upY(self):
        self.y+= self.speed
        self.rect.move_ip(0,self.speed)
        hit = False
        for w in self.walls:
            if self.rect.colliderect(w):
                hit = True
        if hit or self.y > 975:
            self.y-= self.speed
            self.rect.move_ip(0,-self.speed)

    def downY(self):
        self.y-= self.speed
        self.rect.move_ip(0,-self.speed)
        hit = False
        for w in self.walls:
            if self.rect.colliderect(w):
                hit = True
        if hit or self.y < 25:
            self.y+= self.speed
            self.rect.move_ip(0,self.speed)

    def Hole(self):
        return

    def getInputs(self, players, screen):

        #wall touching
        #set to 10000 as the default value of distance, which will hopefully just get ignored by the net
        wTouching = [10000] * 16
        #get wall ray traces
        for index, w in enumerate(self.walls):


            ### terminology. hLineY is the y value of the bottom of a wall
            ### iPoint is the x value of the intersection point of the ray line and the wall bottom
            ### y is the y value of the side intercept

            hLineY = w.y-self.y

            for i, s in enumerate(self.slopes):

                if s != 0:
                    iPoint = int(hLineY/s)
                else:
                    iPoint = w.x-self.x


            #for intersecting the side wall. determines left or right wall closer
                if iPoint >= 0 and w.x >= iPoint:
                    y = int(self.slopes[i]*(w.x - self.x))
                    #determining if the point is within bounds of side
                    if y >= w.y-self.y and y <= w.y+w.h-self.y:
                        distance = math.sqrt((w.x-self.x)**2 + y**2)
                        if distance <= self.visRad and distance < wTouching[i]:
                            wTouching[i] = distance
                            pygame.draw.circle(screen, (16,74,122), (w.x,y+self.y),5)


                elif iPoint <= 0 and w.x + w.w <= iPoint:
                    y = int(self.slopes[i]*(w.x+w.w-self.x))
                    #determining if the point is within bounds of side
                    if y >= w.y-self.y and y <= w.y+w.h-self.y:
                        distance = math.sqrt((w.x-self.x)**2 + y**2)
                        if distance <= self.visRad and distance < wTouching[i]:
                            wTouching[i] = distance
                            pygame.draw.circle(screen, (16,74,122), (w.x+w.w,y+self.y),5)


            #if will be intersecting the wall bottom
                elif (w.x <= iPoint and w.x + w.w >= iPoint and iPoint >= 0) or (w.x <= iPoint and w.x+ w.w >= iPoint and iPoint <= 0):
                    distance = math.sqrt(hLineY**2 + iPoint**2)
                    if distance <= self.visRad and distance < wTouching[i]:
                        wTouching[i] = distance
                        pygame.draw.circle(screen, (16,74,122), (iPoint+self.x,hLineY+self.y),5)





        #set to 10000 as the default value of distance, which will hopefully just get ignored by the net
        pTouching = [10000] * 16
        #get player ray traces
        for index, p in enumerate(players):


            ### terminology. hLineY is the y value of the bottom of a wall
            ### iPoint is the x value of the intersection point of the ray line and the wall bottom
            ### y is the y value of the side intercept

            hLineY = p.rect.y-self.y

            for i, s in enumerate(self.slopes):

                if s != 0:
                    iPoint = int(hLineY/s)
                else:
                    iPoint = p.rect.x-self.x


            #for intersecting the side wall. determines left or right wall closer
                if iPoint >= 0 and p.rect.x >= iPoint:
                    y = int(self.slopes[i]*(p.rect.x - self.x))
                    #determining if the point is within bounds of side
                    if y >= p.rect.y-self.y and y <= p.rect.y+p.rect.h-self.y:
                        distance = math.sqrt((p.rect.x-self.x)**2 + y**2)
                        if distance <= self.visRad and distance < pTouching[i]:
                            pTouching[i] = distance
                            pygame.draw.circle(screen, (92, 8, 33), (p.rect.x,y+self.y),5)


                elif iPoint <= 0 and p.rect.x + p.rect.w <= iPoint:
                    y = int(self.slopes[i]*(p.rect.x+p.rect.w-self.x))
                    #determining if the point is within bounds of side
                    if y >= p.rect.y-self.y and y <= p.rect.y+p.rect.h-self.y:
                        distance = math.sqrt((p.rect.x-self.x)**2 + y**2)
                        if distance <= self.visRad and distance < pTouching[i]:
                            pTouching[i] = distance
                            pygame.draw.circle(screen, (92, 8, 33), (p.rect.x+p.rect.w,y+self.y),5)


            #if will be intersecting the wall bottom
                elif (p.rect.x <= iPoint and p.rect.x + p.rect.w >= iPoint and iPoint >= 0) or (p.rect.x <= iPoint and p.rect.x+ p.rect.w >= iPoint and iPoint <= 0):
                    distance = math.sqrt(hLineY**2 + iPoint**2)
                    if distance <= self.visRad and distance < pTouching[i]:
                        pTouching[i] = distance
                        pygame.draw.circle(screen, (92, 8, 33), (iPoint+self.x,hLineY+self.y),5)







        nnInputArray = [self.x,self.y,self.closestHoleX,self.closestHoleY]
        nnInputArray.extend(wTouching)
        nnInputArray.extend(pTouching)

        return nnInputArray
