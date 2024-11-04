import math
import cairo
import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np

WIDTH, HEIGHT = 600, 600
FRAMES = 60  # Number of frames for the animation

# Load a font for annotation
try:
    font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = ImageFont.load_default()

def cairo_surface_to_pil(surface):
    # Convert Cairo surface to PIL Image
    buf = surface.get_data()
    data = np.ndarray(shape=(HEIGHT, WIDTH, 4),
                      dtype=np.uint8,
                      buffer=buf)
    # Cairo uses ARGB, PIL uses RGBA, so we need to swap the channels
    data = np.roll(data, 1, axis=2)
    return Image.fromarray(data, 'RGBA')


def draw_sphere(context, center_x, center_y, radius, alpha=1.0):
    context.arc(center_x, center_y, radius, 0, 2 * math.pi)
    gradient = cairo.RadialGradient(
        center_x - radius * 0.5,
        center_y - radius * 0.5,
        radius * 0.2,
        center_x,
        center_y,
        radius
    )
    gradient.add_color_stop_rgba(0, 0.9, 0.9, 1, alpha)
    gradient.add_color_stop_rgba(0.7, 0.6, 0.6, 0.8, alpha)
    gradient.add_color_stop_rgba(1, 0.3, 0.3, 0.5, alpha)
    context.set_source(gradient)
    context.fill()


def draw_embryo(context, center_x, center_y, progress):
    scale = 0.1 + progress * 0.4
    red = 0.8 + progress * 0.2
    context.save()

    # Basic embryo shape
    context.translate(center_x, center_y)
    context.scale(scale * 400, scale * 400)

    # Early stage (circular cell)
    if progress < 0.2:
        context.arc(0, 0, 0.5, 0, 2 * math.pi)
    # Middle stages (embryo shape)
    else:
        context.move_to(0, -0.5)
        context.curve_to(0.5, -0.5, 0.5, 0.5, 0, 0.5)
        context.curve_to(-0.5, 0.5, -0.5, -0.5, 0, -0.5)

    # Gradient fill
    gradient = cairo.RadialGradient(0, 0, 0.1, 0, 0, 0.5)
    gradient.add_color_stop_rgb(0, red, 0.5, 0.5)
    gradient.add_color_stop_rgb(1, red * 0.7, 0.3, 0.3)
    context.set_source(gradient)
    context.fill()

    # Add developmental features based on progress
    if progress > 0.3:
        # Neural tube
        context.set_source_rgba(0.7, 0.2, 0.2, 0.6)
        context.move_to(0, -0.3)
        context.line_to(0, 0.3)
        context.set_line_width(0.1)
        context.stroke()

    if progress > 0.5:
        # Early limb buds
        context.set_source_rgba(0.6, 0.2, 0.2, 0.7)
        for x in [-0.3, 0.3]:
            context.arc(x, 0, 0.1, 0, 2 * math.pi)
            context.fill()

    if progress > 0.7:
        # Head formation
        context.set_source_rgba(0.5, 0.1, 0.1, 0.8)
        context.arc(0, -0.3, 0.15, 0, 2 * math.pi)
        context.fill()

        # Limb development
        for x, y in [(0.3, 0.1), (-0.3, 0.1), (0.2, 0.3), (-0.2, 0.3)]:
            context.move_to(x, y)
            context.line_to(x + 0.1, y + 0.1)
            context.set_line_width(0.05)
            context.stroke()

    context.restore()


def draw_environment(context, center_x, center_y, radius, progress):
    for i in range(20):
        angle = (i / 20 + progress) * 2 * math.pi
        r = radius * (0.8 + 0.2 * math.sin(progress * 5 + i))
        x = center_x + r * math.cos(angle)
        y = center_y + r * math.sin(angle)

        context.arc(x, y, 2 + math.sin(progress * 3 + i) * 2, 0, 2 * math.pi)
        context.set_source_rgba(0.6 + 0.4 * math.sin(progress + i),
                                0.7 + 0.3 * math.sin(progress * 2 + i),
                                1.0,
                                0.3)
        context.fill()


def add_text_annotation(image, frame_number, progress):
    draw = ImageDraw.Draw(image)
    text = f"Frame {frame_number + 1}/{FRAMES} | Progress: {progress:.2f}"
    draw.text((10, 10), text, font=font, fill=(255, 255, 255, 255))
    return image


def create_frame(frame_number, total_frames):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    context = cairo.Context(surface)

    # Clear background
    context.set_source_rgb(0.1, 0.1, 0.2)
    context.paint()

    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    radius = 200

    progress = frame_number / total_frames

    # Draw environment
    draw_environment(context, center_x, center_y, radius, progress)

    # Draw sphere
    draw_sphere(context, center_x, center_y, radius)

    # Draw embryo
    draw_embryo(context, center_x, center_y, progress)

    # Convert Cairo surface to PIL image
    pil_image = cairo_surface_to_pil(surface)

    # Add text annotation to the image
    annotated_image = add_text_annotation(pil_image, frame_number, progress)

    return annotated_image


def create_animated_gif():
    # List to store all frames
    frames = []

    # Generate frames
    print("Generating frames...")
    for frame in range(FRAMES):
        pil_image = create_frame(frame, FRAMES)
        frames.append(pil_image)
        print(f"Generated frame {frame + 1}/{FRAMES}")

    # Create the animated GIF
    print("Creating GIF...")
    frames[0].save(
        'embryo_development_steps.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=50,  # Duration for each frame in milliseconds
        loop=0  # 0 means loop forever
    )
    print("GIF created successfully!")


if __name__ == "__main__":
    create_animated_gif()
