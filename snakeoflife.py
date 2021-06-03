import sys
import numpy as np
import random
import pygame

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)
RED = (255,0,0)
BLUE = (0,0,255)


class Grid(object):

    def __init__(self, surface, size, rows):

        self.surface = surface
        self.size = size
        self.rows = rows
        self.row_size = self.size // self.rows

        self.grid = np.full((self.rows,self.rows), 'O', dtype=str)

    def draw_grid(self):

        x = 0
        y = 0

        for i in range(self.rows):
            x += self.row_size
            y += self.row_size
            pygame.draw.line(self.surface, GREY, (x,0), (x, self.size))
            pygame.draw.line(self.surface, GREY, (0,y), (self.size, y))

    def redraw_window(self,snake):

        self.surface.fill(WHITE)

        self.draw_snake(snake)
        self.add_food()
        self.draw_food()
        self.color_cells()
        self.draw_grid()

        pygame.display.update()

    def color_cells(self):

        for i in range(self.rows):
            for j in range(self.rows):

                if self.grid.item((i,j)) == 'O':  # Empty
                    color = WHITE
                elif self.grid.item((i,j)) == 'C': # Conway cells
                    color = BLACK
                elif self.grid.item((i,j)) == 'S': # Snake
                    color = BLUE
                elif self.grid.item((i,j)) == 'F': # Food
                    color = RED
                else:
                    print('error')

                pygame.draw.rect(self.surface, color, (i*self.row_size, j*self.row_size, self.row_size, self.row_size))

    def add_conway_patterns(self,pattern='',snake_head=''):

        # Find a random postion which is not around the snake's head
        if snake_head:
            around_head = True
            while around_head:
                i = random.randint(1, self.rows-3)
                j = random.randint(1, self.rows-3)
                if (abs(snake_head[0]-i)>4) and (abs(snake_head[1]-j)>4):
                    around_head = False

        if not pattern:
            pattern = random.choice(['Glider1','Glider2','Glider3','Glider4','Mathusalem'])

        if pattern == 'Blinker':
            self.grid[i][j] = 'C'
            self.grid[i][j+1] = 'C'
            self.grid[i][j+2] = 'C'

        elif pattern == 'Toad':
            self.grid[i][j-1] = 'C'
            self.grid[i][j] = 'C'
            self.grid[i][j+1] = 'C'
            self.grid[i+1][j] = 'C'
            self.grid[i+1][j+1] = 'C'
            self.grid[i+1][j+2] = 'C'

        elif pattern == 'Glider1':
            self.grid[i][j] = 'C'
            self.grid[i+1][j+1] = 'C'
            self.grid[i-1][j+2] = 'C'
            self.grid[i][j+2] = 'C'
            self.grid[i+1][j+2] = 'C'

        elif pattern == 'Glider2':
            self.grid[i-1][j-1] = 'C'
            self.grid[i-1][j] = 'C'
            self.grid[i-1][j+1] = 'C'
            self.grid[i][j+1] = 'C'
            self.grid[i+1][j] = 'C'

        elif pattern == 'Glider3':
            self.grid[i-1][j-1] = 'C'
            self.grid[i][j-1] = 'C'
            self.grid[i+1][j-1] = 'C'
            self.grid[i-1][j] = 'C'
            self.grid[i][j+1] = 'C'

        elif pattern == 'Glider4':
            self.grid[i+1][j-1] = 'C'
            self.grid[i+1][j] = 'C'
            self.grid[i+1][j+1] = 'C'
            self.grid[i][j-1] = 'C'
            self.grid[i-1][j] = 'C'

        elif pattern == 'Mathusalem':
            self.grid[i+1][j-1] = 'C'
            self.grid[i-1][j] = 'C'
            self.grid[i][j] = 'C'
            self.grid[i+1][j] = 'C'
            self.grid[i][j+1] = 'C'

    def run_conway(self):

        # Save food postion
        save_food = np.where(self.grid=='F', 'F', 0)

        # Game of life rules for Conway cells
        conway_grid = np.where(self.grid=='C', 1, 0)
        neighbour = np.zeros(conway_grid.shape)

        # To get the number of neighbourbour cells
        neighbour[1:-1,1:-1] = (conway_grid[:-2,:-2]  + conway_grid[:-2,1:-1] + conway_grid[:-2,2:] +
                                conway_grid[1:-1,:-2] +                         conway_grid[1:-1,2:] +
                                conway_grid[2:,:-2]   + conway_grid[2:,1:-1]  + conway_grid[2:,2:])

        # Updated state cells
        updated_grid = np.zeros(conway_grid.shape, dtype=int)
        updated_grid[np.where(neighbour==3)]= 1
        updated_grid[np.where(neighbour==2)]=conway_grid[np.where(neighbour==2)]

        # New Conway cells postion and add saved food postion
        self.grid = np.where(updated_grid==1, 'C', 'O')
        self.grid = np.where(save_food=='F', 'F', self.grid)

    def draw_snake(self,snake):

        # Erase previous snake position
        self.grid = np.where(self.grid=='S', 'O', self.grid)

        # Add new snake postion
        for pos in snake.pos_list:
            self.grid[pos[0]][pos[1]] = 'S'


    def add_food(self):

        # Add new food if not anymore on the grid
        if not 'F' in self.grid:
            self.food_x = random.randint(1, self.rows-2)
            self.food_y = random.randint(1, self.rows-2)
            self.grid[self.food_x][self.food_y] = 'F'

    def draw_food(self):

        # Transform Conway cells into food if adjacent to food
        for i in range(self.rows):
            for j in range(self.rows):
                if self.grid.item((i,j)) == 'F':
                    if self.grid.item((i+1,j)) == 'C':
                        self.grid[i+1][j] = 'F'
                    if self.grid.item((i-1,j)) == 'C':
                        self.grid[i-1][j] = 'F'
                    if self.grid.item((i,j+1)) == 'C':
                        self.grid[i][j+1] = 'F'
                    if self.grid.item((i,j-1)) == 'C':
                        self.grid[i][j-1] = 'F'


