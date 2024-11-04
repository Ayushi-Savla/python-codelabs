import math
import sys
import cairo
import pygame
from PIL import Image

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
FPS = 60
RADIUS = 250

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-time Rotating Sphere")


# Function to draw the rotating sphere using Cairo and Pygame
def draw_rotating_sphere(center_x, center_y, radius, texture_path, angle):
    # Create a new Cairo surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    context = cairo.Context(surface)

    # Open the texture image using Pillow and rotate it
    texture_image = Image.open(texture_path)
    rotated_texture = texture_image.rotate(angle, resample=Image.BICUBIC).convert("RGBA")

    # Convert the rotated image to raw RGBA data for Cairo
    img_width, img_height = rotated_texture.size
    raw_data = rotated_texture.tobytes("raw", "BGRA")
    texture_surface = cairo.ImageSurface.create_for_data(
        bytearray(raw_data), cairo.FORMAT_ARGB32, img_width, img_height
    )
    texture_pattern = cairo.SurfacePattern(texture_surface)

    # Calculate the scale factor to fit the texture to the sphere's diameter
    scale_factor = (radius * 2) / max(img_width, img_height)

    # Apply transformations and draw the texture as the sphere's surface
    context.save()
    context.translate(center_x - radius, center_y - radius)
    context.scale(scale_factor, scale_factor)
    context.set_source(texture_pattern)
    context.paint()
    context.restore()

    # Convert the Cairo surface to a format Pygame can display
    cairo_surface_data = surface.get_data()
    pygame_surface = pygame.image.frombuffer(cairo_surface_data, (WIDTH, HEIGHT), "RGBA")
    return pygame_surface


# Main loop to animate the rotation
clock = pygame.time.Clock()
angle = 0  # Start with no rotation

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the rotating sphere and update the display
    sphere_surface = draw_rotating_sphere(WIDTH // 2, HEIGHT // 2, RADIUS, 'earth.jpg', angle)
    screen.blit(sphere_surface, (0, 0))

    # Update the rotation angle
    angle += 1  # Adjust this value for faster or slower rotation

    # Update the display and limit FPS
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
