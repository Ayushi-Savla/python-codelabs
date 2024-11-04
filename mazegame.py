import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 500
CELL_SIZE = 40
MARBLE_RADIUS = 15
SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)  # Define pink color

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marble Maze")

# Marble position
marble_pos = [CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 1 + CELL_SIZE // 2]  # Start in an open space

# Maze layout
maze = [
    "#################",
    "#       #       #",
    "# ##### # ##### #",
    "# #   #   #   # #",
    "# # ### # # # # #",
    "# # #   #   # # #",
    "# # #####  ###  #",
    "#               #",
    "#################",
]

# Function to draw the maze
def draw_maze():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw a gradient circle to simulate a sphere
def draw_sphere(position):
    # Draw gradient circles to create a 3D effect with dark outside and light inside
    for i in range(MARBLE_RADIUS, 0, -1):
        # Calculate the color value based on the radius
        color_value = int(255 * ((MARBLE_RADIUS - i) / MARBLE_RADIUS))  # Darker on the outside
        color = (255, color_value, color_value)  # Full pink with varying shades
        pygame.draw.circle(screen, color, (position[0], position[1]), i)

# Check for collisions with walls
def is_collision(position):
    x, y = position
    # Calculate the cell position
    cell_x = x // CELL_SIZE
    cell_y = y // CELL_SIZE
    # Check if the cell is a wall
    if maze[cell_y][cell_x] == "#":
        return True
    return False

# Main game loop
def main():
    global marble_pos  # Declare marble_pos as global
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        new_marble_pos = marble_pos.copy()

        if keys[pygame.K_LEFT]:
            new_marble_pos[0] -= SPEED
        if keys[pygame.K_RIGHT]:
            new_marble_pos[0] += SPEED
        if keys[pygame.K_UP]:
            new_marble_pos[1] -= SPEED
        if keys[pygame.K_DOWN]:
            new_marble_pos[1] += SPEED

        # Check for collision before updating position
        if not is_collision(new_marble_pos):
            marble_pos = new_marble_pos

        # Clear the screen
        screen.fill(WHITE)

        # Draw the maze and the marble
        draw_maze()
        draw_sphere(marble_pos)

        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
