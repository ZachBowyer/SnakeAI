from NeuralNetwork import NeuralNetwork
import numpy as np

class BotTest1:
    def __init__(self):
        self.NN = NeuralNetwork()

    def getNN(self): return self.NN

    def returnMove(self, data):
        formattedData = np.array([data])
        res = self.NN.call(formattedData)
        dirNum = res.numpy().argmax(axis=1)
        if(dirNum == 0): return 'UP'
        elif(dirNum == 1): return 'LEFT'
        elif(dirNum == 2): return 'RIGHT'
        elif(dirNum == 3): return 'DOWN'
        print("Bot somehow did not choose a direction")
        return 'DOWN'