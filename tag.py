import pygame
import enviornment
from player import *
from nnwk import NeuralNetwork
import random


#def runSim(hunterCount,playerCount)
pygame.init()

screen = pygame.display.set_mode([1000, 1000])

running = True


#loading enviornment
walls = enviornment.walls()
holes = []
for i in enviornment.holes():
    holes.append(pygame.Rect(i[0],i[1],50,50))

print("running")
pygame.display.set_caption("test env")

playerCount = 1
hunterCount = 1

players = []
hunters = []



random.seed(os.urandom(5000))

for i in range (0, playerCount):
    players.append(Player(walls,hunterCount,playerCount,random.randrange(200000)))
for i in range (0, hunterCount):
    hunters.append(Hunter(walls,hunterCount,playerCount,random.randrange(200000)+1))

#creating networks for hunters and players

#player network will have 21 input nodes + those from players and hunters
# 16 traces for walls
# x pos, y pos, closestHoleX, closestHoleY, isInHole
playerNetwork = NeuralNetwork(playerCount,hunterCount,21+2*(playerCount-1+hunterCount), 'player')
playerNetwork.shuffle(1)
#hunter network will have 36 input nodes + those from players and hunters
# x pos, y pos, closestHoleX, closestHoleY
# 16 traces for players
# 16 traces for walls
hunterNetwork = NeuralNetwork(playerCount,hunterCount,36, 'hunter')
hunterNetwork.shuffle(1)


frameCount = 0

hCaptureTimes = [100000] * len(players)

pygame.font.init()
font = pygame.font.SysFont('Arial', 14)

#loop
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False






    screen.fill((255,255,255))

    pDecisions = []
    hDecisions = []




    #display players and hunters. separated for visuals
    for p in players:
        pygame.draw.circle(screen,(150, 194, 147),(p.x,p.y), int(p.visRad))

    for h in hunters:
        pygame.draw.circle(screen,(255,100,100),(h.x,h.y),int(h.visRad))

    for h in holes:
        pygame.draw.rect(screen,(100,100,255),h)




    #display walls last so that they go above everything
    for w in walls:
        pygame.draw.line(screen,(0,0,0),w[0],w[1],4)

    for p in players:
        if not p.captured:
            pDecisions.append(playerNetwork.think(p.getInputs(players,hunters,walls,holes,screen),p))
        else:
            pDecisions.append([0,0,0,0])
    for h in hunters:
        if h.checkingHole == 0:
            hDecisions.append(hunterNetwork.think(h.getInputs(players,walls,holes,screen),h))
        else:
            hDecisions.append([0,0,0,0])


    for p in players:
        if p.isInHole == 0:
            pygame.draw.rect(screen,(0,255,0), p.rect)
        else:
            pygame.draw.rect(screen,(0,100,0), p.rect)
    for h in hunters:
        if not h.checkingHole:
            pygame.draw.rect(screen, (255,0,0), h.rect)
        else:
            pygame.draw.rect(screen, (100,0,0), h.rect)

    for i in range(len(pDecisions)):
        #runs network's decided functions

        if pDecisions[i][0] and players[i].isInHole == 0:
            players[i].upX()
            #print("upX")
        if pDecisions[i][1] and players[i].isInHole == 0:
            players[i].downX()
            #print("downX")
        if pDecisions[i][2] and players[i].isInHole == 0:
            players[i].upY()
            #print("upY")
        if pDecisions[i][3] and players[i].isInHole == 0:
            players[i].downY()
            #print("downY")
        if pDecisions[i][4]:
            players[i].Hole()
            #print("hole")
        #print("cycle")

    for i in range(len(hDecisions)):

        if hDecisions[i][0]:
            hunters[i].upX()
        if hDecisions[i][1]:
            hunters[i].downX()
        if hDecisions[i][2]:
            hunters[i].upY()
        if hDecisions[i][3]:
            hunters[i].downY()
        if hDecisions[i][4]:
            hunters[i].Hole()
            hunters[i].checkLength = 0

        if hunters[i].checkingHole:
            if hunters[i].checkLength > 30:
                for p in players:
                    if p.isInHole:
                        if p.x == h.closestHoleX and p.y == h.closestHoleX:
                            for i in range(len(hCaptureTimes)):
                                if hCaptureTimes[i] == 100000:
                                    hCaptureTimes[i] == frameCount
                                    break
                        p.capture()
                        p.fitness = p.getFitness(frameCount)

            else:
                hunters[i].checkLength+=1

    if hCaptureTimes[len(hCaptureTimes)-1] == 100000 and frameCount<1000:
        frameCount+=1
        text = font.render(str(frameCount), False, (0,32,107))
        screen.blit(text, (950,950))
    else:
        running = False


    pygame.display.flip()

hFitness = hunters[0].getFitness(hCaptureTimes)

for p in players:
    print("players fitness: " + str(p.fitness))

print("hunters fitness: " + str(hFitness))


pygame.quit()
