import random

def walls():
    walls = []
    wallCount = random.randrange(10)+10
    for i in range (0,wallCount):
        if bool(random.getrandbits(1)):
            good = False
            vals = []
            vals = [random.randrange(1000),random.randrange(1000),random.randrange(100)+50,random.randrange(20)+30]
            walls.append(vals)
        else:
            good = False
            vals = []
            vals = [random.randrange(1000),random.randrange(1000),random.randrange(20)+30,random.randrange(100)+50]
            walls.append(vals)

        #border walls
        walls.append([0,0,25,1000])
        walls.append([25,0,975,25])
        walls.append([975,25,25,975])
        walls.append([25,975,950,25])

    return walls


def holes():
    holes = []
    holeCount = random.randrange(10)+5
    for i in range (0,holeCount):
        holes.append([random.randrange(1000), random.randrange(1000)])
    return holes
