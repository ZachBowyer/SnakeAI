from SnakeGameClass import SnakeGameClass
from RandomBot import RandomBot
from BotTest1 import BotTest1
import copy

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

modelPath = 'SavedModels/Model_8_norm_25_25_4_Board500-500'
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
            print(len(bestBot.getNN().getWeights()))
            bestBot.saveModelToFile(modelPath)

    #Sort bots on best fitness
    populationBots = sorted(populationBots, key=lambda x: x[1], reverse=False)

    #Sample best bot per iteration
    reRunBestGame()

    #Remove all but the bottom 50
    for i in range(len(populationBots) - 50): populationBots.pop(0)
    print(populationBots[len(populationBots)-1][1], len(populationBots))
    
    #Make bottom 50 from adjusted weights of top 6
    for i in range(25):
        for j in range(2):
            B = BotTest1()
            B.getNN().loadWeights(populationBots[49-i][0].getNN().getWeights())
            B.getNN().mutateWeights(1, 0.001, 0.1)
            populationBots.append([B,-9999999])