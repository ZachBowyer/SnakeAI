#For if you want to play a game of snake yourself
#Useful for testing if the value of layer inputs are correct
from SnakeGameClass import SnakeGameClass

#Create game
G = SnakeGameClass(10, 500, 500)

#Loop through game
while(True):
    G.loopPlayer()
    print(G.getState())