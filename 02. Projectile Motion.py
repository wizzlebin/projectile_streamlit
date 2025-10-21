# -*- coding: utf-8 -*-
"""
Projectile Motion Animation with Ground, Max Height, and Range Labels
Animation stops when the ball lands.
Created on Mon Oct 20 18:46:54 2025
@author: pushk
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------
# Parameters
# -----------------------------
v = 50.0          # initial velocity (m/s)
theta_deg = 80.0  # launch angle (degrees)
g = 9.81          # acceleration due to gravity (m/s²)

# -----------------------------
# Conversions and setup
# -----------------------------
theta = np.radians(theta_deg)
t_flight = 2 * v * np.sin(theta) / g            # total flight time
t_vals = np.linspace(0, t_flight, 500)

# Motion equations
x_vals = v * np.cos(theta) * t_vals
y_vals = v * np.sin(theta) * t_vals - 0.5 * g * t_vals**2

# Physics parameters
h_max = (v**2 * np.sin(theta)**2) / (2 * g)
range_ = (v**2 * np.sin(2 * theta)) / g
t_hmax = v * np.sin(theta) / g
x_hmax = v * np.cos(theta) * t_hmax

# -----------------------------
# Figure setup
# -----------------------------
fig, ax = plt.subplots(figsize=(18, 10), facecolor='black')
ax.set_facecolor('black')

# Plot static trajectory
ax.plot(x_vals, y_vals, color='dodgerblue', label=f'{theta_deg}° Launch', linewidth=2)

# Ground line
ax.axhline(0, color='white', linestyle='--', linewidth=1.2, alpha=0.8)

# Mark max height
ax.plot(x_hmax, h_max, 'yo', markersize=8, label='Max Height')
ax.text(x_hmax, h_max + 2, f'Hmax = {h_max:.2f} m', color='yellow', fontsize=9, ha='center')

# Mark range
ax.axvline(range_, color='red', linestyle='--', linewidth=1)
ax.text(range_, -5, f'Range = {range_:.2f} m', color='red', fontsize=9, ha='center')

# Labels and style
ax.set_title('Projectile Motion of a Ball', color='white', fontsize=14, pad=10)
ax.set_xlabel('Horizontal Distance (m)', color='white')
ax.set_ylabel('Vertical Height (m)', color='white')
ax.tick_params(colors='white')
ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
ax.grid(color='gray', linestyle='--', alpha=0.4)
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(0, range_ * 1.1)
ax.set_ylim(0, h_max * 1.3)

# -----------------------------
# Trace and moving point setup
# -----------------------------
trace_line, = ax.plot([], [], color='lime', linewidth=2)
point, = ax.plot([], [], 'ro', markersize=8)
x_data, y_data = [], []

# -----------------------------
# Animation update function
# -----------------------------
def update(frame):
    # Map frame number to time (stops exactly at t_flight)
    t = frame * t_flight / total_frames
    x = v * np.cos(theta) * t
    y = v * np.sin(theta) * t - 0.5 * g * t**2

    # Stop if the projectile hits the ground
    if y < 0:
        ani.event_source.stop()
        return trace_line, point

    # Update trace and moving point
    x_data.append(x)
    y_data.append(y)
    trace_line.set_data(x_data, y_data)
    point.set_data([x], [y])

    return trace_line, point

# -----------------------------
# Run animation
# -----------------------------
total_frames = 1000
ani = FuncAnimation(fig, update, frames=total_frames, interval=10, blit=True)
plt.show()
