import cairo

width, height = 800, 600
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
ctx = cairo.Context(surface)
ctx.set_source_rgb(1, 1, 1)  # White background
ctx.paint()

ctx.set_line_width(3) #for outlines

# Draw the left wall with outline
ctx.set_source_rgb(0.85, 0.7, 0.5)  # Darker beige for left wall
ctx.move_to(300, 250)  # Bottom left corner
ctx.line_to(400, 300)  # Top left corner
ctx.line_to(400, 550)  # Bottom right corner of the left wall
ctx.line_to(300, 500)  # Bottom left corner
ctx.close_path()
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Draw the front wall with outline
ctx.set_source_rgb(0.95, 0.8, 0.6)  # Light beige for front wall
ctx.move_to(400, 300)  # Top left corner of front wall
ctx.line_to(700, 300)  # Top right corner of front wall
ctx.line_to(700, 550)  # Bottom right corner
ctx.line_to(400, 550)  # Bottom left corner
ctx.close_path()
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Draw the roof (front-facing part) with outline, positioned above the front wall
ctx.set_source_rgb(0.9, 0.4, 0.2)  # Roof color
ctx.move_to(400, 300)  # Left edge of the roof
ctx.line_to(525, 150)  # Roof peak
ctx.line_to(725, 300)  # Right edge of the roof
ctx.close_path()
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Draw the roof (side part) with outline
ctx.set_source_rgb(0.8, 0.3, 0.2)  # Darker roof side color
ctx.move_to(525, 150)  # Roof peak
ctx.line_to(400, 300)  # Top left corner of the side roof
ctx.line_to(270, 250)  # Left edge of the side roof
ctx.close_path()
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Draw the dormer (small roof structure on top) with outline
ctx.set_source_rgb(0.9, 0.4, 0.2)  # Dormer roof color
ctx.move_to(500, 240)
ctx.line_to(540, 215)
ctx.line_to(580, 240)
ctx.close_path()
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Dormer wall with outline
ctx.set_source_rgb(0.95, 0.8, 0.6)  # Dormer wall color
ctx.rectangle(515, 240, 50, 40)
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Dormer window with outline
ctx.set_source_rgb(0.7, 0.9, 1)  # Light blue for window
ctx.rectangle(525, 250, 30, 20)
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Front windows with outline
ctx.set_source_rgb(0.7, 0.9, 1)  # Window color
ctx.rectangle(450, 370, 50, 70)
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()
ctx.rectangle(525, 370, 50, 70)
ctx.set_source_rgb(0.7, 0.9, 1)
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

ctx.set_source_rgb(0.25, 0.88, 0.82)
ctx.rectangle(450, 400, 50, 10)
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

ctx.set_source_rgb(0.25, 0.88, 0.82)
ctx.rectangle(525, 400, 50, 10)
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Front door with outline
ctx.set_source_rgb(0.6, 0.3, 0.2)  # Door color
ctx.rectangle(610, 420, 50, 130)
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

# Door knob
ctx.arc(645, 485, 5, 0, 2 * 3.1416)
ctx.set_source_rgb(0, 0, 0)  # Black for knob
ctx.fill()

#Left wall window
ctx.set_source_rgb(0.7, 0.9, 1)  # Light blue for window
ctx.move_to(315, 350)  # Top-left corner
ctx.line_to(375, 370)  # Top-right corner
ctx.line_to(375, 430)  # Bottom-right corner
ctx.line_to(315, 410)  # Bottom-left corner
ctx.close_path()
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)  # Black outline
ctx.stroke()

#Horizontal bar for left window
ctx.move_to(315, 380)  # Horizontal bar top point
ctx.line_to(375, 400)  # Horizontal bar bottom point
ctx.stroke()

# Save the result
surface.write_to_png("3D_house.png")
