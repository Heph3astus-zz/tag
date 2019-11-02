#coordinating script
import os
import tag

simCount = 0
genCount = 0


while True:
    print("sims per generation: ")
    simCount = input()
    try:
        simCount = int(simCount)
        break
    except:
        print("not an int. please try again")

while True:
    print("generation count (1 for continue until quit): ")
    genCount = input()
    try:
        genCount = int(genCount)
        break
    except:
        print("not an int. please try again")


print("display one sim per generation (y/n): ")
display = input()

if display == "y" :
    display = True
elif display == "n":
    display = False
else:
    print("unrecognized entry. defaulting to no")
    display = False

playerCount = 0
while True:
    print("playerCount: ")
    playerCount = input()
    try:
        playerCount = int(playerCount)
        break
    except:
        print("not an int. please try again")

hunterCount = 0
while True:
    print("hunterCount: ")
    hunterCount = input()
    try:
        hunterCount = int(hunterCount)
        break
    except:
        print("not an int. please try again")

print("frames cap of simulations (default to 1000):")
frameLen = input()
try:
    frameLen = int(frameLen)
except:
    print("unrecognized entry. defaulting to 1000")
    frameLen = 1000

sims = [None] * simCount

hShuffleRate = 1
pShuffleRate = 1

info = "genInfo/" + str(playerCount) + ";" + str(hunterCount) + ".txt"

genIndex = 0
if os.path.isfile(info):
    with open(os.path.relpath(info),'r') as f:
        l = f.readlines()
        genIndex = int(l[1])
else:
    with open(info,'w') as f:
        f.writelines(["generation:\n0"])
g = 0
prevHFitness = [0] * 5
while g < genCount:

    print("generation " + str(genIndex))
    results = [None] * simCount

    sims = [tag.Sim(playerCount,hunterCount,pShuffleRate,hShuffleRate,False,frameLen)] * simCount

    if display:
        sims[0].display = True

    #run each game loop

    while True:

        isDone = True

        for i in range(len(sims)):
            if results[i] == None:
                if sims[i].running == False:
                    results[i] = sims[i].getResults()

                    continue
                sims[i].runSim()
                isDone = False

        if isDone:
            break

    hFitness = 0
    pFitness = 0
    hNetwork = None
    pNetwork = None

    hShuffleRate = 0
    pShuffleRate = 0

    for i in range(len(results)):
        if results[i][0] >= hFitness:
            hFitness = results[i][0]
            hNetwork = results[i][1]
            #So many dumb things ive done here...
            hShuffleRate = 1
        if results[i][2] > pFitness:
            pFitness = results[i][2]
            pNetwork = results[i][3]
            #just doing this so that I dont have to edit my code. I'm very lazy
            pShuffleRate = 1

    print("generation complete.")
    print("best hunter fitness: " + str(hFitness))
    print("best player fitness: " + str(pFitness))

    try:
        hNetwork.write("hunter",hunterCount,playerCount)
        pNetwork.write("player",hunterCount,playerCount)
    except:
        pass

    genIndex+=1
    data = None
    with open(info,'r') as f:
        data = f.readlines()

    data[1] = str(genIndex)
    with open(info,'w') as f:
        f.writelines(data)
    if genCount != 1:
        g+=1

    for i in range(len(prevHFitness)-1):
        prevHFitness[i] = prevHFitness[i+1]
    prevHFitness[len(prevHFitness)-1] = hFitness


    #code to reset network if nothings happening
    new = False
    for p in prevHFitness:
        if p != prevHFitness[0]:
            new = True

    if not new:
        try:
            os.remove(os.path.relpath("hunterNets/"+str(playerCount)+";"+str(hunterCount) + "." + str(hNetwork.layerCount) + ".txt"))
        except:
            os.remove(os.path.relpath("hunterNets/"+str(playerCount)+";"+str(hunterCount) + ".3.txt"))