class Snake(object):

    def __init__(self, pos):
        self.dir_x = 0
        self.dir_y = 1
        self.pos = pos
        self.pos_list= [pos]
        self.lenght = 1

    def move(self):

        # Get pressed keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.dir_x != 1:
                    self.dir_x = -1
                    self.dir_y = 0

                elif keys[pygame.K_RIGHT] and self.dir_x != -1:
                    self.dir_x = 1
                    self.dir_y = 0

                elif keys[pygame.K_UP] and self.dir_y != 1:
                    self.dir_x = 0
                    self.dir_y = -1

                elif keys[pygame.K_DOWN] and self.dir_y != -1:
                    self.dir_x = 0
                    self.dir_y = 1

        # Update snake postion
        self.pos_list.insert(0,(self.pos_list[0][0]+self.dir_x,self.pos_list[0][1]+self.dir_y))
        if len(self.pos_list) > self.lenght:
            self.pos_list.pop(self.lenght)

        # Check for collision with walls
        if self.dir_x == -1 and self.pos_list[0][0] < 0:
            sys.exit()
        if self.dir_x == 1 and self.pos_list[0][0] > rows:
            sys.exit()
        if self.dir_y == 1 and self.pos_list[0][1] >= rows:
            sys.exit()
        if self.dir_y == -1 and self.pos_list[0][1] < 0:
            sys.exit()

        # Check for collision with itself
        if self.pos_list[0] in self.pos_list[1:]:
            sys.exit()

    def check_food(self, grid):
        i = self.pos_list[0][0]
        j = self.pos_list[0][1]
        if grid.grid[i][j] == 'F':
            self.lenght +=1

    def check_conway_collision(self, grid):
        i = self.pos_list[0][0]
        j = self.pos_list[0][1]
        if grid.grid[i][j] == 'C':
            sys.exit()


def main():

    if len(sys.argv) > 1:
        if sys.argv[1] == '1':
            level = 1
        elif sys.argv[1] == '2':
            level = 2
        elif sys.argv[1] == '3':
            level = 3
        else:
            print('Not a valid level!')
            sys.exit()
    else:
        level = 1

    # Options
    global rows
    size = 600 # px
    rows = 30

    # Level definition
    delay = {1:150,2:100,3:50}
    tick = {1:10,2:14,3:20}
    every = {1:3,2:2,3:1}

    # Set game
    window = pygame.display.set_mode((size,size))
    grid = Grid(window,size,rows)
    grid.add_food()

    # Add snake
    snake = Snake((10,10))

    # Set main loop
    clock = pygame.time.Clock()

    flag = True
    last_len = 0
    score = 0

    while flag:

        pygame.time.delay(delay[level])
        clock.tick(tick[level])

        snake.move()
        snake.check_food(grid)
        snake.check_conway_collision(grid)

        # Add Conway pattern every "every[level]" food eaten
        if last_len != snake.lenght:
            if snake.lenght % every[level] == 0:
                grid.add_conway_patterns('',snake.pos_list[0])
                last_len = snake.lenght

        # Print score in the termial when it changes
        if score < snake.lenght:
            print('Score:', snake.lenght)
            score = snake.lenght

        grid.run_conway()
        grid.redraw_window(snake)

main()
