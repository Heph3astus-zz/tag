#for running individual simulations

import pygame
import enviornment
from player import *
from nnwk import NeuralNetwork
import random



class Sim:
    def __init__(self,playerCount,hunterCount,pShuffleRate,hShuffleRate,display,fLen):
        pygame.init()

        self.fLen = fLen
        self.display=display

        self.screen = pygame.display.set_mode([1000, 1000])

        self.running = True


        #loading enviornment
        self.walls = enviornment.walls()
        self.holes = []
        for i in enviornment.holes():
            self.holes.append(pygame.Rect(i[0],i[1],50,50))

        pygame.display.set_caption("test env")

        self.players = []
        self.hunters = []

        self.playerCount = playerCount
        self.hunterCount = hunterCount


        random.seed(os.urandom(5000))

        for i in range (0, self.playerCount):
            self.players.append(Player(self.walls,self.hunterCount,self.playerCount,random.randrange(200000)))
        for i in range (0, self.hunterCount):
            self.hunters.append(Hunter(self.walls,self.hunterCount,self.playerCount,random.randrange(200000)))

        #creating networks for hunters and players

        #player network will have 37 input nodes + those from players and hunters
        # 32 traces for walls
        # x pos, y pos, closestHoleX, closestHoleY, isInHole
        self.playerNetwork = NeuralNetwork(self.playerCount,self.hunterCount,37+2*(self.playerCount-1+self.hunterCount), 'player')
        self.playerNetwork.shuffle(1)
        #hunter network will have 68 input nodes
        # x pos, y pos, closestHoleX, closestHoleY
        # 32 traces for players
        # 32 traces for walls
        self.hunterNetwork = NeuralNetwork(self.playerCount,self.hunterCount,68, 'hunter')
        self.hunterNetwork.shuffle(1)


        self.frameCount = 0

        self.hCaptureTimes = [10000] * len(self.players)
        for i in range(len(self.hCaptureTimes)):
            self.hCaptureTimes[i] *= i+1

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 14)


        #if in pure sim mode do not display
        if not self.display:
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.environ["SDL_VIDEODRIVER"] = "dummy"

    def runSim(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False






        self.screen.fill((255,255,255))

        pDecisions = []
        hDecisions = []




        #display players and hunters. separated for visuals
        for p in self.players:
            pygame.draw.circle(self.screen,(150, 194, 147),(int(p.x),int(p.y)), int(p.visRad))

        for h in self.hunters:
            pygame.draw.circle(self.screen,(255,100,100),(h.x,h.y),int(h.visRad))

        for h in self.holes:
            pygame.draw.rect(self.screen,(100,100,255),h)




        #display walls last so that they go above everything
        for w in self.walls:
            pygame.draw.line(self.screen,(0,0,0),w[0],w[1],4)

        for p in self.players:
            if not p.captured:
                pDecisions.append(self.playerNetwork.think(p.getInputs(self.players,self.hunters,self.walls,self.holes,self.screen),p))
            else:
                pDecisions.append([0,0,0,0])
        for h in self.hunters:
            if h.checkingHole == 0:
                hDecisions.append(self.hunterNetwork.think(h.getInputs(self.players,self.walls,self.holes,self.screen),h))
            else:
                hDecisions.append([0,0,0,0])


        for p in self.players:
            if p.isInHole == 0:
                pygame.draw.rect(self.screen,(0,255,0), p.rect)
            else:
                pygame.draw.rect(self.screen,(0,100,0), p.rect)
        for h in self.hunters:
            if not h.checkingHole:
                pygame.draw.rect(self.screen, (255,0,0), h.rect)
            else:
                pygame.draw.rect(self.screen, (100,0,0), h.rect)



        for i in range(len(pDecisions)):
            #runs network's decided functions

            if pDecisions[i][0] and self.players[i].isInHole == 0:
                self.players[i].upX()
                #print("upX")
            if pDecisions[i][1] and self.players[i].isInHole == 0:
                self.players[i].downX()
                #print("downX")
            if pDecisions[i][2] and self.players[i].isInHole == 0:
                self.players[i].upY()
                #print("upY")
            if pDecisions[i][3] and self.players[i].isInHole == 0:
                self.players[i].downY()
                #print("downY")
            if pDecisions[i][4]:
                self.players[i].Hole()
                #print("hole")
            #print("cycle")

        for i in range(len(hDecisions)):

            if hDecisions[i][0]:
                self.hunters[i].upX()
            if hDecisions[i][1]:
                self.hunters[i].downX()
            if hDecisions[i][2]:
                self.hunters[i].upY()
            if hDecisions[i][3]:
                self.hunters[i].downY()
            if hDecisions[i][4]:
                self.hunters[i].Hole()
                self.hunters[i].checkLength = 0

            if self.hunters[i].checkingHole:
                if self.hunters[i].checkLength > 30:
                    for p in self.players:
                        if p.isInHole:
                            if p.x == h.closestHoleX and p.y == h.closestHoleX:
                                for i in range(len(self.hCaptureTimes)):
                                    if self.hCaptureTimes[i] == 100000:
                                        self.hCaptureTimes[i] == self.frameCount
                                        break
                            p.capture()
                            p.fitness = p.getFitness(self.frameCount)

                else:
                    self.hunters[i].checkLength+=1

        if self.hCaptureTimes[len(self.hCaptureTimes)-1] == 100000 and self.frameCount<self.fLen:
            self.frameCount+=1
            text = self.font.render(str(self.frameCount), False, (0,32,107))
            self.screen.blit(text, (950,950))
        else:
            self.running = False

        if self.display:
            pygame.display.flip()


    def getResults(self):
        hFitness = self.hunters[0].getFitness(self.hCaptureTimes)
        #print("hf" + str(hFitness))

        worstPFitness = 0

        for p in self.players:
            if p.fitness > worstPFitness:
                worstPFitness = p.getFitness(self.frameCount)

        statement = []

        statement.append(hFitness)
        statement.append(self.hunterNetwork)
        statement.append(worstPFitness)
        statement.append(self.playerNetwork)


        return statement



        pygame.quit()
