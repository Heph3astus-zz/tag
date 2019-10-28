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


    for p in players:
        pygame.draw.rect(screen,(0,255,0), p.rect)

    for h in hunters:
        pygame.draw.rect(screen, (255,0,0), h.rect)



    #display walls last so that they go above everything
    for w in walls:
        pygame.draw.line(screen,(0,0,0),w[0],w[1],4)

    for p in players:
        pDecisions.append(playerNetwork.think(p.getInputs(players,hunters,walls,screen),p))
    for h in hunters:
        hDecisions.append(hunterNetwork.think(h.getInputs(players,walls,screen),h))

    for i in range(len(pDecisions)):
        #runs network's decided functions

        if pDecisions[i][0]:
            players[i].upX()
            #print("upX")
        if pDecisions[i][1]:
            players[i].downX()
            #print("downX")
        if pDecisions[i][2]:
            players[i].upY()
            #print("upY")
        if pDecisions[i][3]:
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
            hunters[i].downy()
        if hDecisions[i][4]:
            hunters[i].Hole()


    pygame.display.flip()



pygame.quit()
