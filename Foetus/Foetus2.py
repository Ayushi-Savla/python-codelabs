import matplotlib.pyplot as plt
import numpy as np

def draw_stage(stage):
    plt.figure(figsize=(4, 4))
    plt.axis('equal')
    plt.axis('off')

    if stage == 1:  # Single cell
        plt.plot(0, 0, 'o', markersize=15, color='orange')
    elif stage == 2:  # Cluster of cells
        angles = np.linspace(0, 2 * np.pi, 6)
        for angle in angles:
            plt.plot(np.cos(angle), np.sin(angle), 'o', markersize=10, color='orange')
    elif stage == 3:  # Growing form
        angles = np.linspace(0, 2 * np.pi, 12)
        for angle in angles:
            plt.plot(1.5 * np.cos(angle), 1.5 * np.sin(angle), 'o', markersize=8, color='orange')
    elif stage == 4:  # Simple fetal outline
        plt.plot(0, 0, 'o', markersize=20, color='orange')
        plt.plot(0.5, 0.5, 'o', markersize=10, color='orange')  # head
        plt.plot(-0.5, -0.5, 'o', markersize=8, color='orange') # body

    plt.show()

# Display each stage
for i in range(1, 5):
    draw_stage(i)

