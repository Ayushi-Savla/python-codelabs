import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Function to create a sphere
def sphere(radius, resolution):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

# Function to morph from sphere to a more complex shape
def morph_shape(t):
    # Spherical coordinates
    radius = 1
    complexity = 0.5 + 0.5 * t  # Controls how 'complex' the shape is
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * (1 + complexity * np.sin(3*v[:, np.newaxis])) * np.outer(np.cos(u), np.sin(v))
    y = radius * (1 + complexity * np.sin(3*v[:, np.newaxis])) * np.outer(np.sin(u), np.sin(v))
    z = radius * (1 + complexity * np.cos(3*v[:, np.newaxis])) * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

# Set up the figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1

# Animation function
def update(frame):
    ax.cla()  # Clear the axes
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    t = frame / 100  # Normalized time
    if t < 0.5:
        # Display the sphere (zygote)
        x, y, z = sphere(1, 30)
    else:
        # Display the complex shape (fetus)
        x, y, z = morph_shape(t - 0.5)
    ax.plot_surface(x, y, z, color='cyan', alpha=0.7)

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=50)
plt.show()
