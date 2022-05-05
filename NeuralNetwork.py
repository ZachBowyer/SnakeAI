import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# https://keras.io/api/models/model/#model-class
class NeuralNetwork(tf.keras.Model):

    #Constructor, sets neural network architecture
    def __init__(self):
        super().__init__()
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(8, input_shape=(4,)))
        self.model.add(tf.keras.layers.Dense(4, activation='relu'))
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
    def mutateWeights(self):
        x=1

#vars = tf.random.uniform(shape=(10, 20))
vars = np.array([[1, 2, 3, 4]])
print(np.shape(vars))
model = NeuralNetwork()
print(model.call(vars))
print(model.getWeights())
model.loadWeights(model.getWeights())