# -*- coding: utf-8 -*-
"""
Dual Projectile Motion Animation
Each projectile starts from a different height.
Stops automatically when both land.
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
h0_1 = 10.0         # starting height of projectile 1 (m)
h0_2 = 20.0         # starting height of projectile 2 (m)
g = 9.81            # gravity (m/s²)

# -----------------------------
# Convert to radians
# -----------------------------
theta1 = np.radians(theta_deg_1)
theta2 = np.radians(theta_deg_2)

# -----------------------------
# Function to compute flight time
# -----------------------------
def flight_time(v, theta, h0):
    a = -0.5 * g
    b = v * np.sin(theta)
    c = h0
    disc = b**2 - 4 * a * c
    if disc < 0:
        return 0
    t1 = (-b + np.sqrt(disc)) / (2 * a)
    t2 = (-b - np.sqrt(disc)) / (2 * a)
    return max(t1, t2)

# -----------------------------
# Compute flight times
# -----------------------------
t_flight1 = flight_time(v, theta1, h0_1)
t_flight2 = flight_time(v, theta2, h0_2)
t_flight = max(t_flight1, t_flight2)

# -----------------------------
# Trajectories (for static path)
# -----------------------------
t_vals = np.linspace(0, t_flight, 600)
x1 = v * np.cos(theta1) * t_vals
y1 = h0_1 + v * np.sin(theta1) * t_vals - 0.5 * g * t_vals**2
x2 = v * np.cos(theta2) * t_vals
y2 = h0_2 + v * np.sin(theta2) * t_vals - 0.5 * g * t_vals**2
y1 = np.maximum(y1, 0)
y2 = np.maximum(y2, 0)

# -----------------------------
# Metrics
# -----------------------------
h1 = h0_1 + (v**2 * np.sin(theta1)**2) / (2 * g)
h2 = h0_2 + (v**2 * np.sin(theta2)**2) / (2 * g)
r1 = v * np.cos(theta1) * t_flight1
r2 = v * np.cos(theta2) * t_flight2

# -----------------------------
# Figure setup
# -----------------------------
fig, ax = plt.subplots(figsize=(9, 5), facecolor='black')
ax.set_facecolor('black')

# Plot static trajectories
ax.plot(x1, y1, color='dodgerblue', linewidth=2, label=f'{theta_deg_1}° from {h0_1}m')
ax.plot(x2, y2, color='orange', linewidth=2, label=f'{theta_deg_2}° from {h0_2}m')

# Ground and platforms
ax.axhline(0, color='white', linestyle='--', linewidth=1.2, alpha=0.8)
ax.hlines(h0_1, -10, 0, color='blue', linewidth=3)
ax.hlines(h0_2, -10, 0, color='orange', linewidth=3)
ax.text(-15, h0_1, f'Start 1 = {h0_1} m', color='cyan', fontsize=9, va='center')
ax.text(-15, h0_2, f'Start 2 = {h0_2} m', color='orange', fontsize=9, va='center')

# Range markers
ax.axvline(r1, color='blue', linestyle='--', linewidth=1)
ax.text(r1, -5, f'R₁={r1:.1f}m', color='cyan', fontsize=9, ha='center')

ax.axvline(r2, color='orange', linestyle='--', linewidth=1)
ax.text(r2, -8, f'R₂={r2:.1f}m', color='orange', fontsize=9, ha='center')

# Labels and style
ax.set_title('Dual Projectile Motion (Different Starting Heights)', color='white', fontsize=14, pad=10)
ax.set_xlabel('Horizontal Distance (m)', color='white')
ax.set_ylabel('Vertical Height (m)', color='white')
ax.tick_params(colors='white')
ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
ax.grid(color='gray', linestyle='--', alpha=0.4)
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-20, max(r1, r2) * 1.1)
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

    # Positions
    x_1 = v * np.cos(theta1) * t
    y_1 = h0_1 + v * np.sin(theta1) * t - 0.5 * g * t**2

    x_2 = v * np.cos(theta2) * t
    y_2 = h0_2 + v * np.sin(theta2) * t - 0.5 * g * t**2

    # Stop when both hit ground
    if y_1 < 0 and y_2 < 0:
        ani.event_source.stop()
        return trace1, trace2, point1, point2

    y_1 = max(y_1, 0)
    y_2 = max(y_2, 0)

    # Update traces and points
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
ani = FuncAnimation(fig, update, frames=total_frames, interval=10, blit=True, repeat = False)
plt.show()
