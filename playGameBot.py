#Load a bot from a file and play a game with it
#The inputs from the gameState must match the model
from BotTest1 import BotTest1
from SnakeGameClass import SnakeGameClass
import time

#Create bot from model
modelPath = 'SavedModels/Model_10_30_30_4_Board500-500_V4.h5'
B = BotTest1()
print("Loading Bot from file..", modelPath)
B.loadModelFromFile(modelPath)

#Create game
G = SnakeGameClass(400, 500, 500)

#Play game
print("Starting game")
start = time.time()
while(G.GameEnded == False):
    move = B.returnMove(G.getState())
    G.loopBot(move, True)
print("Done! The game took", time.time() - start, "seconds")