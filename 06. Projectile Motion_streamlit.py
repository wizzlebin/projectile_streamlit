# projectile_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

g = 9.81

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Projectile Simulator", layout="centered")
st.title("🎯 Projectile Motion Simulator (Animated)")

st.markdown("Use the sidebar to add projectiles and adjust parameters, then click **Start Animation** below.")

# --- Sidebar Inputs ---
n_proj = st.sidebar.number_input("Number of projectiles", min_value=1, max_value=6, value=2, step=1)

projectiles = []
for i in range(int(n_proj)):
    st.sidebar.markdown(f"**Projectile {i+1}**")
    v = st.sidebar.slider(f"Velocity (m/s) - {i+1}", 5, 120, 50, key=f"v{i}")
    ang = st.sidebar.slider(f"Angle (°) - {i+1}", 0, 90, 45, key=f"a{i}")
    h0 = st.sidebar.slider(f"Start Height (m) - {i+1}", 0, 100, 0, key=f"h{i}")
    projectiles.append((v, ang, h0))

# --- Compute max time and distances for scaling ---
t_flights = []
x_max = 0
y_max = 0

for (v, ang_deg, h0) in projectiles:
    ang = np.radians(ang_deg)
    b = v * np.sin(ang)
    disc = b**2 + 2*g*h0
    t_f = (b + np.sqrt(disc)) / g
    t_flights.append(t_f)
    x_land = v * np.cos(ang) * t_f
    x_max = max(x_max, x_land)
    y_peak = h0 + (v*np.sin(ang))**2 / (2*g)
    y_max = max(y_max, y_peak)

max_t = max(t_flights)
colors = plt.cm.get_cmap('tab10', int(n_proj))

# --- Create figure ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, x_max * 1.1)
ax.set_ylim(0, y_max * 1.2)
ax.set_xlabel("Horizontal distance (m)")
ax.set_ylabel("Height (m)")
ax.set_title("Animated Projectile Motion")
ax.grid(alpha=0.3)

# draw platforms for different start heights
for _, _, h0 in projectiles:
    ax.axhline(h0, color="gray", linestyle="--", lw=0.5)

points = []
for i in range(int(n_proj)):
    (ln,) = ax.plot([], [], "o", color=colors(i), label=f"Proj {i+1}")
    points.append(ln)
ax.legend()

# --- Animation control ---
animate_btn = st.button("▶️ Start Animation")

if animate_btn:
    placeholder = st.empty()
    n_frames = 120
    for frame in range(n_frames + 1):
        t = (frame / n_frames) * max_t

        # clear previous lines
        for i, (v, ang_deg, h0) in enumerate(projectiles):
            ang = np.radians(ang_deg)
            x = v * np.cos(ang) * t
            y = h0 + v * np.sin(ang) * t - 0.5 * g * t**2
            if y < 0:
                y = 0
            points[i].set_data(x, y)

        # redraw the figure
        placeholder.pyplot(fig)
        time.sleep(0.03)

st.markdown("---")
st.caption("Implemented with Streamlit — adjust parameters and click Start Animation.")
