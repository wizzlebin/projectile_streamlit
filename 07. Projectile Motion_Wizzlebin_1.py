# projectile_app_plotly_traces_fixed.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -----------------------------
# Streamlit setup
# -----------------------------
st.set_page_config(page_title="Projectile Motion Simulator", layout="centered")
st.markdown(
    "<h1 style='color:#FFD700; text-shadow:1px 1px 3px black;'>🎯 Projectile Motion Simulator (Real-Time Plotly Animation)</h1>",
    unsafe_allow_html=True
)

g = 9.81

# -----------------------------
# Sidebar inputs
# -----------------------------
st.sidebar.header("Projectile Settings")
n_proj = st.sidebar.number_input("Number of projectiles", 1, 5, 2)

projectiles = []
for i in range(int(n_proj)):
    st.sidebar.markdown(f"**Projectile {i+1}**")
    v = st.sidebar.slider(f"Velocity (m/s) - {i+1}", 5, 120, 50, key=f"v{i}")
    ang = st.sidebar.slider(f"Angle (°) - {i+1}", 0, 90, 45, key=f"a{i}")
    h0 = st.sidebar.slider(f"Start Height (m) - {i+1}", 0, 100, 0, key=f"h{i}")
    projectiles.append((v, np.radians(ang), h0))

# -----------------------------
# Helper function
# -----------------------------
def flight_time(v, theta, h0):
    b = v * np.sin(theta)
    disc = b**2 + 2 * g * h0
    return (b + np.sqrt(disc)) / g

# -----------------------------
# Compute trajectories
# -----------------------------
colors = ["#FF4B4B", "#00FFB2", "#FFA600", "#33C3F0", "#FF66CC"]
fig = go.Figure()

max_x, max_y = 0, 0
trajectories = []
flight_times = []

for i, (v, ang, h0) in enumerate(projectiles):
    tf = flight_time(v, ang, h0)
    t_vals = np.linspace(0, tf, 120)
    x_vals = v * np.cos(ang) * t_vals
    y_vals = h0 + v * np.sin(ang) * t_vals - 0.5 * g * t_vals**2
    y_vals = np.maximum(y_vals, 0)
    trajectories.append((x_vals, y_vals))
    flight_times.append(tf)
    max_x = max(max_x, x_vals[-1])
    max_y = max(max_y, np.max(y_vals))

    # Faint full trajectory (background)
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
