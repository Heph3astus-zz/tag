from numpy import exp
import numpy as np
import os
import random

class NeuralNetwork():

    outputBiases = []
    weights = None
    outputWeights = []

    def __init__(self, playerCount, hunterCount, inputCount, type):


        np.random.seed(1)

        #getting weight data if existing and if not creating it
        net = type + 'Nets/' + str(playerCount) + ':' + str(hunterCount) + '.txt'

        self.weights = np.zeros((inputCount,10,inputCount),dtype=float)

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
                self.outputBiases.append(0.5 * np.random.random()+0.5)

            #creating and writing file
            newData = []
            for i in range(0,10):
                for x in range(0,inputCount):
                    for z in range(0,inputCount):
                        newData.append(self.weights[x,i,z])
            for i in range(0,5):
                for x in range(0,inputCount):
                    newData.append(self.outputWeights[i][x])
            for i in range(0,5):
                newData.append(self.outputBiases[i])
            with open(net, 'w') as f:

                for i in range(0,len(newData)-1):
                    f.write("%s\n" % newData[i])
                f.write("%s" % newData[len(newData)-1])


        #display for checking
        #print(self.weights[0,0,0])
        #print(type(self.outputWeights[0][0]))
        #print(self.outputBiases[0])


    def shuffle(self,rate):
        for i in self.weights:
            for x in i:
                for z in x:
                    shuffleNum = np.random.normal(0,rate*0.01,1)
                    z+= shuffleNum
        for i in self.outputWeights:
            for x in i:
                shuffleNum = np.random.normal(0,rate*0.01,1)
                x += shuffleNum
        for i in self.outputBiases:
            shuffleNum = np.random.normal(0,rate*0.01,1)
            i += shuffleNum

    def getWeights():
        arr = self.weights
        arr.append(outputWeights)
        arr.append(outputBiases)
        return arr

    def write(self,type,hCount,pCount):
        data = []
        for i in range(0,10):
            for x in range (0,inputCount):
                for z in range(0,inputCount):
                    data.append(self.weights[x,i,z])
        for i in range (0,5):
            data.append(self.outputWeights[i])
        for i in self.outputWeights:
            for x in i:
                data.append(i)
        for i in self.outputBiases:
            data.append(i)

        net = type + "Nets/" + str(pCount) + ":" + str(hCount)
        with open(net, 'w') as f:
            f.write(data)


    def think(self,inputs,entity):

        if len(inputs) != len(self.weights[0][0]):
            print(len(self.weights[0][0]))
            print(len(inputs))
        #variable storing values of previous layer
        previousValues = inputs
        values = previousValues
        for i in self.weights:
            for index, x in enumerate(i):
                val = 0
                div = 0
                for ind, z in enumerate(x):
                    val += previousValues[ind]*z
                    div += z
                values[index] = val
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
