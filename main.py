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

B = BotTest1()
B2 = B
print(B, B2)
while(True):
    for i in range(popSize):
        G = SnakeGameClass(10000, 500, 500)
        while(G.GameEnded == False):
            move = populationBots[i][0].returnMove(G.getState())
            G.loopBot(move, False)
        populationBots[i][1] = G.get_score()
    
    #print("Beforesort")
    #print(populationBots)
    #Sort bots on best fitness
    populationBots = sorted(populationBots, key=lambda x: x[1], reverse=False)

    #print("After sort")
    #print(populationBots)
    #Remove the bottom 50
    for i in range(50):
        populationBots.pop(0)
    
    #print("After bottom 50 removed")
    print(populationBots[len(populationBots)-1][1], len(populationBots))

    #Sample best bot per iteration
    G = SnakeGameClass(40, 500, 500)
    while(G.GameEnded == False):
            move = populationBots[len(populationBots)-1][0].returnMove(G.getState())
            G.loopBot(move, True)
    
    #Make bottom 50 from adjusted weights of survivors
    for i in range(50):
        B = populationBots[i][0]
        B.getNN().mutateWeights(0.1, 0.001, 0.01)
        populationBots.append([B,0])
    
    #print("After 50 added")
    #print(populationBots)

#while(True):
#    #G.loopPlayer()
#    #print(G.getState())
#    if(G.GameEnded == True): 
#        print("This bot's fitness is", G.get_score())
#        break