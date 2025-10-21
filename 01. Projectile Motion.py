# -*- coding: utf-8 -*-
"""
Dual Projectile Motion Animation
Shows two projectiles launched at different angles.
Each stops when it hits the ground.
Created on Mon Oct 20 18:46:54 2025
@author: pushk
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------
# Parameters
# -----------------------------
v = 50.0            # initial velocity (m/s)
theta_deg_1 = 80.0  # launch angle for projectile 1
theta_deg_2 = 45.0  # launch angle for projectile 2
g = 9.81            # acceleration due to gravity (m/s²)

# -----------------------------
# Convert angles to radians
# -----------------------------
theta1 = np.radians(theta_deg_1)
theta2 = np.radians(theta_deg_2)

# -----------------------------
# Flight times
# -----------------------------
t_flight1 = 2 * v * np.sin(theta1) / g
t_flight2 = 2 * v * np.sin(theta2) / g
t_flight = max(t_flight1, t_flight2)  # for animation sync

# -----------------------------
# Generate trajectory points
# -----------------------------
t_vals = np.linspace(0, t_flight, 500)
x1 = v * np.cos(theta1) * t_vals
y1 = v * np.sin(theta1) * t_vals - 0.5 * g * t_vals**2
x2 = v * np.cos(theta2) * t_vals
y2 = v * np.sin(theta2) * t_vals - 0.5 * g * t_vals**2
y1 = np.maximum(y1, 0)
y2 = np.maximum(y2, 0)

# -----------------------------
# Key motion stats
# -----------------------------
h1 = (v**2 * np.sin(theta1)**2) / (2 * g)
r1 = (v**2 * np.sin(2 * theta1)) / g
h2 = (v**2 * np.sin(theta2)**2) / (2 * g)
r2 = (v**2 * np.sin(2 * theta2)) / g

# -----------------------------
# Figure setup
# -----------------------------
fig, ax = plt.subplots(figsize=(9, 5), facecolor='black')
ax.set_facecolor('black')

# Plot static trajectories
ax.plot(x1, y1, color='dodgerblue', label=f'{theta_deg_1}° Launch')
ax.plot(x2, y2, color='orange', label=f'{theta_deg_2}° Launch')

# Ground line
ax.axhline(0, color='white', linestyle='--', linewidth=1.2, alpha=0.8)

# Mark range for each
ax.axvline(r1, color='blue', linestyle='--', linewidth=1)
ax.text(r1, -4, f'R₁={r1:.1f}m', color='cyan', fontsize=9, ha='center')

ax.axvline(r2, color='orange', linestyle='--', linewidth=1)
ax.text(r2, -7, f'R₂={r2:.1f}m', color='orange', fontsize=9, ha='center')

# Style
ax.set_title('Dual Projectile Motion Comparison', color='white', fontsize=14, pad=10)
ax.set_xlabel('Horizontal Distance (m)', color='white')
ax.set_ylabel('Vertical Height (m)', color='white')
ax.tick_params(colors='white')
ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
ax.grid(color='gray', linestyle='--', alpha=0.4)
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(0, max(r1, r2) * 1.1)
ax.set_ylim(0, max(h1, h2) * 1.3)

# -----------------------------
# Animation setup
# -----------------------------
trace1, = ax.plot([], [], color='cyan', linewidth=2)
trace2, = ax.plot([], [], color='yellow', linewidth=2)
point1, = ax.plot([], [], 'ro', markersize=8)
point2, = ax.plot([], [], 'go', markersize=8)
x1_data, y1_data, x2_data, y2_data = [], [], [], []

# -----------------------------
# Update function
# -----------------------------
def update(frame):
    t = frame * t_flight / total_frames

    # Projectile 1
    x_1 = v * np.cos(theta1) * t
    y_1 = v * np.sin(theta1) * t - 0.5 * g * t**2

    # Projectile 2
    x_2 = v * np.cos(theta2) * t
    y_2 = v * np.sin(theta2) * t - 0.5 * g * t**2

    # Stop animation when both hit ground
    if y_1 < 0 and y_2 < 0:
        ani.event_source.stop()
        return trace1, trace2, point1, point2

    # Clip ground
    y_1 = max(y_1, 0)
    y_2 = max(y_2, 0)

    # Update data
    x1_data.append(x_1)
    y1_data.append(y_1)
    trace1.set_data(x1_data, y1_data)
    point1.set_data([x_1], [y_1])

    x2_data.append(x_2)
    y2_data.append(y_2)
    trace2.set_data(x2_data, y2_data)
    point2.set_data([x_2], [y_2])

    return trace1, trace2, point1, point2

# -----------------------------
# Run animation
# -----------------------------
total_frames = 1000
ani = FuncAnimation(fig, update, frames=total_frames, interval=10, blit=True)
plt.show()

