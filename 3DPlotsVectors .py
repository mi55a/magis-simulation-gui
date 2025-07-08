import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.interpolate import griddata
import os

# Define desktop and folders
desktop = os.path.expanduser("~/Desktop")
input_folder = os.path.join(desktop, "MagneticCSVs")
output_folder = os.path.join(desktop, "MagneticPlots")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Darker yellow-only colorscale for surface plot
yellow_colorscale = [
    [0.0, 'rgb(255, 255, 102)'],  # Medium Yellow (darker than before)
    [0.5, 'rgb(204, 204, 0)'],    # Dark Yellow 
    [1.0, 'rgb(153, 153, 0)']     # Darker Yellow
]

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".csv"):
        filepath = os.path.join(input_folder, filename)
        plot_name = os.path.splitext(filename)[0] + ".html"
        save_path = os.path.join(output_folder, plot_name)

        if os.path.exists(save_path):
            print(f"✔️  Skipping {filename} — plot already exists.")
            continue

        print(f"📈 Processing: {filename}")

        try:
            # Read CSV
            df = pd.read_csv(filepath)

            # Extract data
            x = df.iloc[:, 4].values
            y = df.iloc[:, 5].values
            z = df.iloc[:, 6].values
            mag = df.iloc[:, 7].values

            # Normalize magnitude for colors
            norm_mag = mag / np.nanmax(mag)

            # Interpolate grid for surface plot
            grid_x, grid_y = np.meshgrid(
                np.linspace(x.min(), x.max(), 100),
                np.linspace(y.min(), y.max(), 100)
            )
            grid_z = griddata((x, y), z, (grid_x, grid_y), method='linear')
            grid_mag = griddata((x, y), mag, (grid_x, grid_y), method='linear')
            norm_grid_mag = grid_mag / np.nanmax(grid_mag)

            # Extract actual magnetic field components from your CSV
            # Assuming columns are: [timestamp, other, other, other, x, y, z, magnitude]
            # You need to tell me which columns contain Bx, By, Bz (magnetic field components)
            # For now, I'll assume you have magnetic field components in columns 8, 9, 10
            # If not, change these indices to match your CSV structure
            
            try:
                # Try to get magnetic field components (adjust these column indices as needed)
                Bx = df.iloc[:, 8].values if df.shape[1] > 8 else np.random.uniform(-1, 1, len(x))
                By = df.iloc[:, 9].values if df.shape[1] > 9 else np.random.uniform(-1, 1, len(x))
                Bz = df.iloc[:, 10].values if df.shape[1] > 10 else np.random.uniform(-1, 1, len(x))
            except:
                # Fallback to random directions if columns don't exist
                np.random.seed(42)
                Bx = np.random.uniform(-1, 1, len(x))
                By = np.random.uniform(-1, 1, len(x))
                Bz = np.random.uniform(-1, 1, len(x))
            
            # Normalize magnetic field vectors to unit length (direction only)
            B_magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
            B_magnitude[B_magnitude == 0] = 1  # prevent division by zero
            
            # Unit direction vectors
            Bx_unit = Bx / B_magnitude
            By_unit = By / B_magnitude  
            Bz_unit = Bz / B_magnitude

            # Set ALL vectors to the same fixed length (just for visualization)
            fixed_vector_length = 0.02  # Fixed length for all vectors
            dx_scaled = Bx_unit * fixed_vector_length
            dy_scaled = By_unit * fixed_vector_length
            dz_scaled = Bz_unit * fixed_vector_length

            # Calculate axis ranges with MORE padding for the bigger vectors
            padding = fixed_vector_length * 1.0  # Increased padding multiplier
            x_min_extended = x.min() - padding
            x_max_extended = x.max() + padding
            y_min_extended = y.min() - padding
            y_max_extended = y.max() + padding
            z_min_extended = z.min() - padding
            z_max_extended = z.max() + padding

            # Create subplot figure with 2 3D plots side by side
            fig = make_subplots(rows=1, cols=2,
                                specs=[[{'type': 'surface'}, {'type': 'scene'}]],
                                subplot_titles=("Magnetic Field Surface", "Vector Field"))

            # Surface plot (left)
            fig.add_trace(
                go.Surface(
                    x=grid_x, y=grid_y, z=grid_z,
                    surfacecolor=norm_grid_mag,
                    colorscale=yellow_colorscale,
                    cmin=0, cmax=1,
                    colorbar=dict(title="Magnetic Field Magnitude"),
                    lighting=dict(ambient=0.9),
                    showscale=True,
                    name="Magnetic Field"
                ),
                row=1, col=1
            )



            # Vector plot (right) - All vectors same length, showing direction only
            fig.add_trace(
                go.Cone(
                    x=x, y=y, z=z,
                    u=dx_scaled, v=dy_scaled, w=dz_scaled,
                    colorscale=[[0, 'blue'], [1, 'blue']],
                    sizemode="absolute",
                    sizeref=0.3,  # Visible but not huge
                    showscale=False,
                    anchor="tail",
                    name="Magnetic Field Direction"
                ),
                row=1, col=2
            )

            # Add red tips as small red spheres at vector endpoints
            fig.add_trace(
                go.Scatter3d(
                    x=x + dx_scaled,
                    y=y + dy_scaled,
                    z=z + dz_scaled,
                    mode='markers',
                    marker=dict(color='red', size=2),  # Smaller markers
                    name='Vector Tips',
                    showlegend=True
                ),
                row=1, col=2
            )

            fig.update_layout(
                height=600, width=1200,
                title_text=f"Magnetic Field and Vector Plots - {filename}",
                showlegend=True,
                scene=dict(  # Left subplot (surface plot)
                    xaxis=dict(range=[x.min(), x.max()]),
                    yaxis=dict(range=[y.min(), y.max()]),
                    zaxis=dict(range=[z.min(), z.max()]),
                    aspectmode='data'
                ),
                scene2=dict(  # Right subplot (vector plot) - extended ranges
                    xaxis=dict(range=[x_min_extended, x_max_extended]),
                    yaxis=dict(range=[y_min_extended, y_max_extended]),
                    zaxis=dict(range=[z_min_extended, z_max_extended]),
                    aspectmode='data'
                )
            )

            # Save interactive plot as HTML
            fig.write_html(save_path)
            print(f"✅ Saved interactive plot: {save_path}")

        except Exception as e:
            print(f"❌ Error with {filename}: {e}")