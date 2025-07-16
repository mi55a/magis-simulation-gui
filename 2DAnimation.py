import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os

# --- CONFIG ---
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
data_folder = os.path.join(desktop_path, "MagneticCSVs")
csv_filename = "TD-20250625-14-19-14-1484222-MOVING_AWAY-continuous.csv"
csv_path = os.path.join(data_folder, csv_filename)

# Read the entire CSV once
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"File not found: {csv_path}")
    exit()

# Check required columns exist
required_columns = ['timestamp', 'x', 'y', 'z', 'mag']
if not all(col in df.columns for col in required_columns):
    print(f"CSV is missing one or more required columns: {required_columns}")
    exit()

# --- Setup plot ---
fig, axes = plt.subplots(2, 2, figsize=(12, 7))
fig.suptitle(f"Data from file: {csv_filename}", fontsize=16, fontweight='bold')
axes = axes.flatten()
colors = ['blue', 'green', 'red', 'purple']
labels = ['x', 'y', 'z', 'mag']

timestamps = []
data_stream = {label: [] for label in labels}
lines = []

for i, label in enumerate(labels):
    ax = axes[i]
    line, = ax.plot([], [], marker='o', linestyle='', color=colors[i], label=label)  # No lines, just points
    ax.set_xlabel("Timestamp")
    ax.set_ylabel(label)
    ax.set_title(f"{label} vs Timestamp")
    ax.grid(True)
    ax.legend()
    lines.append(line)

# Function to save final plot
def save_final_plot():
    output_folder = os.path.join(desktop_path, "2DPlots")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    save_path = os.path.join(output_folder, "Final_2DPlot.png")
    fig.savefig(save_path)
    print(f"Final plot saved to: {save_path}")

# Animation update function
def update(frame):
    if frame >= len(df):
        save_final_plot()  # Save plot once animation ends
        return lines

    row = df.iloc[frame]
    timestamps.append(row['timestamp'])
    for label in labels:
        data_stream[label].append(row[label])

    for i, label in enumerate(labels):
        lines[i].set_data(timestamps, data_stream[label])
        axes[i].relim()
        axes[i].autoscale_view()

    return lines

# Run animation: 200ms between frames (adjust as needed)
ani = animation.FuncAnimation(fig, update, frames=len(df), interval=200, blit=False, repeat=False)

plt.tight_layout()
plt.show()
