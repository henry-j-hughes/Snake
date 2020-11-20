import pygame
from pygame import mixer
import sys
import random
import os

os.chdir("C:/Users/hjhug\OneDrive\Documents\VisualStudioCode\Snake")

# choose colours (R,G,B)
snake_color = (15, 56, 15)
food_color = (15, 56, 15)
board_light = (139, 172, 15)
board_dark = (130, 160, 15)

class Snake():
    def __init__(self):
        # initialise snake attributes
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = snake_color
        self.score = 0

    def get_head_position(self):
        # return the position of the head of the snake
        return self.positions[0]

    def turn(self, point):
        # if the snake is one block, it can move in any direction
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        # function to move the snake
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        # if the game is lost
        if len(self.positions) > 2 and new in self.positions[2:]:
            # reset the board
            self.reset()
            game_over = mixer.Sound("gameover.mp3")
            game_over.play()
        else:
            # otherwise, grow the snake
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        # when the game ends
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface):
        # create a draw function
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, board_light, r, 1)

    def handle_keys(self):
        # handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        # initialise food properties
        self.position = (0,0)
        self.color = food_color
        self.randomize_position()

    def randomize_position(self):
        # randomise position
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface):
        # draw the food onto the surface
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, board_light, r, 1)

def drawGrid(surface):
    # function that draws the grid
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, board_light, r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, board_dark, rr)

# set global variables

# re: grid
screen_width = 480
screen_height = 480
gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

# re: moves
up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.3)
    pygame.init()

    hstext = open("hstext.txt")
    highscore = int(hstext.read())

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    # soundtrack
    mixer.music.load('hed.wav')
    mixer.music.play(-1)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.Font("8-BitMadness.ttf",26, bold=True)

    while (True):
        clock.tick(5 + round(snake.score/4, 1))
        snake.handle_keys()
        drawGrid(surface)
        snake.move()

        if snake.get_head_position() == food.position:
            eating_sound = mixer.Sound("eat.mp3")
            eating_sound.play()
            snake.length += 1
            snake.score += 1
            
            if snake.score > highscore:
                highscore = snake.score
                hswrite = open("hstext.txt", "w")
                hswrite.write(str(highscore))

            food.randomize_position()
        
        snake.draw(surface)
        food.draw(surface)

        screen.blit(surface, (0,0))
        score = myfont.render("Score {0}".format(snake.score), 1, snake_color)
        screen.blit(score, (5,25))
        high_score = myfont.render("High score {0}".format(highscore), 1, snake_color)
        screen.blit(high_score, (5,5))
        
        # update the display
        pygame.display.update()


# This notation means main() will only run when this script is excecuted
if __name__ == "__main__":
    main()
