from numpy import exp
import numpy as np
import os
import random

class NeuralNetwork():

    outputBiases = []
    weights = None
    outputWeights = []

    def __init__(self, playerCount, hunterCount, inputCount, eType):


        random.seed(os.urandom(5000))

        #getting weight data if existing and if not creating it
        n = eType + "Nets/" + str(playerCount) + ";" + str(hunterCount) + ".txt"
        net = os.path.relpath(n)

        self.weights = np.zeros((inputCount,10,inputCount),dtype=float)

        self.inputCount = inputCount

        if os.path.isfile(net):
            with open(net) as f:
                #read weights
                counter = 0
                data = f.readlines()
                for i in range(0,10):
                    for x in range (0,inputCount):
                        for z in range(0,inputCount):
                            self.weights[x,i,z] = float(data[z+(inputCount*x)+(inputCount*inputCount*i)])
                            counter+=1

                counter2 = 0
                for i in range (0,5):
                    self.outputWeights.append([])

                for i in range(counter,len(data)-5):
                    self.outputWeights[counter2].append(float(data[i]))
                    if (i-counter+1)%(inputCount) == 0:
                        counter2+=1
                for i in range(len(data)-5,len(data)):
                    self.outputBiases.append(float(data[i]))
        else:

            for i in range(0,10):
                for x in range(0,inputCount):
                    for z in range(0,inputCount):
                        num = 2 * random.random() - 1
                        self.weights[x,i,z] = num

            for i in range(0,5):
                self.outputWeights.append([])
                for x in range(0,inputCount):
                    self.outputWeights[i].append(2*random.random() - 1)

            #range is to number of functions
            for i in range(0,5):
                self.outputBiases.append(0.5 * random.random()+0.5)

            #creating and writing file
            newData = []
            for i in range(0,10):
                for x in range(0,self.inputCount):
                    for z in range(0,self.inputCount):
                        newData.append(self.weights[x,i,z])
            for i in range(0,5):
                for x in range(0,self.inputCount):
                    newData.append(float(self.outputWeights[i][x]))

            for i in range(0,5):
                newData.append(float(self.outputBiases[i]))
            with open(net, 'w') as f:

                for i in range(0,len(newData)-1):
                    f.write("%s\n" % newData[i])
                f.write("%s" % newData[len(newData)-1])



    def shuffle(self,rate):
        for i in range(0,10):
            for x in range(0,self.inputCount):
                for z in range(0,self.inputCount):
                    self.weights[x,i,z] += float(np.random.normal(loc = 0, scale = rate*0.0001,size = 1))
                    if self.weights[x,i,x] > 1.2:
                        self.weights[i,i,x] = 1.2
                    elif self.weights[x,i,x] < -1.2:
                        self.weights[i,i,x] = -1.2
        for i in range(0,5):
            for x in range(0,self.inputCount):
                self.outputWeights[i][x] += float(np.random.normal(loc = 0,scale = rate*0.0001,size = 1))
                if self.outputWeights[i][x] > 1.2:
                    self.outputWeights[i][x] = 1.2
                elif self.outputWeights[i][x] < -1.2:
                    self.outputWeights[i][x] = -1.2
        for i in range(0,5):
            self.outputBiases[i] += float(np.random.normal(loc = 0, scale = rate*0.01,size = 1))
            if self.outputBiases[i] > 0.85:
                self.outputBiases[i] = 0.85
            if self.outputBiases[i] < 0.5:
                self.outputBiases[i] = 0.5


    def getWeights():
        arr = self.weights
        arr.append(outputWeights)
        arr.append(outputBiases)
        return arr

    def write(self,eType,hCount,pCount):
        n = eType + "Nets/" + str(pCount) + ";" + str(hCount) + ".txt"
        net = os.path.relpath(n)
        #creating and writing file
        newData = []
        for i in range(0,10):
            for x in range(0,self.inputCount):
                for z in range(0,self.inputCount):
                    newData.append(self.weights[x,i,z])
        for i in range(0,5):
            for x in range(0,self.inputCount):
                newData.append(float(self.outputWeights[i][x]))

        for i in range(0,5):
            newData.append(float(self.outputBiases[i]))
        with open(net, 'w') as f:

            for i in range(0,len(newData)-1):
                f.write("%s\n" % newData[i])
            f.write("%s" % newData[len(newData)-1])


    def think(self,inputs,entity):
        #variable storing values of previous layer
        previousValues = inputs
        values = previousValues
        for i in self.weights:
            for index, x in enumerate(i):
                val = 0
                div = 0
                for ind, z in enumerate(x):
                    val += float(previousValues[ind]*z)
                    div += z
                values[index] = val/div
            previousValues = values

        average = 0
        aCount = 0
        #gets final output layer and turns it into a boolean array to do functions on
        outputs = [False,False,False,False,False]
        for ind, i in enumerate(self.outputWeights):
            if ind == 5:
                break
            val = 0
            div = 0
            for index, x in enumerate(previousValues):
                val += x*i[index]
                div += i[index]

            if (val/div) >= self.outputBiases[ind]:
                outputs[ind] = True
                average += val/div
                aCount += 1

        try:
            outputs.append(average/aCount)
        except:
            outputs.append(100000)

        return outputs
