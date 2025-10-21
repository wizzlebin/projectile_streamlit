# -*- coding: utf-8 -*-
"""
Multiple Projectile Motion Animation
Each projectile has its own:
  - velocity, angle, starting height (platform)
  - unique color
  - correct flight time
  - animated velocity vector
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------------------
# CONSTANTS
# -----------------------------------------
g = 9.81  # gravity (m/s²)

# -----------------------------------------
# USER INPUT: [velocity (m/s), angle (°), starting height (m)]
# -----------------------------------------
projectiles = [
    [50, 80, 10],
    [40, 45, 20],
    [60, 60, 5]
]

n_proj = len(projectiles)

# -----------------------------------------
# COMPUTE PARAMETERS
# -----------------------------------------
velocities = [p[0] for p in projectiles]
angles_deg = [p[1] for p in projectiles]
heights = [p[2] for p in projectiles]
angles_rad = [np.radians(a) for a in angles_deg]


def flight_time(v, theta, h0):
    """Compute total flight time given velocity, angle, and initial height."""
    a = -0.5 * g
    b = v * np.sin(theta)
    c = h0
    disc = b**2 - 4 * a * c
    if disc < 0:
        return 0
    t1 = (-b + np.sqrt(disc)) / (2 * a)
    t2 = (-b - np.sqrt(disc)) / (2 * a)
    return max(t1, t2)


flight_times = [flight_time(v, th, h0) for v, th, h0 in zip(velocities, angles_rad, heights)]
t_max = max(flight_times)

# -----------------------------------------
# PRECOMPUTE TRAJECTORIES
# -----------------------------------------
projectile_data = []
for v, th, h0, t_f in zip(velocities, angles_rad, heights, flight_times):
    t_vals = np.linspace(0, t_f, 400)
    x = v * np.cos(th) * t_vals
    y = h0 + v * np.sin(th) * t_vals - 0.5 * g * t_vals**2
    y = np.maximum(y, 0)
    vx = v * np.cos(th)
    vy = v * np.sin(th) - g * t_vals
    projectile_data.append((x, y, vx, vy, t_vals))

# -----------------------------------------
# COLORS — ensure visually distinct colors
# -----------------------------------------
cmap = plt.cm.get_cmap('tab10', n_proj)
color_list = [cmap(i) for i in range(n_proj)]

# -----------------------------------------
# FIGURE SETUP
# -----------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), facecolor='black')
ax.set_facecolor('black')

# Plot static trajectories and platforms
for i in range(n_proj):
    x, y, _, _, _ = projectile_data[i]
    ax.plot(x, y, color=color_list[i], linewidth=1.5,
            label=f'v={velocities[i]} m/s, θ={angles_deg[i]}°, h₀={heights[i]} m')

    # Platform line at starting height
    ax.hlines(heights[i], xmin=-5, xmax=5, colors=color_list[i],
              linewidth=4, alpha=0.9)

# Ground line
ax.axhline(0, color='white', linestyle='--', linewidth=1.2, alpha=0.8)

# Style setup
ax.set_title('Multiple Projectile Motion with Velocity Vectors & Platforms',
             color='white', fontsize=14)
ax.set_xlabel('Horizontal Distance (m)', color='white')
ax.set_ylabel('Vertical Height (m)', color='white')
ax.tick_params(colors='white')
ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
ax.grid(color='gray', linestyle='--', alpha=0.4)

# Axis limits
x_max = max([np.max(x) for x, _, _, _, _ in projectile_data])
y_max = max([np.max(y) for _, y, _, _, _ in projectile_data])
ax.set_xlim(-10, x_max * 1.1)
ax.set_ylim(0, y_max * 1.3)

# -----------------------------------------
# ANIMATION ELEMENTS
# -----------------------------------------
traces, points, vectors = [], [], []
for i in range(n_proj):
    trace, = ax.plot([], [], color=color_list[i], linewidth=2)
    point, = ax.plot([], [], 'o', color=color_list[i], markersize=8)
    vector = ax.quiver([], [], [], [], angles='xy', scale_units='xy', scale=1,
                       color=color_list[i], width=0.005)
    traces.append(trace)
    points.append(point)
    vectors.append(vector)

total_frames = 1000

# -----------------------------------------
# UPDATE FUNCTION
# -----------------------------------------
def update(frame):
    for i in range(n_proj):
        x, y, vx, vy, t_vals = projectile_data[i]
        t_f = flight_times[i]

        # Current time scaled to overall animation duration
        t_i = (frame / total_frames) * t_max

        if t_i > t_f:
            # Projectile landed — freeze at end
            traces[i].set_data(x, y)
            points[i].set_data([], [])
            vectors[i].set_UVC(0, 0)
            continue

        # Find current index
        idx = np.searchsorted(t_vals, t_i)
        idx = min(idx, len(x) - 1)

        # Update trajectory
        traces[i].set_data(x[:idx], y[:idx])
        points[i].set_data([x[idx]], [y[idx]])

        # Velocity vector (scaled down for display)
        v_scale = 0.25
        vectors[i].set_offsets([x[idx], y[idx]])
        vectors[i].set_UVC(v_scale * vx, v_scale * vy[idx])

    return traces + points + vectors


# -----------------------------------------
# RUN ANIMATION
# -----------------------------------------
ani = FuncAnimation(fig, update, frames=total_frames, interval=10,
                    blit=True
                    , repeat=False)
plt.show()

ani.save('projectile_motion.mp4', writer='ffmpeg', fps=60)
print("Animation saved as projectile_motion.mp4")