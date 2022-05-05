import random

#First bot test, go in random directions (Mostly to test interface with code)
class RandomBot:

    def __init__(self):
        self.x = 1
    
    # Only valid moves are 'DOWN' 'UP' 'LEFT' 'RIGHT'
    def returnMove(self, data):
        r = random.randint(1,3)
        if(r == 0): return 'UP'
        elif(r == 1): return 'LEFT'
        elif(r == 2): return 'RIGHT'
        elif(r == 3): return 'DOWN'
        return 'DOWN'