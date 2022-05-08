from SnakeGameClass import SnakeGameClass
from RandomBot import RandomBot
from BotTest1 import BotTest1

G = SnakeGameClass(29, 500, 500)
#B = RandomBot()
B = BotTest1()

while(True):
    #move = B.returnMove(G.getState())
    #G.loopBot(move, True)
    G.loopPlayer()
    end = G.GameEnded
    print(G.getState())
    if(end == True): 
        print("This bot's fitness is", G.get_score())
        break