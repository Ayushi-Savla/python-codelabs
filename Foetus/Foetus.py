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


class DevelopmentStage:
    def __init__(self, day, description):
        self.day = day
        self.description = description

    def draw(self, screen, time):
        # Clear screen
        screen.fill(WHITE)

        # Draw stage description
        font = pygame.font.Font(None, 36)
        text = font.render(f"Day {self.day}: {self.description}", True, BLACK)
        screen.blit(text, (10, 10))

        if self.day <= 5:  # Early cell division stages
            self.draw_early_stage(screen, time)
        elif self.day <= 14:  # Blastocyst stage
            self.draw_blastocyst(screen, time)
        elif self.day <= 21:  # Embryonic disc
            self.draw_embryonic_disc(screen, time)
        else:  # Fetal stage
            self.draw_fetus(screen, time)

    def draw_early_stage(self, screen, time):
        cells = 2 ** min(int(self.day), 3)
        radius = 30
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        for i in range(cells):
            angle = (2 * math.pi * i) / cells + time * 0.001
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            pygame.draw.circle(screen, PINK, (int(x), int(y)), 20)

    def draw_blastocyst(self, screen, time):
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Outer circle
        pygame.draw.circle(screen, PINK, (center_x, center_y), 60)
        # Inner cavity
        pygame.draw.circle(screen, WHITE, (center_x, center_y), 40)
        # Inner cell mass
        pygame.draw.circle(screen, PINK, (center_x + 20, center_y - 20), 20)

    def draw_embryonic_disc(self, screen, time):
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Draw embryonic disc shape
        pygame.draw.ellipse(screen, PINK, (center_x - 40, center_y - 60, 80, 120))
        # Neural tube formation
        pygame.draw.line(screen, BLACK, (center_x, center_y - 50), (center_x, center_y + 50), 3)

    def draw_fetus(self, screen, time):
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Head
        pygame.draw.circle(screen, FLESH, (center_x, center_y - 30), 25)

        # Body
        pygame.draw.ellipse(screen, FLESH, (center_x - 20, center_y, 40, 60))

        # Arms
        angle = math.sin(time * 0.001) * 0.3
        arm_length = 30

        # Left arm
        start_x = center_x - 20
        start_y = center_y + 20
        end_x = start_x - arm_length * math.cos(angle)
        end_y = start_y + arm_length * math.sin(angle)
        pygame.draw.line(screen, FLESH, (start_x, start_y), (int(end_x), int(end_y)), 8)

        # Right arm
        start_x = center_x + 20
        end_x = start_x + arm_length * math.cos(angle)
        pygame.draw.line(screen, FLESH, (start_x, start_y), (int(end_x), int(end_y)), 8)

        # Legs
        leg_angle = math.sin(time * 0.001 + math.pi) * 0.2
        leg_length = 40

        # Left leg
        start_x = center_x - 10
        start_y = center_y + 60
        end_x = start_x - leg_length * math.sin(leg_angle)
        end_y = start_y + leg_length * math.cos(leg_angle)
        pygame.draw.line(screen, FLESH, (start_x, start_y), (int(end_x), int(end_y)), 8)

        # Right leg
        start_x = center_x + 10
        end_x = start_x + leg_length * math.sin(leg_angle)
        pygame.draw.line(screen, FLESH, (start_x, start_y), (int(end_x), int(end_y)), 8)


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
        DevelopmentStage(56, "Fetus")
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
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - 10, progress_width, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()