import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --------------------------------------
# Streamlit setup
# --------------------------------------
st.set_page_config(page_title="Projectile Motion Simulator", layout="centered")

st.markdown(
    "<h1 style='color:#FFD700; text-shadow:1px 1px 3px black;'>🎯 Projectile Motion Simulator (Real-Time Plotly Animation)</h1>",
    unsafe_allow_html=True
)

g = 9.81  # gravity (m/s²)

# --------------------------------------
# Sidebar Controls
# --------------------------------------
st.sidebar.header("Projectile Settings")

n_proj = st.sidebar.number_input("Number of projectiles", min_value=1, max_value=5, value=2, step=1)

projectiles = []
for i in range(int(n_proj)):
    st.sidebar.markdown(f"**Projectile {i+1}**")
    v = st.sidebar.slider(f"Velocity (m/s) - {i+1}", 5, 120, 50, key=f"v{i}")
    ang = st.sidebar.slider(f"Angle (°) - {i+1}", 0, 90, 45, key=f"a{i}")
    h0 = st.sidebar.slider(f"Start Height (m) - {i+1}", 0, 100, 0, key=f"h{i}")
    projectiles.append((v, np.radians(ang), h0))

# --------------------------------------
# Helper Calculations
# --------------------------------------
def flight_time(v, theta, h0):
    """Compute total flight time until projectile hits ground."""
    return (v * np.sin(theta) + np.sqrt((v * np.sin(theta))**2 + 2 * g * h0)) / g

flight_times = [flight_time(v, th, h0) for v, th, h0 in projectiles]
t_max = max(flight_times)

colors = ["#FF4B4B", "#00BFFF", "#FFD700", "#ADFF2F", "#FF69B4"]

# --------------------------------------
# Build Plotly Figure
# --------------------------------------
fig = go.Figure()

# Static trajectories and starting points
for i, (v, th, h0) in enumerate(projectiles):
    t_vals = np.linspace(0, t_max, 200)
    x_vals = v * np.cos(th) * np.minimum(t_vals, flight_times[i])
    y_vals = h0 + v * np.sin(th) * np.minimum(t_vals, flight_times[i]) - 0.5 * g * np.minimum(t_vals, flight_times[i])**2
    y_vals = np.maximum(y_vals, 0)

    # Trajectory trace
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        line=dict(color=colors[i], width=3),
        name=f"Projectile {i+1}"
    ))

    # Marker for projectile
    fig.add_trace(go.Scatter(
        x=[x_vals[0]],
        y=[y_vals[0]],
        mode="markers",
        marker=dict(size=12, color=colors[i]),
        name=f"Marker {i+1}",
        showlegend=False
    ))

# --------------------------------------
# Create Animation Frames
# --------------------------------------
frames = []
n_frames = 60
for k in range(n_frames):
    frame_data = []
    for i, (v, th, h0) in enumerate(projectiles):
        t_frame = k / n_frames * t_max
        x_frame = v * np.cos(th) * min(t_frame, flight_times[i])
        y_frame = h0 + v * np.sin(th) * min(t_frame, flight_times[i]) - 0.5 * g * min(t_frame, flight_times[i])**2
        y_frame = max(y_frame, 0)

        # Move marker only, keep line as-is
        frame_data.append(go.Scatter(x=[x_frame], y=[y_frame], mode="markers",
                                     marker=dict(size=12, color=colors[i])))
    frames.append(go.Frame(data=frame_data, name=str(k)))

fig.frames = frames

# --------------------------------------
# Axis limits and layout
# --------------------------------------
x_max = max(v * np.cos(th) * ft for v, th, ft in zip([p[0] for p in projectiles],
                                                     [p[1] for p in projectiles],
                                                     flight_times))
y_max = max([h + v**2 * np.sin(th)**2 / (2*g) for v, th, h in projectiles])

fig.update_layout(
    xaxis=dict(title="Horizontal Distance (m)", range=[0, x_max*1.1], showgrid=True, gridcolor="gray"),
    yaxis=dict(title="Vertical Height (m)", range=[0, y_max*1.2], showgrid=True, gridcolor="gray"),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title={
        "text": "🎯 Projectile Motion (Real-Time Animation)",
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

# --------------------------------------
# Display in Streamlit
# --------------------------------------
st.plotly_chart(fig, use_container_width=True)

st.caption("✨ Adjust the sliders to instantly see updated projectile paths and animation.")
