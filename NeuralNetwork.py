import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# https://keras.io/api/models/model/#model-class
class NeuralNetwork(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(8, input_shape=(4,)))
        self.model.add(tf.keras.layers.Dense(4, activation='relu'))
        self.model.add(tf.keras.layers.Dense(4, activation='softmax'))
    
    def getWeights(self):
        for layer in self.model.layers:
            weights = layer.get_weights()
            print(np.shape(weights))
            print(weights)

    def call(self, inputs):
        #ans = self.model.predict(inputs)
        ans = self.model(inputs)
        return ans

#vars = tf.random.uniform(shape=(10, 20))
vars = np.array([[1, 2, 3, 4]])
print(np.shape(vars))
model = NeuralNetwork()
print(model.call(vars))