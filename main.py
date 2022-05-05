from SnakeGameClass import SnakeGameClass
G = SnakeGameClass(29, 500, 500)

while(True):
    G.loopBot('DOWN', True)
    print(G.get_score())
    end = G.GameEnded
    if(end == True): break
    #print(FirstGame.getCurrentBoard())
