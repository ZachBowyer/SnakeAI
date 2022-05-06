from NeuralNetwork import NeuralNetwork

class BotTest1:
    def __init__(self):
        self.NN = NeuralNetwork()

    def returnMove(self, data):
        print(data)
        result = self.NN.call(data)
        if(r == 0 and cd != 'DOWN'): return 'UP'
        elif(r == 1 and cd != 'RIGHT'): return 'LEFT'
        elif(r == 2 and cd != 'LEFT'): return 'RIGHT'
        elif(r == 3 and cd != 'UP'): return 'DOWN'