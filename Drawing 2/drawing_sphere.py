import math
import cairo

WIDTH, HEIGHT = 1000, 1000
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(surface)

def draw_sphere(context, center_x, center_y, radius, texture_path):
    context.arc(center_x, center_y, radius, 0, 2 * math.pi)

    texture_surface = cairo.ImageSurface.create_from_png(texture_path)
    texture_pattern = cairo.SurfacePattern(texture_surface)

    img_width = texture_surface.get_width()
    img_height = texture_surface.get_height()

    texture_aspect_ratio = img_width / img_height
    sphere_aspect_ratio = 1

    if texture_aspect_ratio > sphere_aspect_ratio:
        scale_factor = radius * 2 / img_width
    else:
        scale_factor = radius * 2 / img_height

    context.save()
    context.translate(center_x - radius, center_y - radius)
    context.scale(scale_factor, scale_factor)
    context.set_source(texture_pattern)
    context.paint()
    context.restore()

context.set_source_rgb(0.2,0.2,0.2)
context.paint()
draw_sphere(context, WIDTH // 2, HEIGHT // 2, 500, 'earth-1617121_1280.png')

surface.write_to_png('drawing_sphere.png')

print('done')