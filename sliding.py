import random
import copy
import pygame

# 0 means empty
size = 3 # 3x3 grid
width = 100
height = 100
shuffle = 500 # number of random shuffles to starting grid
valid_moves = ["up", "down", "left", "right"]

# PYGAME CONSTANTS
pygame.init()
CALIBRI = pygame.font.SysFont('calibri', 75)
SCREEN_SIZE = [500, 500]
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.display.set_caption("Sliding Puzzle")

# HELPERS FOR GAME SETUP
# creates grid based on values in val
def generate_grid(vals):
    grid = []
    cur = 0
    for _ in range(0, size):
        new_row = []
        for _ in range(0, size):
            new_row.append(Cell(vals[cur]))
            cur += 1
        grid.append(new_row)
    return grid

# creates default grid with values 1-9
def default_grid():
    return generate_grid([1, 2, 3, 4, 5, 6, 7, 8, ' '])

# HEURISTIC FUNCTIONS FOR A* SEARCH
# returns how far value n is in g, compared to its true position in a default grid
def m(g, n):
    for i in range(size):
        for j in range(size):
            if g.cells[i][j].value == n:
                x_pos = i
                y_pos = j
    real = {1:[0, 0], 2:[0, 1], 3:[0, 2], 4:[1, 0], 5:[1, 1], 6:[1, 2], 
            7:[2, 0], 8:[2, 1]}
    real_x = real[n][0]
    real_y = real[n][1]
    r_v = abs(real_x - x_pos) + abs(real_y - y_pos)
    return r_v

# returns sum total of 'misplaced' tiles in given grid
def df(g):
    count = 0
    for i in range(1, 9):
        count += m(g, i)
    return count

# solve current state of game using the A* search algorithm
def solve(g):
    final_answer = Grid()

    g.draw()
    to_visit = [g]
    cur = to_visit[0]
    visited = [cur]
    while cur != final_answer:
        pygame.event.get()
        for move in valid_moves:
            new = copy.deepcopy(cur)
            try:
                new.swap(move)
            except:
                continue
            if new in visited or new == cur:
                continue
            new.move_list.append(move)
            to_visit.append(new)
        to_visit.pop(0)
        to_visit.sort(key=lambda x: len(x.move_list) + df(x))
        cur = to_visit[0]
        visited.append(cur)
    print(cur.move_list)
    print("solved in {0} moves".format(len(cur.move_list)))
    soln = cur.move_list
    for m in soln:
        g.swap(m)
        g.moves += 1
        pygame.time.delay(200)
        g.draw()

    return len(cur.move_list)

class Cell:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

class Grid:
    def __init__(self, cells=None):
        if cells is None:
            cells = default_grid()
        self.cells = cells
        self.empty = (size - 1, size - 1)
        self.moves = 0
        self.move_list = []

    def __repr__(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                print(self.cells[i][j], end="")
            print()
        return ""

    def __eq__(self, other):
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                if self.cells[i][j] != other.cells[i][j]: 
                    return False
        return True

    # move tile in given direction (if possible)
    #  this is interpreted as swapping the empty square with the appropriate adjacent square
    def swap(self, direction):
        # making sure that new coordinates lie within grid
        def in_range(k, n):
            return 0 <= k < n

        if direction not in valid_moves:
            raise Exception("not a valid key")

        empty_row = self.empty[0]
        empty_column = self.empty[1]
        if direction == "up":
            new_row, new_col = empty_row + 1, empty_column
        elif direction == "down":
            new_row, new_col = empty_row - 1, empty_column
        elif direction == "left":
            new_row, new_col = empty_row, empty_column + 1
        else:
            new_row, new_col = empty_row, empty_column - 1

        if not (in_range(new_row, size) and in_range(new_col, size)):
            raise Exception("out of range")
        self.cells[empty_row][empty_column].value = self.cells[new_row][new_col].value
        self.cells[new_row][new_col].value = ' '
        self.empty = (new_row, new_col)

    def draw(self):
        SCREEN.fill(WHITE)
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(SCREEN, BLACK, [100*i + 100, 100*j + 100, width, height], 1)
                text = CALIBRI.render(str(self.cells[j][i].value), True, BLACK)
                SCREEN.blit(text, [100*i + 133, 100*j + 115])
        font = pygame.font.SysFont('calibri', 55)
        move_count = font.render("Number of moves: " + str(self.moves), True, BLACK)
        SCREEN.blit(move_count, [10, 15])
        pygame.display.flip()

    def display_winner():
        text = CALIBRI.render("Winner!", True, BLACK)
        SCREEN.blit(text, [100, 400])
        pygame.display.flip()
    
def play():
    final_answer = Grid()
    g = Grid()
    
    running = True

    for _ in range(shuffle):
        try:
            g.swap(random.choice(valid_moves))
            g.draw()
        except:
            continue
    
    while(running):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                elif event.key == pygame.K_LEFT:
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                elif event.key == pygame.K_s:
                    solve(g)
                elif event.key == pygame.K_q:
                    running = False

                try:
                    g.swap(direction)
                    direction = ""
                    g.moves += 1
                except:
                    continue
        
            if (g == final_answer):
                g.draw()
                g.display_winner()
                pygame.time.delay(1000)
                running = False
            else:
                g.draw()

    pygame.quit()


play()
