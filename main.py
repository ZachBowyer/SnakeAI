from SnakeGameClass import SnakeGameClass
FirstGame = SnakeGameClass(29, 500, 500)

while(True):
    FirstGame.loopPlayer()
    print(FirstGame.getCurrentBoard())
