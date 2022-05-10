##################################################################################################################
# File for training the AI
#   1. Create initial population of genetic algorithm
#       (Can load from tensorflow model file or start from scratch)
#   2. Evaluate all population members (Run through games for each of them)
#       Keep track of best performance globaly, and save to file when new best is found
#   3. Sort population on best fitness
#   4. Run sample game of the best of that generation (optional)
#   5. Remove the worst performers (Bottom half of population usually)
#   6. Create child population from surviving parents (Asexual)
#   7. Step 2 (Control-c to stop the program)
##################################################################################################################
#Imports
from SnakeGameClass import SnakeGameClass
from RandomBot import RandomBot
from BotTest1 import BotTest1
import copy
##################################################################################################################
#Information for re-running the best game recorded
currentHighestScore = -9999999
bestFoodList = []
bestBot = BotTest1()
def reRunBestGame():
    G = SnakeGameClass(40, 500, 500)
    food = copy.deepcopy(bestFoodList)
    G.rerunGameInit(food)
    while(G.GameEnded == False):
        move = bestBot.returnMove(G.getState())
        G.rerunGameLoop(move, True)

modelPath = 'SavedModels/Model_6_20_20_4_Board500-500'
load = False 

#Create initial genetic algorithm population
popSize = 100
populationBots = []
for i in range(popSize):
    B = BotTest1()
    if load == True: 
        print("Loading Bot", i, "from file..", modelPath)
        B.loadModelFromFile(modelPath)
    populationBots.append([B,0])

#Main training loop for the genetic algorithm/neural network
while(True):

    #print("Eval all pop members")
    #Evaluate all population members
    for i in range(popSize):
        G = SnakeGameClass(99999, 500, 500)
        while(G.GameEnded == False):
            move = populationBots[i][0].returnMove(G.getState())
            G.loopBot(move, False)
        populationBots[i][1] = G.get_score()

        #Store info about best bot and game
        if(G.get_score() > currentHighestScore):
            print("High score model, saving to..", modelPath)
            bestFoodList = G.getHistoricalFoodList()
            currentHighestScore = G.get_score()
            bestBot = populationBots[i][0]
            bestBot.saveModelToFile(modelPath)

    #Sort bots on best fitness
    #print("Sorting...")
    populationBots = sorted(populationBots, key=lambda x: x[1], reverse=False)

    #Sample best bot of that generation
    G = SnakeGameClass(70, 500, 500)
    while(G.GameEnded == False):
        move = populationBots[len(populationBots)-1][0].returnMove(G.getState())
        G.loopBot(move, True)

    #print("Removing all but bottom ...", int(popSize/2))
    #Remove all but the bottom 50
    for i in range(len(populationBots) - int(popSize/2)): populationBots.pop(0)
    avgFitness = 0
    for i in range(len(populationBots)): avgFitness += populationBots[i][1]
    avgFitness /= len(populationBots)
    print("Average fitness of this generation is:", avgFitness)
    
    #print("Creating", int(popSize/2), "more")
    #Make bottom 50 from adjusted weights of top 6
    for i in range(10):
        for j in range(10):
            B = BotTest1()
            B.getNN().loadWeights(populationBots[49-i][0].getNN().getWeights())
            B.getNN().mutateWeights(1, 0.001, 0.05)
            populationBots.append([B,-9999999])