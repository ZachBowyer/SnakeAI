import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import random

# https://keras.io/api/models/model/#model-class
class NeuralNetwork(tf.keras.Model):

    #Constructor, sets neural network architecture
    def __init__(self):
        super().__init__()
        bias_initializer = tf.keras.initializers.HeNormal()
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(8, input_shape=(4,), bias_initializer=bias_initializer))
        self.model.add(tf.keras.layers.Dense(4, activation='relu', bias_initializer=bias_initializer))
        self.model.add(tf.keras.layers.Dense(4, activation='softmax'))
    
    # Returns weights/biases as list of numpy arrays
    def getWeights(self):
        return self.model.get_weights()

    # Given an input, run it through network and return output
    def call(self, inputs):
        #ans = self.model.predict(inputs)
        ans = self.model(inputs)
        return ans

    #Used in creating new instances (Load weights from parent)
    def loadWeights(self, weights):
        self.model.set_weights(weights)
    
    #Used for mutating child networks (Slightly change weights and biases at random)
    def mutateWeights(self, prob_change, amount):
        newWeights = []
        for layer in self.model.layers:
            for x in layer.get_weights():
                numDimensions = len(np.shape(x))

                # If 1D layer (bias layer)
                if(numDimensions == 1):
                    newBiases = []
                    for elements in x: 
                        newBiases.append(elements+1)
                    newWeights.append(np.array(newBiases, dtype='float32'))

                # If 2D layer (weight layer)
                if(numDimensions == 2):
                    newWeightsOuter = []
                    for inner in x:
                        newWeightsInner = []
                        for elements in inner:
                            newWeightsInner.append(elements+1)
                        newWeightsOuter.append(newWeightsInner)
                    newWeights.append(np.array(newWeightsOuter, dtype='float32'))

#vars = tf.random.uniform(shape=(10, 20))
vars = np.array([[1, 2, 3, 4]])
model = NeuralNetwork()
model.mutateWeights(0.01, 0.01)
#print(model.call(vars))