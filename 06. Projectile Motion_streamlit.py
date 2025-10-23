# projectile_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import io

st.set_page_config(page_title="Projectile Motion Simulator", layout="centered")
st.title("🎯 Projectile Motion Simulator")
st.markdown("Use sliders in the sidebar to adjust projectile parameters, then click **Generate Animation**.")

g = 9.81

# -----------------------------
# Sidebar user input
# -----------------------------
n_proj = st.sidebar.number_input("Number of projectiles", min_value=1, max_value=5, value=2, step=1)

projectiles = []
for i in range(int(n_proj)):
    st.sidebar.markdown(f"**Projectile {i+1}**")
    v = st.sidebar.slider(f"Velocity (m/s) - {i+1}", 5, 120, 50, key=f"v{i}")
    ang = st.sidebar.slider(f"Angle (°) - {i+1}", 0, 90, 45, key=f"a{i}")
    h0 = st.sidebar.slider(f"Start Height (m) - {i+1}", 0, 100, 0, key=f"h{i}")
    projectiles.append((v, ang, h0))

animate = st.sidebar.button("🎬 Generate Animation")

# -----------------------------
# Helper functions
# -----------------------------
def flight_time(v, theta, h0):
    b = v * np.sin(theta)
    disc = b**2 + 2 * g * h0
    return (b + np.sqrt(disc)) / g

# -----------------------------
# Prepare figure
# -----------------------------
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_facecolor("black")
ax.axhline(0, color='white', linestyle='--', linewidth=1)

colors = plt.cm.get_cmap('tab10', int(n_proj))

velocities = [p[0] for p in projectiles]
angles = [np.radians(p[1]) for p in projectiles]
heights = [p[2] for p in projectiles]
flight_times = [flight_time(v, th, h0) for v, th, h0 in zip(velocities, angles, heights)]

# Determine max range & height
x_max = max([v * np.cos(th) * ft for v, th, ft in zip(velocities, angles, flight_times)])
y_max = max([h + v**2 * np.sin(th)**2 / (2 * g) for v, th, h in zip(velocities, angles, heights)])

ax.set_xlim(0, x_max * 1.1)
ax.set_ylim(0, y_max * 1.2)
ax.set_xlabel("Horizontal Distance (m)", color='white')
ax.set_ylabel("Vertical Height (m)", color='white')
ax.set_title("Projectile Motion Animation", color='white')
ax.tick_params(colors='white')
ax.grid(alpha=0.3, color='gray')

# Ground platforms
for i, (_, _, h0) in enumerate(projectiles):
    ax.hlines(h0, -5, 5, color=colors(i), linewidth=3)

# Animation elements
traces, points = [], []
for i in range(n_proj):
    trace, = ax.plot([], [], color=colors(i), lw=2)
    point, = ax.plot([], [], 'o', color=colors(i), markersize=8)
    traces.append(trace)
    points.append(point)

x_data = [[] for _ in range(n_proj)]
y_data = [[] for _ in range(n_proj)]

t_max = max(flight_times)
total_frames = 200

def update(frame):
    t = frame * t_max / total_frames
    for i in range(n_proj):
        v, th, h0 = velocities[i], angles[i], heights[i]
        tf = flight_times[i]

        if t > tf:
            continue  # stop updating after landing

        x = v * np.cos(th) * t
        y = h0 + v * np.sin(th) * t - 0.5 * g * t**2
        y = max(y, 0)

        x_data[i].append(x)
        y_data[i].append(y)

        traces[i].set_data(x_data[i], y_data[i])
        points[i].set_data([x], [y])

    return traces + points

# -----------------------------
# Generate Animation
# -----------------------------
if animate:
    ani = FuncAnimation(fig, update, frames=total_frames, interval=30, blit=True, repeat=False)

    buf = io.BytesIO()
    try:
        ani.save(buf, writer=PillowWriter(fps=20))
        buf.seek(0)
        st.image(buf, caption="Projectile Motion Animation", use_container_width=True)
    except Exception as e:
        st.error(f"⚠️ Animation rendering failed: {e}")
        st.pyplot(fig)
else:
    st.pyplot(fig)

st.caption("✨ Adjust parameters and click **Generate Animation** to see the motion.")
