# projectile_app_plotly_physics_fixed.py
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
    t_vals = np.linspace(0, tf, 200)
    x_vals = v * np.cos(ang) * t_vals
    y_vals = h0 + v * np.sin(ang) * t_vals - 0.5 * g * t_vals**2
    y_vals = np.maximum(y_vals, 0)
    trajectories.append((t_vals, x_vals, y_vals))
    flight_times.append(tf)
    max_x = max(max_x, x_vals[-1])
    max_y = max(max_y, np.max(y_vals))

    # Faint full trajectory
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        line=dict(color=colors[i % len(colors)], width=1, dash="dot"),
        name=f"Path {i+1}"
    ))

# -----------------------------
# Build animation frames (time-synced)
# -----------------------------
n_frames = 120
t_max = max(flight_times)
frames = []

for f_idx in range(n_frames):
    t = f_idx / (n_frames - 1) * t_max  # normalized time
    frame_data = []
    for i, (t_vals, x_vals, y_vals) in enumerate(trajectories):
        # find projectile position at this global time
        if t > t_vals[-1]:
            x = x_vals[-1]
            y = 0
        else:
            x = np.interp(t, t_vals, x_vals)
            y = np.interp(t, t_vals, y_vals)

        # Trace line up to this time
        mask = t_vals <= t
        frame_data.append(go.Scatter(
            x=x_vals[mask],
            y=y_vals[mask],
            mode="lines",
            line=dict(color=colors[i % len(colors)], width=3),
            showlegend=False
        ))

        # Moving marker
        frame_data.append(go.Scatter(
            x=[x],
            y=[y],
            mode="markers",
            marker=dict(size=10, color=colors[i % len(colors)], line=dict(color="white", width=1)),
            showlegend=False
        ))

    frames.append(go.Frame(data=frame_data, name=f"frame{f_idx}"))

fig.frames = frames

# -----------------------------
# Layout (dark mode + play/pause)
# -----------------------------
fig.update_layout(
    xaxis=dict(title="Horizontal Distance (m)", range=[0, max_x * 1.1], gridcolor="gray"),
    yaxis=dict(title="Vertical Height (m)", range=[0, max_y * 1.2], gridcolor="gray"),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title={
        "text": "🎯 Projectile Motion (Real-Time Physics Animation)",
        "font": {"color": "#FFD700", "size": 22},
        "x": 0.5,
        "xanchor": "center"
    },
    updatemenus=[{
        "type": "buttons",
        "direction": "left",
        "x": 0.1, "y": -0.15,
        "showactive": True,
        "bgcolor": "#333",
        "font": {"color": "white"},
        "buttons": [{
            "label": "▶️ Play / ⏸ Pause",
            "method": "animate",
            "args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}]
        }]
    }],
    showlegend=True,
    margin=dict(l=60, r=30, t=80, b=60)
)

# -----------------------------
# Show graph
# -----------------------------
st.plotly_chart(fig, use_container_width=True)
st.caption("✨ Each projectile now follows correct physics and lands exactly on the ground.")
