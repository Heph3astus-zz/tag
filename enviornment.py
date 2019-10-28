import random
import math

def walls():
    walls = []
    wallCount = random.randrange(15)+30
    for i in range (0,wallCount):
        sPoint = (random.randrange(900),random.randrange(900))
        r = random.randrange(50)+100
        a = random.random()*math.pi*2

        walls.append([sPoint,(math.cos(a)*r+sPoint[0],math.sin(a)*r+sPoint[1])])
    walls.append([(0,0),(0,1000)])
    walls.append([(0,0),(1000,0)])
    walls.append([(0,1000),(1000,1000)])
    walls.append([(1000,0),(1000,1000)])
    return walls


def holes():
    holes = []
    holeCount = random.randrange(10)+5
    for i in range (0,holeCount):
        holes.append([random.randrange(1000), random.randrange(1000)])
    return holes
