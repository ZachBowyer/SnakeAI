import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import random

####################################################################################################################
# https://keras.io/api/models/model/#model-class
class NeuralNetwork(tf.keras.Model):

    #Constructor, sets neural network architecture
    def __init__(self):
        super().__init__()
        bias_initializer = tf.keras.initializers.HeNormal()
        self.model = tf.keras.Sequential()
        self.model.add(keras.Input(shape=(5,)))
        #self.model.add(tf.keras.layers.Normalization(axis=1))
        self.model.add(tf.keras.layers.Dense(30, activation="relu", bias_initializer=bias_initializer))
        self.model.add(tf.keras.layers.Dense(30, activation="relu", bias_initializer=bias_initializer))
        self.model.add(tf.keras.layers.Dense(4, activation='softmax'))
        self.model.compile()
    
    # Returns weights/biases as list of numpy arrays
    def getWeights(self): return self.model.get_weights()

    # Given an input, run it through network and return output
    def call(self, inputs): return self.model(inputs)

    #Used in creating new instances (Load weights from parent)
    def loadWeights(self, weights):
        self.model.set_weights(weights)

    #Save and load model from file
    def saveToFile(self, filePath): self.model.save(filePath)
    def loadFromFile(self, filePath): self.model = keras.models.load_model(filePath)
    
    #Used for mutating child networks (Slightly change weights and biases at random)
    def mutateWeights(self, prob_change, amountLower, amountUpper):
        prob_Integer = round(1/prob_change, 0)

        newWeights = []
        for layer in self.model.layers:
            for x in layer.get_weights():
                numDimensions = len(np.shape(x))

                # If 1D layer (bias layer)
                if(numDimensions == 1):
                    newBiases = []
                    for elements in x: 
                        #Mutate if random probability hits
                        randomNum = 1
                        if(prob_change != 1): randomNum = random.randint(1, prob_Integer-1)

                        #Probability of adding/subtracting to weight is %50
                        rand2 = random.randint(0,1)
                        if(randomNum == 1):
                            amount = random.uniform(amountLower, amountUpper)
                            if(rand2 == 0): newBiases.append(elements+amount)
                            else: newBiases.append(elements-amount)
                        else: newBiases.append(elements)
                    newWeights.append(np.array(newBiases, dtype='float32'))

                # If 2D layer (weight layer)
                if(numDimensions == 2):
                    newWeightsOuter = []
                    for inner in x:
                        newWeightsInner = []
                        for elements in inner:
                            #Mutate if random probability hits
                            randomNum = 1
                            if(prob_change != 1): randomNum = random.randint(1, prob_Integer-1)

                            #Probability of adding/subtracting to weight is %50
                            rand2 = random.randint(0,1)
                            if(randomNum == 1):
                                amount = random.uniform(amountLower, amountUpper)
                                if(rand2 == 0):
                                    newWeightsInner.append(elements+amount)
                                else:
                                    newWeightsInner.append(elements-amount)
                            else: newWeightsInner.append(elements)
                        newWeightsOuter.append(newWeightsInner)
                    newWeights.append(np.array(newWeightsOuter, dtype='float32'))
        self.model.set_weights(newWeights)
####################################################################################################################
#vars = np.array([[1, 2, 3, 4]])
#model = NeuralNetwork()
#model.mutateWeights(0.05, 0.00001, 0.01)
#print(model.call(vars))