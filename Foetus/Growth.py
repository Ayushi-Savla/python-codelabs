import math
import cairo
import time
import os
from PIL import Image

# Define dimensions
WIDTH, HEIGHT = 600, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)


def draw_womb(context, center_x, center_y, radius):
    # Draw the outer womb shape
    context.arc(center_x, center_y, radius, 0, 2 * math.pi)

    # Create a radial gradient for the womb effect
    gradient = cairo.RadialGradient(center_x - radius * 0.5, center_y - radius * 0.5, radius * 0.2,
                                    center_x, center_y, radius)
    gradient.add_color_stop_rgb(0, 1, 0.8, 0.8)  # Light pink at the center
    gradient.add_color_stop_rgb(0.7, 1, 0.5, 0.5)  # Mid pink
    gradient.add_color_stop_rgb(1, 0.8, 0.2, 0.2)  # Darker pink towards the edge

    context.set_source(gradient)
    context.fill()


# Prepare images for each growth stage (update paths to your images)
stages = [
    "/Images/zygote1.jpg",  # Image of zygote
    "images/zygote.jpg",  # Image of embryo
    "images/zygote2.jpg",  # Image of early fetus
    "images/embryo3.jpeg",  # Image of mid fetus
    "images/embryo.jpeg",
    "images/embryo1.jpg",
    "images/embryo2.jpeg",
    "images/foetus.jpg"
]

# Check if images exist; you need to have them in the same directory
for img in stages:
    if not os.path.exists(img):
        print(f"Image {img} not found. Please provide images for each stage.")
        exit()

# Animate the growth stages
for i, img_path in enumerate(stages):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)  # Create a new surface for each frame
    context = cairo.Context(surface)

    # Fill background with a soft gray color
    context.set_source_rgb(0.9, 0.9, 0.9)
    context.paint()

    # Draw the womb-like sphere
    draw_womb(context, WIDTH // 2, HEIGHT // 2, 200)

    # Load the current stage image
    embryo_image = Image.open(img_path)

    # Calculate the new size for the embryo image
    scale_factor = 1 + i * 0.2  # Adjust growth factor as needed
    new_size = (int(embryo_image.width * scale_factor), int(embryo_image.height * scale_factor))

    # Resize the image
    embryo_image = embryo_image.resize(new_size, Image.ANTIALIAS)

    # Save the resized image temporarily to use with Cairo
    temp_path = "temp_embryo.png"
    embryo_image.save(temp_path)

    # Load and overlay the resized embryo image
    embryo_surface = cairo.ImageSurface.create_from_png(temp_path)
    embryo_width, embryo_height = embryo_surface.get_width(), embryo_surface.get_height()

    # Calculate position to center the embryo image within the sphere
    x_position = (WIDTH // 2) - (embryo_width // 2)
    y_position = (HEIGHT // 2) - (embryo_height // 2)

    # Draw the embryo image on the womb sphere
    context.set_source_surface(embryo_surface, x_position, y_position)
    context.paint()

    # Save the final image with the embryo overlay
    output_file = f"womb_with_{os.path.basename(img_path).split('.')[0]}.png"
    surface.write_to_png(output_file)
    print(f"Womb-like sphere with {os.path.basename(img_path)} created!")

    # Clean up the temporary file
    os.remove(temp_path)

    # Add a delay for animation effect
    time.sleep(1)  # Adjust delay for timing of stages

print("Animation frames created!")

