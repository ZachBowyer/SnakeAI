##################################################################################################################
# File for bot class definition
# 
# Each bot contains a NeuralNetwork object
#   These network objects are of a predefined architecture
##################################################################################################################
#Imports
from NeuralNetwork import NeuralNetwork
import numpy as np

##################################################################################################################
class BotTest1:
    #Constructor
    def __init__(self):
        self.NN = NeuralNetwork()

    #Return internal neural network object
    def getNN(self): return self.NN

    #Given input data, return a result from the neural network
    def returnMove(self, data):

        #Format 1D list to numpy array
        formattedData = np.array([data])
        res = self.NN.call(formattedData)

        #Get index of largest number (Because output is a probability distribution)
        dirNum = res.numpy().argmax(axis=1)

        #Choose a direction to move
        if(dirNum == 0): return 'UP'
        elif(dirNum == 1): return 'LEFT'
        elif(dirNum == 2): return 'RIGHT'
        elif(dirNum == 3): return 'DOWN'
        print("Bot somehow did not choose a direction")
        return 'DOWN'
    
    #Save and load models with files
    def saveModelToFile(self, filePath): self.NN.saveToFile(filePath)
    def loadModelFromFile(self, filePath):self.NN.loadFromFile(filePath)