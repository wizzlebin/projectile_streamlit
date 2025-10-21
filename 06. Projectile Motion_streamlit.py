# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 15:27:36 2025

@author: pushk
"""

# projectile_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

g = 9.81

st.set_page_config(page_title="Projectile Simulator", layout="centered")
st.title("🎯 Projectile Motion Simulator")

st.markdown("Use the sidebar to add projectiles and adjust parameters.")

# --- sidebar inputs ---
n_proj = st.sidebar.number_input("Number of projectiles", min_value=1, max_value=6, value=2, step=1)

projectiles = []
for i in range(int(n_proj)):
    st.sidebar.markdown(f"**Projectile {i+1}**")
    v = st.sidebar.slider(f"Velocity (m/s) - {i+1}", 5, 120, 50, key=f"v{i}")
    ang = st.sidebar.slider(f"Angle (°) - {i+1}", 0, 90, 45, key=f"a{i}")
    h0 = st.sidebar.slider(f"Start Height (m) - {i+1}", 0, 100, 0, key=f"h{i}")
    projectiles.append((v, ang, h0))

# --- plotting area ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_facecolor("white")

colors = plt.cm.get_cmap('tab10', int(n_proj))

x_max_guess = 1.0
y_max_guess = 1.0

for i, (v, ang_deg, h0) in enumerate(projectiles):
    ang = np.radians(ang_deg)

    # compute time of flight (positive root)
    # solve h0 + v*sin(ang)*t - 0.5*g*t^2 = 0
    b = v * np.sin(ang)
    disc = b**2 + 2*g*h0
    t_f = (b + np.sqrt(disc)) / g

    t = np.linspace(0, t_f, 300)
    x = v * np.cos(ang) * t
    y = h0 + v * np.sin(ang) * t - 0.5 * g * t**2
    y = np.maximum(y, 0)

    ax.plot(x, y, color=colors(i), lw=2, label=f"v={v}, θ={ang_deg}°, h={h0}")
    # mark landing and max height
    x_land = v * np.cos(ang) * t_f
    ax.scatter([x_land], [0], color=colors(i))
    # max height
    t_h = v * np.sin(ang) / g
    y_h = h0 + v * np.sin(ang) * t_h - 0.5 * g * t_h**2
    ax.scatter([v * np.cos(ang) * t_h], [y_h], color=colors(i), marker="^")
    x_max_guess = max(x_max_guess, x_land)
    y_max_guess = max(y_max_guess, np.max(y))

ax.axhline(0, color='k', linestyle='--', linewidth=0.7)
ax.set_xlim(0, x_max_guess * 1.15)
ax.set_ylim(0, y_max_guess * 1.15)
ax.set_xlabel("Horizontal distance (m)")
ax.set_ylabel("Height (m)")
ax.set_title("Projectile Trajectories")
ax.legend(loc='upper right', fontsize='small')
ax.grid(alpha=0.3)

st.pyplot(fig)

st.markdown("---")
st.caption("Implemented with Streamlit — modify parameters in the left sidebar.")
