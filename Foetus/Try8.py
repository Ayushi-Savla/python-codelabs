import math
import pygame
import cairo
import numpy as np

# Set up Pygame window dimensions and FPS
WIDTH, HEIGHT = 600, 600
FPS = 30
FRAMES = 60  # Number of frames for the animation

def cairo_surface_to_pygame(surface):
    # Convert Cairo surface to a Pygame surface
    buf = surface.get_data()
    data = np.ndarray(shape=(HEIGHT, WIDTH, 4),
                      dtype=np.uint8,
                      buffer=buf)
    data = np.roll(data, 1, axis=2)  # Swap channels from ARGB to RGBA
    pygame_surface = pygame.image.frombuffer(data.tobytes(), (WIDTH, HEIGHT), 'RGBA')
    return pygame_surface


def draw_glow(context, center_x, center_y, radius, color):
    gradient = cairo.RadialGradient(center_x, center_y, radius * 0.1, center_x, center_y, radius)
    gradient.add_color_stop_rgba(0, *color, 0.8)
    gradient.add_color_stop_rgba(1, *color, 0.0)  # Fade out to transparent

    context.set_source(gradient)
    context.arc(center_x, center_y, radius, 0, 2 * math.pi)
    context.fill()


def draw_embryo(context, center_x, center_y, progress):
    # More organic embryo shape with smooth transitions
    scale = 0.5 + progress * 0.4
    context.save()
    context.translate(center_x, center_y)
    context.scale(scale * 300, scale * 400)

    # Embryo shape that evolves
    if progress < 0.3:
        # Early stage - circular/oval
        context.arc(0, 0, 0.5, 0, 2 * math.pi)
    elif progress < 0.6:
        # Middle stage - the shape starts curving
        context.move_to(-0.3, -0.4)
        context.curve_to(0.5, -0.5, 0.6, 0.3, 0, 0.4)
        context.curve_to(-0.5, 0.4, -0.6, -0.3, -0.3, -0.4)
    else:
        # Late stage - more detailed curve
        context.move_to(0, -0.4)
        context.curve_to(0.4, -0.3, 0.5, 0.3, 0, 0.5)
        context.curve_to(-0.5, 0.3, -0.4, -0.3, 0, -0.4)

    # Pinkish fill with slight glow
    gradient = cairo.RadialGradient(0, 0, 0.1, 0, 0, 0.5)
    gradient.add_color_stop_rgba(0, 1, 0.5, 0.5, 0.8)
    gradient.add_color_stop_rgba(1, 0.8, 0.3, 0.3, 0.5)
    context.set_source(gradient)
    context.fill()

    context.restore()


def draw_environment(context, center_x, center_y, progress):
    # Background with soft radial gradient
    gradient = cairo.RadialGradient(center_x, center_y, 50, center_x, center_y, WIDTH // 2)
    gradient.add_color_stop_rgb(0, 0.05, 0.05, 0.1)  # Dark center
    gradient.add_color_stop_rgb(1, 0.1, 0.05, 0.2)  # Softer outer area

    context.set_source(gradient)
    context.rectangle(0, 0, WIDTH, HEIGHT)
    context.fill()


def create_frame(frame_number, total_frames):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    context = cairo.Context(surface)

    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    radius = 150
    progress = frame_number / total_frames

    # Draw environment
    draw_environment(context, center_x, center_y, progress)

    # Glow effect around the embryo
    draw_glow(context, center_x, center_y, radius * 1.2, (1, 0.5, 0.5))  # Soft pinkish glow

    # Draw embryo with progression
    draw_embryo(context, center_x, center_y, progress)

    return surface


def run_pygame_animation():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Embryo Development Animation")
    clock = pygame.time.Clock()

    frame = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Create current frame using Cairo
        surface = create_frame(frame, FRAMES)
        pygame_surface = cairo_surface_to_pygame(surface)

        # Display the frame on the Pygame window
        screen.blit(pygame_surface, (0, 0))
        pygame.display.flip()

        # Increment the frame counter
        frame = (frame + 1) % FRAMES  # Loop animation

        # Control the frame rate
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run_pygame_animation()
