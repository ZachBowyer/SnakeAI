import pygame, sys, time, random

#Wrapper around the Snake code supplied
class SnakeGameClass:

    #Constructor
    def __init__(self, speed, sizeX, sizeY):
        self.difficulty = speed
        self.frame_size_x = sizeX
        self.frame_size_y = sizeY
        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')
        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        # Colors (R, G, B)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        # Game variables
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.GameEnded = False
    
    def game_over(self):
        self.my_font = pygame.font.SysFont('times new roman', 90)
        self.game_over_surface = self.my_font.render('YOU DIED', True, self.red)
        self.game_over_rect = self.game_over_surface.get_rect()
        self.game_over_rect.midtop = (self.frame_size_x/2, self.frame_size_y/4)
        self.game_window.fill(self.black)
        self.game_window.blit(self.game_over_surface, self.game_over_rect)
        self.show_score(0, self.red, 'times', 20)
        self.GameEnded = True
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
    
    
    # Score
    def show_score(self, choice, color, font, size):
        self.score_font = pygame.font.SysFont(font, size)
        self.score_surface = self.score_font.render('Score : ' + str(self.score), True, color)
        self.score_rect = self.score_surface.get_rect()
        if choice == 1:
            self.score_rect.midtop = (self.frame_size_x/10, 15)
        else:
            self.score_rect.midtop = (self.frame_size_x/2, self.frame_size_y/1.25)
        self.game_window.blit(self.score_surface, self.score_rect)
        # pygame.display.flip()

    #Main game loop for people playing...
    def loopPlayer(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Moving the snake
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        # Spawning food on the screen
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True

        # GFX
        self.game_window.fill(self.black)
        for pos in self.snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(self.game_window, self.green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(self.game_window, self.white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            self.game_over()
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            self.game_over()
        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over()

        self.show_score(1, self.white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        self.fps_controller.tick(self.difficulty)

    #####################################################################################
    # Code we wrote, bots will use this mainly

    # Get all relevant information (For bots)
    def getCurrentBoard(self):
        return [self.snake_pos, self.snake_body, self.frame_size_x-10, self.frame_size_y-10]

    #Sets a state
    def game_overBot(self):
        self.GameEnded = True
    
    def get_score(self):
        return self.score

    #Game loop for bots
    def loopBot(self, SuppliedDirection, displayGraphics):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        #if self.change_to == 'UP' and self.direction != 'DOWN':
        #    self.direction = 'UP'
        #if self.change_to == 'DOWN' and self.direction != 'UP':
        #    self.direction = 'DOWN'
        #if self.change_to == 'LEFT' and self.direction != 'RIGHT':
        #    self.direction = 'LEFT'
        #if self.change_to == 'RIGHT' and self.direction != 'LEFT':
        #    self.direction = 'RIGHT'

        # Moving the snake
        if SuppliedDirection == 'UP':
            self.snake_pos[1] -= 10
        if SuppliedDirection == 'DOWN':
            self.snake_pos[1] += 10
        if SuppliedDirection == 'LEFT':
            self.snake_pos[0] -= 10
        if SuppliedDirection == 'RIGHT':
            self.snake_pos[0] += 10

        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        # Spawning food on the screen
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True

        if(displayGraphics == True):
            # GFX
            self.game_window.fill(self.black)
            for pos in self.snake_body:
                # Snake body
                # .draw.rect(play_surface, color, xy-coordinate)
                # xy-coordinate -> .Rect(x, y, size_x, size_y)
                pygame.draw.rect(self.game_window, self.green, pygame.Rect(pos[0], pos[1], 10, 10))

            # Snake food
            pygame.draw.rect(self.game_window, self.white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            self.game_overBot()
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            self.game_overBot()
        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_overBot()

        self.show_score(1, self.white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        self.fps_controller.tick(self.difficulty)
