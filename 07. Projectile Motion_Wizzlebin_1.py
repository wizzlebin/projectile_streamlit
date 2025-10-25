# projectile_app_plotly.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Projectile Motion Simulator", layout="centered")
st.title("🎯 Projectile Motion Simulator (Real-Time Plotly Animation)")
st.markdown(
    "<h1 style='color:#000000;'>🎯 Projectile Motion Simulator (Real-Time Plotly Animation)</h1>",
    unsafe_allow_html=True
)


g = 9.81

# -----------------------------
# Sidebar inputs (auto-refresh)
# -----------------------------
n_proj = st.sidebar.number_input("Number of projectiles", 1, 5, 2)

projectiles = []
for i in range(int(n_proj)):
    st.sidebar.markdown(f"**Projectile {i+1}**")
    v = st.sidebar.slider(f"Velocity (m/s) - {i+1}", 5, 120, 50, key=f"v{i}")
    ang = st.sidebar.slider(f"Angle (°) - {i+1}", 0, 90, 45, key=f"a{i}")
    h0 = st.sidebar.slider(f"Start Height (m) - {i+1}", 0, 100, 0, key=f"h{i}")
    projectiles.append((v, ang, h0))


# -----------------------------
# Helper function
# -----------------------------
def flight_time(v, theta, h0):
    b = v * np.sin(theta)
    disc = b**2 + 2 * g * h0
    return (b + np.sqrt(disc)) / g


# -----------------------------
# Build animation dynamically
# -----------------------------
colors = ["#FF4B4B", "#00FFB2", "#FFA600", "#33C3F0", "#FF66CC"]
fig = go.Figure()
max_x, max_y = 0, 0
trajectories = []
frames = []

# Precompute trajectories
for i, (v, ang_deg, h0) in enumerate(projectiles):
    th = np.radians(ang_deg)
    tf = flight_time(v, th, h0)
    t_vals = np.linspace(0, tf, 100)
    x_vals = v * np.cos(th) * t_vals
    y_vals = h0 + v * np.sin(th) * t_vals - 0.5 * g * t_vals**2
    y_vals = np.maximum(y_vals, 0)
    trajectories.append((x_vals, y_vals))
    max_x = max(max_x, x_vals[-1])
    max_y = max(max_y, np.max(y_vals))

    # Static trajectory path
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        line=dict(color=colors[i % len(colors)], width=2),
        name=f"Projectile {i+1} ({ang_deg}°)"
    ))

# -----------------------------
# Animation frames (trace + marker)
# -----------------------------
num_frames = 100
for f_idx in range(num_frames):
    frame_data = []
    for i, (x_vals, y_vals) in enumerate(trajectories):
        if f_idx < len(x_vals):
            # Draw trace up to current point
            frame_data.append(go.Scatter(
                x=x_vals[:f_idx+1],
                y=y_vals[:f_idx+1],
                mode="lines",
                line=dict(color=colors[i % len(colors)], width=2),
                showlegend=False
            ))
            # Moving marker
            frame_data.append(go.Scatter(
                x=[x_vals[f_idx]],
                y=[y_vals[f_idx]],
                mode="markers",
                marker=dict(color=colors[i % len(colors)], size=10),
                showlegend=False
            ))
    frames.append(go.Frame(data=frame_data, name=str(f_idx)))

fig.frames = frames

# -----------------------------
# Layout & improved toggle button
# -----------------------------
fig.update_layout(
    xaxis=dict(title="Horizontal Distance (m)", range=[0, max_x * 1.1], fixedrange=True),
    yaxis=dict(title="Vertical Height (m)", range=[0, max_y * 1.2], fixedrange=True),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title="Projectile Motion (Real-Time Animation)",
    updatemenus=[{
        "type": "buttons",
        "direction": "left",
        "x": 0.1, "y": -0.15,
        "showactive": True,
        "bgcolor": "#222",  # <-- apply here (not inside button)
        "font": {"color": "black", "size": 14},
        "buttons": [{
            "label": "▶️ Play / ⏸ Pause",
            "method": "animate",
            "args": [
                None,
                {
                    "fromcurrent": True,
                    "mode": "immediate",
                    "frame": {"duration": 50, "redraw": True},
                    "transition": {"duration": 0}
                }
            ]
        }]
    }]
)

# -----------------------------
# Initial markers (start points)
# -----------------------------
fig.add_trace(go.Scatter(
    x=[p[0][0] for p in trajectories],
    y=[p[1][0] for p in trajectories],
    mode="markers",
    marker=dict(size=10, color=colors[:len(trajectories)]),
    name="Start Points"
))

# -----------------------------
# Display plot
# -----------------------------
st.plotly_chart(fig, use_container_width=True)
st.caption("✨ Real-time browser animation with persistent traces and dark-themed controls.")
