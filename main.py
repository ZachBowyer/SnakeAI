##################################################################################################################
# File for training the AI
#   1. Create initial population of genetic algorithm
#       (Can load from tensorflow model file or start from scratch)
#   2. Evaluate all population members (Run through games for each of them)
#       Keep track of best performance globaly, and save to file when new best is found
#   3. Sort population on best fitness
#   4. Run sample game of the best of that generation (optional)
#   5. Remove the worst performers (Bottom half of population usually)
#   6. Display average fitness for the generation
#   7. Create child population from surviving parents (Asexual)
#   8. Step 2 (Control-c to stop the program)
##################################################################################################################
#Imports
from SnakeGameClass import SnakeGameClass
from RandomBot import RandomBot
from BotTest1 import BotTest1
import copy
import time

##################################################################################################################
#Information for re-running the best game recorded
currentHighestScore = -9999999
bestBot = BotTest1()

#Information for saving/loading bots
modelPath = 'SavedModels/Model_22_40_4_Board500-500_V5.h5'
load = False 

# 1. Create initial population of genetic algorithm
popSize = 100
populationBots = []
for i in range(popSize):
    B = BotTest1()
    if load == True: 
        print("Loading Bot", i, "from file..", modelPath)
        B.loadModelFromFile(modelPath)
    populationBots.append([B,0])

##################################################################################################################
#Main training loop for the genetic algorithm/neural network
while(True):
    start = time.time()
    #2.Evaluate all population members (Run through games for each of them)
    for i in range(popSize):
        G = SnakeGameClass(999999999999, 500, 500)
        while(G.GameEnded == False):
            move = populationBots[i][0].returnMove(G.getState())
            G.loopBot(move, False)
        populationBots[i][1] = G.get_score()

        #Store info about best bot and game
        #if(G.get_score() > currentHighestScore):
        #    print("High score model, saving to..", modelPath)
        #    currentHighestScore = G.get_score()
        #    bestBot = populationBots[i][0]
        #    bestBot.saveModelToFile(modelPath)

    #3. Sort population on best fitness
    populationBots = sorted(populationBots, key=lambda x: x[1], reverse=False)

    #4. Run sample game of the best of that generation (optional)
    G = SnakeGameClass(70, 500, 500)
    while(G.GameEnded == False):
        move = populationBots[len(populationBots)-1][0].returnMove(G.getState())
        G.loopBot(move, False)

    #5. Remove the worst performers (Bottom half of population usually)
    for i in range(len(populationBots) - int(popSize/2)): populationBots.pop(0)

    #6. Display average fitness for the generation
    avgFitness = 0
    for i in range(len(populationBots)): avgFitness += populationBots[i][1]
    avgFitness /= len(populationBots)
    print("Average fitness of generation:", avgFitness, "executed in", time.time() - start, "seconds")
    print("Saving best of this iteration with score of", populationBots[len(populationBots)-1][1], "to:", modelPath)
    populationBots[len(populationBots)-1][0].saveModelToFile(modelPath)

    #8. Create child population from surviving parents (Asexual)
    for i in range(10):
        for j in range(10):
            B = BotTest1()
            B.getNN().loadWeights(populationBots[49-i][0].getNN().getWeights())
            B.getNN().mutateWeights(1, 0.001, 0.05)
            populationBots.append([B,-9999999])
##################################################################################################################