import pygame
import sys
import random


pygame.init()


screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

block_size = 30
grid_width = 10
grid_height = 20
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]
shape_fill = [[1, 4], [2, 2], [1, 3, 0], [1, 3, -1], [1, 2, 0], [1, 2, -1]]

shape_colors = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, RED, GREEN]

class Tetromino:


    def __init__(self, shape):

        self.shape = shape
        self.color = shape_colors[shapes.index(self.shape)]
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self, dx, dy):
    
        if self.valid_move(dx, dy):
            self.x += dx
            self.y += dy
            return True
        return False


    def rotate(self):

        rotated = list(zip(*self.shape[::-1]))
        if self.valid_move(0, 0, rotated):
            self.shape = rotated

    def valid_move(self, dx, dy, shape=None):
    
        if shape is None:
            shape = self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = self.x + x + dx, self.y + y + dy
                    if (new_x < 0 or new_x >= grid_width or
                        new_y >= grid_height or
                        (new_y >= 0 and grid[new_y][new_x])):
                        return False
        return True

class Shadow(Tetromino):
    pass
    
def draw_grid():

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * block_size, y * block_size, block_size, block_size))
            pygame.draw.rect(screen, WHITE, (x * block_size, y * block_size, block_size, block_size), 1)

def draw_tetromino(tetromino):

    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino.color,
                                 ((tetromino.x + x) * block_size,
                                  (tetromino.y + y) * block_size,
                                  block_size, block_size))

def merge_tetromino(tetromino):

    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines():

    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for line in full_lines:
        del grid[line]
        grid.insert(0, [0 for _ in range(grid_width)])
    return len(full_lines)

def game_over():

    return any(grid[0])

print(grid)

def choose_block():
    grid_gaps = []
    for i, j in enumerate(grid):
        gaps = []
        track = 0
        track_top = 0
        for k, l in enumerate(j):


            if not(l):
                visiting = []
                visited = []
                a = i
                b = k

                while True:
                    if a > 0:
                        if (grid[a-1][b] == 0) and ([a - 1, b] not in visited) and ([a - 1, b] not in visiting):
                            visiting.append([a - 1, b])
                    else:
                        track += 1
                        break

                    if b < 9:
                        if grid[a][b + 1] == 0 and ([a, b + 1] not in visited) and ([a, b + 1] not in visiting):
                            visiting.append([a, b + 1])
                            
                    if a < 19:
                        if grid[a + 1][b] == 0 and ([a + 1, b] not in visited) and ([a + 1, b] not in visiting):
                            visiting.append([a + 1, b])
                            
                    if b > 0:
                        if grid[a][b - 1] == 0 and ([a, b - 1] not in visited) and ([a, b - 1] not in visiting):
                            visiting.append([a, b - 1])
                    visited.append([a, b])
                    if len(visiting) > 0:
                        x = visiting.pop()
                        a = x[0]
                        b = x[1]

                    else:
                        break
                        
                
            elif k != 9:
                if track != 0:
                    gaps.append(track)
                    track = 0

            if k == 9:
                gaps.append(track)
        grid_gaps.append(gaps)
    grid_gaps.reverse()
    grid_gaps.sort(key=len)
    for i in list(grid_gaps):
        for j in i:
            if j > 4:
                grid_gaps.remove(i)
                break

    fill = list(shape_fill)
    random.shuffle(fill)
    
    for i in grid_gaps:
        for j in i:
            for k in fill:
                if j in k:
                    fill.remove(k)
                    break         
            if len(fill) == 1:
                break
        if len(fill) == 1:
            break
    print(len(fill))
    x = random.choice(fill)
    return(shapes[shape_fill.index(x)])
    
    

def main():
    clock = pygame.time.Clock()
    tetromino = Tetromino(random.choice(shapes))
    fall_time = 0
    fall_speed = 0.5
    score = 0

    while True:
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetromino.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    tetromino.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    tetromino.move(0, 1)
                elif event.key == pygame.K_SPACE:
                    while tetromino.move(0, 1):
                        pass
                elif event.key == pygame.K_UP:
                    tetromino.rotate()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            if not tetromino.move(0, 1):
                merge_tetromino(tetromino)
                lines_cleared = clear_lines()
                score += lines_cleared * 100
                tetromino = Tetromino(choose_block())
                if game_over():
                    print(f"Game Over! Score: {score}")
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        draw_grid()
        draw_tetromino(tetromino)
        pygame.display.flip()

if __name__ == "__main__":
    main()
