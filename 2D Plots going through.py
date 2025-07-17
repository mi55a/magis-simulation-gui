import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.colors as mcolors

# --- CONFIG ---
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
data_folder = os.path.join(desktop_path, "MagneticCSVs")
output_folder = os.path.join(desktop_path, "2DPlots")
os.makedirs(output_folder, exist_ok=True)

# Get all CSV files in the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Create a persistent figure
fig, axes = plt.subplots(2, 2, figsize=(12, 7))
plt.ion()  # Interactive mode ON

for csv_filename in csv_files:
    base_name = os.path.splitext(csv_filename)[0]
    save_path = os.path.join(output_folder, f"{base_name}_2DPlot.png")

    # Skip if plot already exists
    if os.path.exists(save_path):
        print(f"Skipping {csv_filename}: plot already exists.")
        continue

    csv_path = os.path.join(data_folder, csv_filename)
    print(f"Processing: {csv_filename}")

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to read {csv_filename}: {e}")
        continue

    # Check required columns
    required_columns = ['timestamp', 'x', 'y', 'z', 'mag']
    if not all(col in df.columns for col in required_columns):
        print(f"Skipping {csv_filename}: missing required columns")
        continue

    # Clear and reset figure
    fig.clf()
    fig.suptitle(f"Data from file: {csv_filename}", fontsize=16, fontweight='bold')

    # Rebuild subplots with spacing
    axes = fig.subplots(2, 2).flatten()
    plt.subplots_adjust(hspace=0.4)  # More space between top and bottom

    colors = ['lightseagreen', 'deeppink', 'lightcoral', 'slateblue']
    labels = ['x', 'y', 'z', 'mag']
    timestamps = []
    data_stream = {label: [] for label in labels}
    lines = []

    for i, label in enumerate(labels):
        ax = axes[i]
        line, = ax.plot([], [], marker='o', linestyle='', color=colors[i], label=label)
        ax.set_xlabel("Timestamp")
        ax.set_ylabel(label)
        ax.set_title(f"{label} vs Timestamp")
        ax.grid(True)
        ax.legend()
        lines.append(line)

    # Animation loop
    for frame in range(len(df)):
        row = df.iloc[frame]
        timestamps.append(row['timestamp'])
        for label in labels:
            data_stream[label].append(row[label])
        for i, label in enumerate(labels):
            lines[i].set_data(timestamps, data_stream[label])
            axes[i].relim()
            axes[i].autoscale_view()
        plt.pause(0.2)  # Slower update speed

    # Save final plot
    fig.savefig(save_path)
    print(f"Saved: {save_path}")

# Done
plt.ioff()
print("All plots completed.")
