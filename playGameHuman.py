from SnakeGameClass import SnakeGameClass
G = SnakeGameClass(2, 500, 500)
while(True):
    print(G.getState())
    G.loopPlayer()