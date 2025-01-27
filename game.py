import pygame
import random

# Constants
WIDTH = 608
HEIGHT = 672
BLOCK_SIZE = 32
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Maze layout
maze_layout = [
    "#############################",
    "#...............#...........#",
    "#.####.#####.###.#.#####.####",
    "#.................#.........#",
    "#.####.#.###.# #####.#.####.#",
    "#......#...#.......#.....#...#",
    "###### ### # ##### # ### #####",
    "     #.#   #   #   # #.#     ",
    "######.# #-#####-# # #.######",
    "     .  #         #  #.     ",
    "######.# #####-##### #.######",
    "#...............#............#",
    "#.#####.# ##### # #######.###",
    "#...#.......#.......#.....#..#",
    "###.#.#.##### # # ###.#####.##",
    "#.....#.#     # #   #.#.....##",
    "#.#####.# #####-##### #.#####",
    "#............................#",
    "#############################",
]

def is_wall(x, y):
    # Convert pixel coordinates to grid coordinates
    row = int(y // BLOCK_SIZE)
    col = int(x // BLOCK_SIZE)
    
    # Check bounds
    if row < 0 or row >= len(maze_layout) or col < 0 or col >= len(maze_layout[0]):
        return True
        
    return maze_layout[row][col] == '#'

def get_valid_directions(x, y):
    valid = []
    # Check each direction (up, down, left, right)
    if not is_wall(x, y - BLOCK_SIZE):  # Up
        valid.append(1)
    if not is_wall(x, y + BLOCK_SIZE):  # Down
        valid.append(2)
    if not is_wall(x - BLOCK_SIZE, y):  # Left
        valid.append(3)
    if not is_wall(x + BLOCK_SIZE, y):  # Right
        valid.append(4)
    return valid

class Pacman:
    def __init__(self):
        self.x = BLOCK_SIZE * 10
        self.y = BLOCK_SIZE * 15
        self.direction = 0  # 0: stop, 1: up, 2: down, 3: left, 4: right
        self.speed = 2
        self.mouth_open = True
        self.mouth_counter = 0

    def move(self):
        # Store previous position
        prev_x = self.x
        prev_y = self.y

        # Try to move
        if self.direction == 1:
            self.y -= self.speed
        elif self.direction == 2:
            self.y += self.speed
        elif self.direction == 3:
            self.x -= self.speed
        elif self.direction == 4:
            self.x += self.speed

        # Check for wall collision
        if is_wall(self.x, self.y):
            self.x = prev_x
            self.y = prev_y

        # Simple animation for mouth
        self.mouth_counter += 1
        if self.mouth_counter >= 10:
            self.mouth_open = not self.mouth_open
            self.mouth_counter = 0

class Ghost:
    def __init__(self, color):
        self.x = BLOCK_SIZE * 13
        self.y = BLOCK_SIZE * 11
        self.color = color
        self.direction = random.randint(1, 4)
        self.speed = 1
        self.move_counter = 0

    def move(self):
        if self.move_counter > 0:
            self.move_counter -= 1
            return

        # Store previous position
        prev_x = self.x
        prev_y = self.y

        # Get valid directions
        valid_dirs = get_valid_directions(self.x, self.y)
        
        if valid_dirs:
            # If current direction is valid, 80% chance to keep going
            if self.direction in valid_dirs and random.random() < 0.8:
                pass
            else:
                # Otherwise choose a random valid direction
                self.direction = random.choice(valid_dirs)
            
            # Move in chosen direction
            if self.direction == 1:
                self.y -= self.speed
            elif self.direction == 2:
                self.y += self.speed
            elif self.direction == 3:
                self.x -= self.speed
            elif self.direction == 4:
                self.x += self.speed

            # Check for wall collision
            if is_wall(self.x, self.y):
                self.x = prev_x
                self.y = prev_y
                self.direction = random.choice(valid_dirs)  # Choose new direction if we hit a wall

        self.move_counter = random.randint(5, 15)  # Shorter intervals for more responsive movement

def draw_maze(screen):
    for row in range(len(maze_layout)):
        for col in range(len(maze_layout[row])):
            if maze_layout[row][col] == '#':
                x = col * BLOCK_SIZE
                y = row * BLOCK_SIZE
                
                # Check top neighbor
                if row == 0 or col >= len(maze_layout[row-1]) or maze_layout[row-1][col] != '#':
                    pygame.draw.line(screen, BLUE, (x, y), (x + BLOCK_SIZE, y), 3)
                
                # Check bottom neighbor
                if row == len(maze_layout)-1 or col >= len(maze_layout[row+1]) or maze_layout[row+1][col] != '#':
                    pygame.draw.line(screen, BLUE, (x, y + BLOCK_SIZE), (x + BLOCK_SIZE, y + BLOCK_SIZE), 3)
                
                # Check left neighbor
                if col == 0 or maze_layout[row][col-1] != '#':
                    pygame.draw.line(screen, BLUE, (x, y), (x, y + BLOCK_SIZE), 3)
                
                # Check right neighbor
                if col == len(maze_layout[row])-1 or maze_layout[row][col+1] != '#':
                    pygame.draw.line(screen, BLUE, (x + BLOCK_SIZE, y), (x + BLOCK_SIZE, y + BLOCK_SIZE), 3)
            
            elif maze_layout[row][col] == '.':
                pygame.draw.circle(screen, WHITE, (col*BLOCK_SIZE + BLOCK_SIZE//2, row*BLOCK_SIZE + BLOCK_SIZE//2), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()

    pacman = Pacman()
    ghost = Ghost(RED)
    score = 0

    running = True
    while running:
        screen.fill(BLACK)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.direction = 1
                elif event.key == pygame.K_DOWN:
                    pacman.direction = 2
                elif event.key == pygame.K_LEFT:
                    pacman.direction = 3
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = 4

        # Move characters
        pacman.move()
        ghost.move()
        
        # Collect dots
        row = int(pacman.y // BLOCK_SIZE)
        col = int(pacman.x // BLOCK_SIZE)
        if 0 <= row < len(maze_layout) and 0 <= col < len(maze_layout[row]):
            if maze_layout[row][col] == '.':
                maze_layout[row] = maze_layout[row][:col] + ' ' + maze_layout[row][col+1:]
                score += 10

        # Draw everything
        draw_maze(screen)
        
        # Draw Pacman
        if pacman.mouth_open:
            pygame.draw.circle(screen, YELLOW, (pacman.x, pacman.y), BLOCK_SIZE//2)
        else:
            pygame.draw.circle(screen, YELLOW, (pacman.x, pacman.y), BLOCK_SIZE//2)
            # Draw mouth for each direction
            if pacman.direction == 1:  # Up
                pygame.draw.polygon(screen, BLACK, [
                    (pacman.x, pacman.y),
                    (pacman.x - BLOCK_SIZE//2, pacman.y + BLOCK_SIZE//2),
                    (pacman.x + BLOCK_SIZE//2, pacman.y + BLOCK_SIZE//2)
                ])
            elif pacman.direction == 2:  # Down
                pygame.draw.polygon(screen, BLACK, [
                    (pacman.x, pacman.y),
                    (pacman.x - BLOCK_SIZE//2, pacman.y - BLOCK_SIZE//2),
                    (pacman.x + BLOCK_SIZE//2, pacman.y - BLOCK_SIZE//2)
                ])
            elif pacman.direction == 3:  # Left
                pygame.draw.polygon(screen, BLACK, [
                    (pacman.x, pacman.y),
                    (pacman.x + BLOCK_SIZE//2, pacman.y - BLOCK_SIZE//2),
                    (pacman.x + BLOCK_SIZE//2, pacman.y + BLOCK_SIZE//2)
                ])
            elif pacman.direction == 4:  # Right
                pygame.draw.polygon(screen, BLACK, [
                    (pacman.x, pacman.y),
                    (pacman.x - BLOCK_SIZE//2, pacman.y - BLOCK_SIZE//2),
                    (pacman.x - BLOCK_SIZE//2, pacman.y + BLOCK_SIZE//2)
                ])

        # Draw Ghost
        pygame.draw.circle(screen, ghost.color, (ghost.x, ghost.y), BLOCK_SIZE//2)

        # Check collision with ghost
        if abs(pacman.x - ghost.x) < BLOCK_SIZE and abs(pacman.y - ghost.y) < BLOCK_SIZE:
            print("Game Over!")
            running = False

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()