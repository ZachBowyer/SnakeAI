import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

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
    def mutateWeights(self):
        for layer in self.model.layers:
            print(layer.get_weights())
            #newArr = np.array(layer.get_weights())
            #print("new", newArr)
            #layer.set_weights(layer.get_weights())
            #newWeights = np.array(layer.get_weights())
            #print("newW", newWeights)
            #for weightArray in layer.get_weights():
            #    print(weightArray)
                #layer.set_weights(weightArray)
            #print(layer.get_weights())
        #for layerWeights in self.weights:   #Each layer
        #    for tensors in layerWeights:      #Is a list of lists
        #        print(tensors)
        #        values = tf.keras.backend.get_value(tensors)
        #        if values is not list: 
        #            tensors[0] = 7
        #            values = [values]
        #        if values is list:
        #            x=1
        #        print(values)

#vars = tf.random.uniform(shape=(10, 20))
vars = np.array([[1, 2, 3, 4]])
model = NeuralNetwork()
model.mutateWeights()
#print(model.call(vars))