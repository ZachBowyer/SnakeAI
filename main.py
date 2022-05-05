from SnakeGameClass import SnakeGameClass
from RandomBot import RandomBot

G = SnakeGameClass(29, 500, 500)
B = RandomBot()

while(True):
    move = B.returnMove(G.getState())
    G.loopBot(move, True)
    end = G.GameEnded
    if(end == True): 
        print("This bot's fitness is", G.get_score())
        break