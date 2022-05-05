import random

#First bot test, go in random directions (Mostly to test interface with code)
class RandomBot:

    def __init__(self):
        self.x = 1
    
    # Only valid moves are 'DOWN' 'UP' 'LEFT' 'RIGHT'
    def returnMove(self, data):
        r = random.randint(1,3)
        cd = data[1]
        if(r == 0 and cd != 'DOWN'): return 'UP'
        elif(r == 1 and cd != 'RIGHT'): return 'LEFT'
        elif(r == 2 and cd != 'LEFT'): return 'RIGHT'
        elif(r == 3 and cd != 'UP'): return 'DOWN'
        return 'DOWN'