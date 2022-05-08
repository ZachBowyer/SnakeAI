from SnakeGameClass import SnakeGameClass
G = SnakeGameClass(10, 500, 500)
while(True):
    print(G.getState())
    G.loopPlayer()