# projectile_app_plotly.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Projectile Motion Simulator", layout="centered")
st.title("🎯 Projectile Motion Simulator (Real-Time Plotly Animation)")
st.markdown("Use sliders in the sidebar to adjust projectile parameters, then click **Play** to animate in real time!")

g = 9.81

# -----------------------------
# Sidebar inputs
# -----------------------------
n_proj = st.sidebar.number_input("Number of projectiles", 1, 5, 2)

projectiles = []
for i in range(int(n_proj)):
    st.sidebar.markdown(f"**Projectile {i+1}**")
    v = st.sidebar.slider(f"Velocity (m/s) - {i+1}", 5, 120, 50, key=f"v{i}")
    ang = st.sidebar.slider(f"Angle (°) - {i+1}", 0, 90, 45, key=f"a{i}")
    h0 = st.sidebar.slider(f"Start Height (m) - {i+1}", 0, 100, 0, key=f"h{i}")
    projectiles.append((v, ang, h0))

animate = st.sidebar.button("🎬 Show Animation")

# -----------------------------
# Physics functions
# -----------------------------
def flight_time(v, theta, h0):
    b = v * np.sin(theta)
    disc = b**2 + 2 * g * h0
    return (b + np.sqrt(disc)) / g

# -----------------------------
# Generate figure
# -----------------------------
if animate:
    fig = go.Figure()
    colors = ["red", "lime", "orange", "cyan", "magenta"]

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

        # Static trace (path)
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode="lines", line=dict(color=colors[i % len(colors)], width=2),
            name=f"Projectile {i+1} ({ang_deg}°)"
        ))

    # Animation frames (moving markers)
    num_frames = 100
    for frame_idx in range(num_frames):
        frame_data = []
        for i, (x_vals, y_vals) in enumerate(trajectories):
            if frame_idx < len(x_vals):
                frame_data.append(
                    go.Scatter(
                        x=[x_vals[frame_idx]],
                        y=[y_vals[frame_idx]],
                        mode="markers",
                        marker=dict(color=colors[i % len(colors)], size=10),
                        name=f"Projectile {i+1}"
                    )
                )
        frames.append(go.Frame(data=frame_data, name=str(frame_idx)))

    # Layout & buttons
    fig.frames = frames
    fig.update_layout(
        xaxis=dict(title="Horizontal Distance (m)", range=[0, max_x * 1.1]),
        yaxis=dict(title="Vertical Height (m)", range=[0, max_y * 1.2]),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        title="Projectile Motion Animation (Real-Time)",
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [
                {"label": "▶️ Play", "method": "animate",
                 "args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}]},
                {"label": "⏸ Pause", "method": "animate",
                 "args": [[None], {"mode": "immediate", "frame": {"duration": 0, "redraw": False}}]}
            ]
        }]
    )

    # Initial frame (all start points)
    fig.add_trace(go.Scatter(
        x=[p[0][0] for p in trajectories],
        y=[p[1][0] for p in trajectories],
        mode="markers",
        marker=dict(size=10, color=colors[:len(trajectories)])
    ))

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Adjust projectile parameters in the sidebar and click **Show Animation** to start.")

st.caption("✨ Uses Plotly for real-time browser-side animation (no GIFs, instant playback).")
