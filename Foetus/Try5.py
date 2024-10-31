import pygame
import math
import sys
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human Development Animation")

# Colors
WHITE = (255, 255, 255)
FLESH = (255, 224, 189)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)
GLOW_COLOR = (255, 182, 193)


def create_glow_surface(width, height, color, radius):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    center = (width // 2, height // 2)

    for i in range(radius, 0, -1):
        alpha = int((1 - (i / radius)) * 255)
        color_with_alpha = (*color, alpha)
        pygame.draw.circle(surface, color_with_alpha, center, i)

    return surface


class DevelopmentStage:
    def __init__(self, day, description):
        self.day = day
        self.description = description

    def draw(self, screen, time):
        # Dark background
        screen.fill(DARK_RED)

        # Draw stage description
        font = pygame.font.Font(None, 36)
        text = font.render(f"Day {self.day}: {self.description}", True, WHITE)
        screen.blit(text, (10, 10))

        if self.day >= 56:  # Fetal stage
            self.draw_detailed_fetus(screen, time)
        else:
            self.draw_earlier_stage(screen, time)

    def draw_earlier_stage(self, screen, time):
        # Similar to before but with added glow effects
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Create and apply glow effect
        glow = create_glow_surface(200, 200, GLOW_COLOR, 50)
        screen.blit(glow, (center_x - 100, center_y - 100))

        if self.day <= 5:
            cells = 2 ** min(int(self.day), 3)
            radius = 30
            for i in range(cells):
                angle = (2 * math.pi * i) / cells + time * 0.001
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                pygame.draw.circle(screen, PINK, (int(x), int(y)), 20)

        elif self.day <= 14:
            pygame.draw.circle(screen, PINK, (center_x, center_y), 60)
            pygame.draw.circle(screen, (255, 240, 245), (center_x, center_y), 40)
        else:
            pygame.draw.ellipse(screen, PINK, (center_x - 40, center_y - 60, 80, 120))

    def draw_detailed_fetus(self, screen, time):
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Create and apply main glow effect
        glow = create_glow_surface(400, 400, GLOW_COLOR, 150)
        screen.blit(glow, (center_x - 200, center_y - 200))

        # Draw fetus with more detail
        # Head
        head_x = center_x
        head_y = center_y - 50
        pygame.draw.ellipse(screen, FLESH, (head_x - 35, head_y - 45, 70, 90))

        # Face profile
        points = [
            (head_x - 15, head_y - 20),  # Forehead
            (head_x - 25, head_y),  # Nose
            (head_x - 20, head_y + 15),  # Mouth
            (head_x - 15, head_y + 25)  # Chin
        ]
        pygame.draw.lines(screen, (FLESH[0] - 20, FLESH[1] - 20, FLESH[2] - 20), False, points, 2)

        # Body
        body_angle = math.sin(time * 0.0005) * 0.1
        body_points = [
            (center_x - 20, center_y),  # Upper torso
            (center_x - 15, center_y + 40),  # Mid torso
            (center_x - 10, center_y + 80)  # Lower torso
        ]
        pygame.draw.lines(screen, FLESH, False, body_points, 25)

        # Arms
        arm_start_y = center_y + 20
        # Left arm (curved)
        arm_points = [
            (center_x - 20, arm_start_y),
            (center_x - 40, arm_start_y + 20),
            (center_x - 45, arm_start_y + 40)
        ]
        pygame.draw.lines(screen, FLESH, False, arm_points, 12)

        # Legs
        leg_start_y = center_y + 80
        # Left leg (curved)
        leg_points = [
            (center_x - 10, leg_start_y),
            (center_x - 20, leg_start_y + 30),
            (center_x - 25, leg_start_y + 50)
        ]
        pygame.draw.lines(screen, FLESH, False, leg_points, 15)

        # Add soft shadows
        for point in body_points:
            shadow_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surface, (0, 0, 0, 50), (10, 10), 10)
            screen.blit(shadow_surface, (point[0] - 10, point[1] - 10))


def main():
    clock = pygame.time.Clock()
    current_time = 0

    stages = [
        DevelopmentStage(1, "Zygote"),
        DevelopmentStage(3, "8-cell stage"),
        DevelopmentStage(5, "Morula"),
        DevelopmentStage(14, "Blastocyst"),
        DevelopmentStage(21, "Embryonic disc"),
        DevelopmentStage(28, "Early embryo"),
        DevelopmentStage(56, "Fetus"),
        DevelopmentStage(84, "Developed Fetus")
    ]

    stage_index = 0
    stage_timer = 0
    STAGE_DURATION = 3000  # 3 seconds per stage

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stage_index = (stage_index + 1) % len(stages)
                    stage_timer = 0

        current_time += clock.get_time()
        stage_timer += clock.get_time()

        if stage_timer >= STAGE_DURATION:
            stage_index = (stage_index + 1) % len(stages)
            stage_timer = 0

        stages[stage_index].draw(screen, current_time)

        # Draw progress bar
        progress_width = (stage_timer / STAGE_DURATION) * WIDTH
        pygame.draw.rect(screen, WHITE, (0, HEIGHT - 10, progress_width, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()