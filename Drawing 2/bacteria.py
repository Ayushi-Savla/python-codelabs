import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 240)  # Off-white background
NUM_BACTERIA = 50
SPEED = 1.0  # Speed for realistic movement
GROWTH_RATE = 0.1  # Growth rate for bacteria
MAX_SIZE = 5  # Maximum size for bacteria (significantly reduced)

# Toxin properties
TOXIN_RADIUS = 5
TOXIN_DURATION = 60  # Duration in frames
SPHERE_RADIUS = 20  # Radius of the sphere around bacteria
MICROSCOPE_RADIUS = 300  # Radius of the microscope lens

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bacteria with Defense Mechanism")

# Bacteria data structure
class Bacterium:
    def __init__(self):
        # Random starting position within the microscope lens
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, MICROSCOPE_RADIUS - 10)  # Stay within the microscope radius
        self.x = SCREEN_WIDTH // 2 + radius * math.cos(angle)
        self.y = SCREEN_HEIGHT // 2 + radius * math.sin(angle)
        self.size = random.randint(2, 5)  # Varying size for realism (significantly reduced)
        self.shape = random.choice(["circle", "rod"])  # Shape selection
        self.angle = random.uniform(0, 2 * math.pi)
        self.dx = SPEED * math.cos(self.angle)
        self.dy = SPEED * math.sin(self.angle)

    def move(self):
        # Simulate random movement
        angle_change = random.uniform(-0.1, 0.1)
        new_dx = self.dx * math.cos(angle_change) - self.dy * math.sin(angle_change)
        new_dy = self.dx * math.sin(angle_change) + self.dy * math.cos(angle_change)
        self.dx, self.dy = new_dx, new_dy

        # Move bacterium
        self.x += self.dx
        self.y += self.dy

        # Constrain movement within the microscope lens
        distance_from_center = math.hypot(self.x - SCREEN_WIDTH // 2, self.y - SCREEN_HEIGHT // 2)
        if distance_from_center > MICROSCOPE_RADIUS - self.size:
            # Calculate the angle to the center and set position at the edge
            angle = math.atan2(self.y - (SCREEN_HEIGHT // 2), self.x - (SCREEN_WIDTH // 2))
            self.x = (MICROSCOPE_RADIUS - self.size) * math.cos(angle) + (SCREEN_WIDTH // 2)
            self.y = (MICROSCOPE_RADIUS - self.size) * math.sin(angle) + (SCREEN_HEIGHT // 2)

    def draw(self):
        # Draw the sphere effect around the bacterium
        pygame.draw.circle(screen, (200, 200, 255, 50), (int(self.x), int(self.y)), SPHERE_RADIUS)

        # Draw the bacterium itself
        if self.shape == "circle":
            pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), self.size)
        elif self.shape == "rod":
            # Create a spherical effect for rod-shaped bacteria by using ellipses
            pygame.draw.ellipse(screen, (0, 0, 255), (self.x - self.size, self.y - self.size // 2, self.size * 2, self.size))

class Toxin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.duration = TOXIN_DURATION

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), TOXIN_RADIUS)

    def update(self):
        self.duration -= 1

def draw_microscope():
    # Draw the microscope lens
    pygame.draw.circle(screen, (100, 100, 100, 150), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), MICROSCOPE_RADIUS)  # Glass effect
    pygame.draw.circle(screen, (0, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), MICROSCOPE_RADIUS, 2)  # Outline

# Create bacteria
bacteria = [Bacterium() for _ in range(NUM_BACTERIA)]
toxins = []

def check_collision(bacteria, toxins):
    for i in range(len(bacteria)):
        for j in range(i + 1, len(bacteria)):
            distance = math.hypot(bacteria[i].x - bacteria[j].x, bacteria[i].y - bacteria[j].y)
            if distance < (bacteria[i].size + bacteria[j].size):
                # Simple rebound behavior
                bacteria[i].dx *= -1
                bacteria[i].dy *= -1
                bacteria[j].dx *= -1
                bacteria[j].dy *= -1

                # Create toxins at the collision point
                toxins.append(Toxin((bacteria[i].x + bacteria[j].x) / 2, (bacteria[i].y + bacteria[j].y) / 2))

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    # Fill the screen with the background color
    screen.fill(BACKGROUND_COLOR)  # Off-white background

    # Draw the microscope lens
    draw_microscope()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw each bacterium
    for bacterium in bacteria:
        bacterium.move()
        bacterium.draw()

    # Update and draw toxins
    for toxin in toxins:
        toxin.draw()
        toxin.update()

    # Remove expired toxins
    toxins = [toxin for toxin in toxins if toxin.duration > 0]

    # Check for collisions between bacteria
    check_collision(bacteria, toxins)

    pygame.display.flip()
    clock.tick(30)  # Set frame rate to 30 FPS

pygame.quit()
