##################################################################################################################
# File for the snake game framework
# Original source code written by Rajat Dipta Biswas - https://github.com/rajatdiptabiswas/snake-pygame
# Bot integration and abstraction by Zachary Bowyer and Jonathan Olderr
#
# Can run a game for a human player
# Can run a game for a bot player
# Can store food to replay a game
##################################################################################################################
#Imports
import pygame, sys, time, random
import numpy as np
import math

##################################################################################################################
# Class wrapper around the original snake code
class SnakeGameClass:

    ##################################################################################################################
    #Constructor
    def __init__(self, speed, sizeX, sizeY):
        self.difficulty = speed
        self.frame_size_x = sizeX
        self.frame_size_y = sizeY
        self.starvationTime = 0
        self.maxStarvationTime = 250
        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        # Colors (R, G, B)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.grey = pygame.Color(105, 105, 105)

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        #Game variables
        self.HistoricalFoodList = []
        self.HistoricalSnakePositions = []
        self.snake_pos = [250, 250]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.HistoricalFoodList.append(self.food_pos) 
        self.food_spawn = True

        #Start snake going random direction 
        r = random.randrange(1, 5)
        if(r == 1): self.direction = 'RIGHT'
        if(r == 2): self.direction = 'UP'
        if(r == 3): self.direction = 'DOWN'
        if(r == 4): self.direction = 'LEFT'

        self.change_to = self.direction
        self.score = 0
        self.GameEnded = False
    
    ##################################################################################################################
    #Display a game over screen and quit the script
    def game_over(self):
        self.my_font = pygame.font.SysFont('times new roman', 90)
        self.game_over_surface = self.my_font.render('YOU DIED', True, self.red)
        self.game_over_rect = self.game_over_surface.get_rect()
        self.game_over_rect.midtop = (self.frame_size_x/2, self.frame_size_y/4)
        self.game_window.fill(self.black)
        self.game_window.blit(self.game_over_surface, self.game_over_rect)
        self.show_score(1, self.red, 'times', 20)
        self.GameEnded = True
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
    
    ##################################################################################################################
    #Return score
    def get_score(self): return self.score

    ##################################################################################################################
    #Get list of food for a rerun if needed
    def getHistoricalFoodList(self): return self.HistoricalFoodList

    ##################################################################################################################
    #Manahattan distance between two points
    def manhattan(self, X1, Y1, X2, Y2): return abs(X1-X2) + abs(Y1-Y2)    

    ##################################################################################################################
    #Draw score as text on screen
    def show_score(self, choice, color, font, size):
        self.score_font = pygame.font.SysFont(font, size)
        self.score_surface = self.score_font.render('Score : ' + str(round(self.score, 3)) + " - " + str(self.starvationTime) + "/" + str(self.maxStarvationTime), True, color)
        self.score_rect = self.score_surface.get_rect()
        if choice == 1:
            self.score_rect.midtop = (self.frame_size_x/4, 15)
        else:
            self.score_rect.midtop = (self.frame_size_x/2, self.frame_size_y/1.25)
        self.game_window.blit(self.score_surface, self.score_rect)
        # pygame.display.flip()

    ##################################################################################################################
    #Spawns a new piece of food randomly on the board
    def spawnNewFood(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True
    
    ##################################################################################################################
    #Given the current direction, move the snake
    def moveSnake(self):
        if self.direction == 'UP': self.snake_pos[1] -= 10
        if self.direction == 'DOWN': self.snake_pos[1] += 10
        if self.direction == 'LEFT': self.snake_pos[0] -= 10
        if self.direction == 'RIGHT': self.snake_pos[0] += 10

    ##################################################################################################################
    #Prints out board, snake, food, and score
    def displayGraphics(self):
        self.game_window.fill(self.black)
        # Snake body
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, self.green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(self.game_window, self.white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
        self.show_score(1, self.white, 'consolas', 20)

        # Refresh game screen
        pygame.display.update()

    ##################################################################################################################
    #Boolean if snake has hit wall or body
    def isGameOver(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10: return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10: return True
        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True
        return False
    
    ##################################################################################################################
    #Add length to the snake if needed, else edit the tail location
    def checkForSnakeGrowth(self):
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.starvationTime = 0
            self.maxStarvationTime += 5
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################
    #####################################################################################

    # Get all relevant information (For bots)
    # Return 1D array (For neural network consistency)
    def getState(self):
        #Code current snake direction as either 1,2,3,4
        snakeDir = 1
        if(self.direction == 'UP'): snakeDir = 1
        elif(self.direction == 'DOWN'): snakeDir = 2
        elif(self.direction == 'LEFT'): snakeDir = 3
        elif(self.direction == 'RIGHT'): snakeDir = 4
        foodX = self.food_pos[0]
        foodY = self.food_pos[1]
        snakeHeadX = self.snake_pos[0]
        snakeHeadY = self.snake_pos[1]
        snakeTailX = self.snake_body[len(self.snake_body)-1][0]
        snakeTailY = self.snake_body[len(self.snake_body)-1][1]
        snakeMidX = self.snake_body[int(len(self.snake_body) / 2) + 1][0]
        snakeMidY = self.snake_body[int(len(self.snake_body) / 2) + 1][1]
        minX = 0
        minY = 0
        maxX = self.frame_size_x-10
        maxY = self.frame_size_y-10

        distanceToFood = self.manhattan(snakeHeadX, snakeHeadY, foodX, foodY)
        distanceToFoodX = snakeHeadX - foodX
        distanceToFoodY = snakeHeadY - foodY

        #Check if snake is in a direct line to food
        DFN = 0 
        if(snakeHeadX == foodX and foodY < snakeHeadY): DFN = 1
        DFS = 0 
        if(snakeHeadX == foodX and foodY > snakeHeadY): DFS = 1
        DFE = 0 
        if(snakeHeadY == foodY and foodX > snakeHeadX): DFE = 1
        DFW = 0 
        if(snakeHeadY == foodY and foodX < snakeHeadX): DFW = 1
        DFNE = 0 
        if(distanceToFoodX == -distanceToFoodY and foodY < snakeHeadY): DFNE = 1 
        DFNW = 0 
        if(distanceToFoodX == distanceToFoodY and foodY < snakeHeadY): DFNW = 1 
        DFSE = 0 
        if(distanceToFoodX == distanceToFoodY and foodY > snakeHeadY): DFSE = 1 
        DFSW = 0 
        if(distanceToFoodX == -distanceToFoodY and foodY > snakeHeadY): DFSW = 1 

        #Bool for if going a direction will result in death the next turn 
        deathN = 0
        deathS = 0
        deathE = 0
        deathW = 0

        #Manhattan distance to closest gameEnder - Snake body or edge
        ND = self.manhattan(snakeHeadX, snakeHeadY, snakeHeadX, minY)
        ED = self.manhattan(snakeHeadX, snakeHeadY, maxX, snakeHeadY)
        SD = self.manhattan(snakeHeadX, snakeHeadY, snakeHeadX, maxY)
        WD = self.manhattan(snakeHeadX, snakeHeadY, minX, snakeHeadY)
        if(ND == 0 or (self.direction == 'UP' and ND == 10)): deathN = 100
        if(SD == 0 or (self.direction == 'DOWN' and SD == 10)): deathS = 100
        if(ED == 0 or (self.direction == 'RIGHT' and ED == 10)): deathE = 100
        if(WD == 0 or (self.direction == 'LEFT' and WD == 10)): deathW = 100
        for x in self.snake_body:
            distance = self.manhattan(snakeHeadX, snakeHeadY, x[0], x[1])
            if(x[0] == snakeHeadX and x[1] < snakeHeadY and distance < ND): 
                if(distance == 10 or (self.direction == 'UP' and distance == 20)): deathN = 100
                ND = distance
            if(x[0] == snakeHeadX and x[1] > snakeHeadY and distance < SD): 
                if(distance == 10 or (self.direction == 'DOWN' and distance == 20)): deathS = 100
                SD = distance
            if(x[1] == snakeHeadY and x[0] > snakeHeadX and distance < ED): 
                if(distance == 10 or (self.direction == 'RIGHT' and distance == 20)): deathE = 100
                ED = distance
            if(x[1] == snakeHeadY and x[0] < snakeHeadX and distance < WD): 
                if(distance == 10 or (self.direction == 'LEFT' and distance == 20)): deathW = 100
                WD = distance

        timeRemaining = self.maxStarvationTime - self.starvationTime
        numPointsAroundHead = 0
        numPointsAroundMid = 0
        numPointsAroundTail = 0
        numPointsAroundFood = 0

        for x in self.snake_body:
            distanceH = self.manhattan(snakeHeadX, snakeHeadY, x[0], x[1])
            distanceM = self.manhattan(snakeMidX, snakeMidY, x[0], x[1])
            distanceT = self.manhattan(snakeTailX, snakeTailY, x[0], x[1])
            distanceF = self.manhattan(foodX, foodY, x[0], x[1])
            if(distanceH) < 50: numPointsAroundHead += 1
            if(distanceM) < 50: numPointsAroundMid += 1
            if(distanceT) < 50: numPointsAroundTail += 1
            if(distanceF) < 50: numPointsAroundFood += 1

        return [distanceToFoodX, distanceToFoodY, deathN, deathS, deathE, deathW, numPointsAroundHead, numPointsAroundMid, numPointsAroundTail, numPointsAroundFood]

    #Sets a state
    def game_overBot(self): 
        self.GameEnded = True
        self.score -= 10

    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    #Main game loop for people playing...
    def loopPlayer(self):
        #self.score -= 1
        #self.starvationTime += 1
        #if(self.starvationTime > 200):
        #    self.game_overBot()
        foodX = self.food_pos[0]
        foodY = self.food_pos[1]
        snakeHeadX = self.snake_pos[0]
        snakeHeadY = self.snake_pos[1]
        self.HistoricalSnakePositions.append([snakeHeadX, snakeHeadY])
        oldDistanceToFood = self.manhattan(snakeHeadX, snakeHeadY, foodX, foodY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'): self.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'): self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'): self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'): self.change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE: pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == 'UP' and self.direction != 'DOWN': self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP': self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT': self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT': self.direction = 'RIGHT'

        # Moving the snake
        self.moveSnake()

        #Snake body growing mechanism
        self.checkForSnakeGrowth()

        #Check if new food should be spawned
        self.spawnNewFood()

        # GFX
        self.displayGraphics()

        #Check if the game is over
        if(self.isGameOver() == True): self.game_over()

        # Refresh rate
        self.fps_controller.tick(self.difficulty)

    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    #Game loop for bots
    def loopBot(self, SuppliedDirection, displayGraphics):
        #Force bot to make moves towards food to survive...
        foodX = self.food_pos[0]
        foodY = self.food_pos[1]
        snakeHeadX = self.snake_pos[0]
        snakeHeadY = self.snake_pos[1]
        self.HistoricalSnakePositions.append([snakeHeadX, snakeHeadY])
        self.starvationTime += 1
        if(self.starvationTime > self.maxStarvationTime): self.game_overBot()
        oldDistanceToFood = self.manhattan(snakeHeadX, snakeHeadY, foodX, foodY)

        #Making sure the snake cannot move in the opposite direction instantaneously
        if SuppliedDirection == 'UP' and self.direction == 'DOWN': self.direction = 'DOWN'
        elif SuppliedDirection == 'DOWN' and self.direction == 'UP': self.direction = 'UP'
        elif SuppliedDirection == 'LEFT' and self.direction == 'RIGHT': self.direction = 'RIGHT'
        elif SuppliedDirection == 'RIGHT' and self.direction == 'LEFT': self.direction = 'LEFT'
        else: self.direction = SuppliedDirection

        # Moving the snake
        self.moveSnake()
        
        newDistanceToFood = self.manhattan(self.snake_pos[0], self.snake_pos[1], foodX, foodY)
        if(newDistanceToFood < oldDistanceToFood): self.score += 0.01
        else: self.score -= 0.001

        # Snake body growing mechanism
        self.checkForSnakeGrowth()

        #Check if new food should be spawned
        self.spawnNewFood()

        # GFX
        if(displayGraphics == True): self.displayGraphics()

        #Check if the game is over
        if(self.isGameOver() == True): self.game_overBot()
        
        # Refresh rate
        self.fps_controller.tick(self.difficulty)

    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    # Test
    def rerunGameInit(self, foodList):
        self.HistoricalFoodList = foodList
        self.GameEnded = False
        self.snake_pos = [250, 250]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = self.HistoricalFoodList.pop(0)
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.GameEnded = False

    def rerunGameLoop(self, SuppliedDirection, displayGraphics):
        #Force bot to make moves towards food to survive...
        foodX = self.food_pos[0]
        foodY = self.food_pos[1]
        snakeHeadX = self.snake_pos[0]
        snakeHeadY = self.snake_pos[1]
        oldDistanceToFood = self.manhattan(snakeHeadX, snakeHeadY, foodX, foodY)

        self.starvationTime += 1
        if(self.starvationTime > 200): self.game_overBot()

        #Making sure the snake cannot move in the opposite direction instantaneously
        if SuppliedDirection == 'UP' and self.direction == 'DOWN': self.score -= 9999
        if SuppliedDirection == 'DOWN' and self.direction == 'UP': self.score -= 9999
        if SuppliedDirection == 'LEFT' and self.direction == 'RIGHT': self.score -= 9999
        if SuppliedDirection == 'RIGHT' and self.direction == 'LEFT': self.score -= 9999
        self.direction = SuppliedDirection

        # Moving the snake
        self.moveSnake()

        newDistanceToFood = self.manhattan(self.snake_pos[0], self.snake_pos[1], foodX, foodY)
        if(newDistanceToFood < oldDistanceToFood): self.score += 0.01
        #else: self.score -= 0.01

        #Snake body growing mechanism
        self.checkForSnakeGrowth()

        #Check if new food should be spawned
        self.spawnNewFood()

        #GFX
        if(displayGraphics == True): self.displayGraphics()
         
        #Check if the game is over
        if(self.isGameOver() == True): self.game_overBot()

        # Refresh rate
        self.fps_controller.tick(30)