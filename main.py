from SnakeGameClass import SnakeGameClass
from RandomBot import RandomBot
from BotTest1 import BotTest1

#B = RandomBot()
#B = BotTest1()

#Genetic algorithm
popSize = 100
populationBots = []

for i in range(popSize):
    B = BotTest1()
    populationBots.append([B,0])

#B = BotTest1()
#B2 = BotTest1()
#B2.getNN().loadWeights(B.getNN().getWeights())
#B2.getNN().mutateWeights(0.2, 0.0001, 0.1)
#print(B.getNN().getWeights())
#print("--------")
#print(B2.getNN().getWeights())

while(True):
    for i in range(popSize):
        G = SnakeGameClass(10000, 500, 500)
        while(G.GameEnded == False):
            move = populationBots[i][0].returnMove(G.getState())
            G.loopBot(move, False)
        populationBots[i][1] = G.get_score()

    #Sort bots on best fitness
    populationBots = sorted(populationBots, key=lambda x: x[1], reverse=False)

    #Remove all but the bottom 50
    for i in range(len(populationBots) - 50): populationBots.pop(0)
    print(populationBots[len(populationBots)-1][1], len(populationBots))

    #Sample best bot per iteration
    G = SnakeGameClass(70, 500, 500)
    while(G.GameEnded == False):
            move = populationBots[len(populationBots)-1][0].returnMove(G.getState())
            G.loopBot(move, True)
    
    #Make bottom 50 from adjusted weights of top 6
    for i in range(5):
        for j in range(20):
            B = BotTest1()
            B.getNN().loadWeights(populationBots[49-i][0].getNN().getWeights())
            B.getNN().mutateWeights(1, 0.001, 0.1)
            populationBots.append([B,0])
    
#while(True):
#    #G.loopPlayer()
#    #print(G.getState())
#    if(G.GameEnded == True): 
#        print("This bot's fitness is", G.get_score())
#        break