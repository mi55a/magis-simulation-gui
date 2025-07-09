import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from scipy.interpolate import griddata

# Define desktop and folders
desktop = os.path.expanduser("~/Desktop")
input_folder = os.path.join(desktop, "MagneticCSVs")
output_folder = os.path.join(desktop, "MagneticPlots")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Darker yellow-only colorscale for surface plot (for Plotly)
yellow_colorscale = [
    [0.0, 'rgb(255, 255, 102)'],  # Medium Yellow
    [0.5, 'rgb(204, 204, 0)'],    # Dark Yellow
    [1.0, 'rgb(153, 153, 0)']     # Darker Yellow
]

# Constants for distance calculation (these are fixed based on professor's notes)
# Assuming these are in inches
LENG_FRONT = 25.5
LENG_PIPE = 240.25
LENG_BACK = 16.5
LENG_FULL = LENG_FRONT + LENG_PIPE + LENG_BACK

# --- Main Processing Loop ---
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".csv"):
        filepath = os.path.join(input_folder, filename)

        combined_plotly_save_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_combined.html")

        # Check if the combined plot already exists to avoid reprocessing
        if os.path.exists(combined_plotly_save_path):
            print(f"✔️  Skipping {filename} — combined Plotly plot already exists.")
            continue

        print(f"📈 Processing: {filename}")

        try:
            df = pd.read_csv(filepath)

            # Convert all column names to lowercase for easier and robust access
            df.columns = df.columns.str.lower()

            # --- Attempt to find a suitable timestamp column for distance calculation ---
            timestamp_candidate_cols = ['state_ts', 'marker_ts', 'timestamp']

            chosen_ts_col_name_in_df = None # This will store the lowercase column name used
            df['processed_timestamp'] = pd.NaT # Initialize a new column for processed timestamps

            for col_name in timestamp_candidate_cols:
                if col_name in df.columns: # Check if lowercase column exists
                    try:
                        # Convert to datetime, coercing errors to NaT (Not a Time)
                        temp_ts_series = pd.to_datetime(df[col_name], unit='ms', errors='coerce')

                        # Drop NaT values to only consider valid timestamps
                        temp_ts_series = temp_ts_series.dropna()

                        if len(temp_ts_series) < 2: # Need at least 2 unique time points to calculate variation
                            print(f"🔍 Column '{col_name}' has less than 2 valid timestamps after conversion. Trying next candidate.")
                            continue

                        min_ts_check = (temp_ts_series.astype(np.int64) // 10**6).min()
                        max_ts_check = (temp_ts_series.astype(np.int64) // 10**6).max()

                        if pd.notna(min_ts_check) and pd.notna(max_ts_check) and (max_ts_check != min_ts_check):
                            chosen_ts_col_name_in_df = col_name # Mark this column as the chosen one
                            df['processed_timestamp'] = pd.to_datetime(df[col_name], unit='ms', errors='coerce') # Store valid timestamps in the new column
                            print(f"✅ Using '{col_name}' column for distance calculation as it shows time variation.")
                            break # Found a suitable column, exit loop
                        else:
                            print(f"🔍 Column '{col_name}' has identical or invalid timestamps ({min_ts_check}, {max_ts_check}). Trying next candidate.")
                    except Exception as dt_e:
                        print(f"❌ Could not process '{col_name}' for timestamp: {dt_e}. Trying next candidate.")

            if chosen_ts_col_name_in_df is None:
                print(f"Skipping {filename}: No suitable timestamp column (state_ts, marker_ts, or timestamp) with varying values found for distance calculation.")
                continue

            # Explicitly convert required magnetic field columns to numeric, coercing errors to NaN
            required_cols_for_plot = ['x', 'y', 'z', 'mag']
            for col in required_cols_for_plot:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                else:
                    print(f"Warning: Column '{col}' not found in {filename}. Plotting may be affected.")

            # Filter out rows where essential plotting data or processed timestamp is NaN
            df_cleaned = df.dropna(subset=['x', 'y', 'z', 'mag', 'processed_timestamp']).copy() # Use .copy() to avoid SettingWithCopyWarning

            if df_cleaned.empty:
                print(f"Skipping {filename}: No valid data points remaining after cleaning essential columns for plotting.")
                continue

            # --- Calculate 'distance_along_pipe' based on processed_timestamp ---
            df_timestamps_ms = (df_cleaned['processed_timestamp'].astype(np.int64) // 10**6).values

            min_ts_ms = np.min(df_timestamps_ms)
            max_ts_ms = np.max(df_timestamps_ms)

            if pd.isna(min_ts_ms) or pd.isna(max_ts_ms) or (max_ts_ms == min_ts_ms):
                print(f"Skipping {filename}: Timestamp data for distance calculation is invalid after cleaning. This should not happen if previous checks were correct.")
                continue

            # Determine travel direction from filename (case-insensitive)
            filename_lower = filename.lower()
            file_direction = "UNKNOWN" # Default value

            if "away" in filename_lower:
                file_direction = "MOVING_AWAY"
            elif "home" in filename_lower:
                file_direction = "MOVING_HOME"
            else:
                print(f"Warning: Could not determine travel direction from filename '{filename}'. Assuming MOVING_AWAY. Please ensure 'away' or 'home' is clearly present in the filename.")
                file_direction = "MOVING_AWAY"

            # Define start and end distances for the linear interpolation based on direction
            if file_direction == "MOVING_AWAY":
                dist_at_min_ts = 0.0
                dist_at_max_ts = LENG_FULL
            elif file_direction == "MOVING_HOME":
                dist_at_min_ts = LENG_FULL
                dist_at_max_ts = 0.0

            # Calculate slope and intercept
            slope = (dist_at_max_ts - dist_at_min_ts) / (max_ts_ms - min_ts_ms)
            intr = dist_at_min_ts - slope * min_ts_ms

            # Calculate 'distance_along_pipe' for each timestamp
            df_cleaned['distance_along_pipe'] = df_timestamps_ms * slope + intr
            df_cleaned['distance_along_pipe'] = pd.to_numeric(df_cleaned['distance_along_pipe'], errors='coerce')


            # Extract magnetic field components and magnitude from the cleaned DataFrame.
            x_field = df_cleaned['x'].values
            y_field = df_cleaned['y'].values
            z_field = df_cleaned['z'].values
            mag_field = df_cleaned['mag'].values

            # The X-coordinate for positioning the vectors in the plot
            x_measurement_location = df_cleaned['distance_along_pipe'].values


            # Normalize magnitude for colors in the surface plot (0 to 1 range)
            if np.all(np.isnan(mag_field)) or len(mag_field) == 0 or np.nanmax(mag_field) == 0:
                norm_mag_field = np.zeros_like(mag_field, dtype=float)
            else:
                norm_mag_field = mag_field / np.nanmax(mag_field)


            # --- Prepare data for the Magnetic Field Component Surface Plot ---
            grid_x_field, grid_y_field, grid_z_field, norm_grid_mag_field = np.array([]), np.array([]), np.array([]), np.array([])
            surface_plot_available = False

            valid_griddata_indices_field = ~np.isnan(x_field) & ~np.isnan(y_field) & ~np.isnan(z_field) & ~np.isnan(mag_field)

            if np.sum(valid_griddata_indices_field) >= 4:
                x_interp_range_field = np.linspace(np.nanmin(x_field[valid_griddata_indices_field]), np.nanmax(x_field[valid_griddata_indices_field]), 100)
                y_interp_range_field = np.linspace(np.nanmin(y_field[valid_griddata_indices_field]), np.nanmax(y_field[valid_griddata_indices_field]), 100)
                grid_x_field, grid_y_field = np.meshgrid(x_interp_range_field, y_interp_range_field)

                grid_z_field = griddata((x_field[valid_griddata_indices_field], y_field[valid_griddata_indices_field]), z_field[valid_griddata_indices_field], (grid_x_field, grid_y_field), method='linear')
                grid_mag_field = griddata((x_field[valid_griddata_indices_field], y_field[valid_griddata_indices_field]), mag_field[valid_griddata_indices_field], (grid_x_field, grid_y_field), method='linear')

                if np.all(np.isnan(grid_mag_field)) or np.nanmax(grid_mag_field) == 0:
                    norm_grid_mag_field = np.zeros_like(grid_mag_field, dtype=float)
                else:
                    norm_grid_mag_field = grid_mag_field / np.nanmax(grid_mag_field)

                if not np.all(np.isnan(grid_z_field)):
                    surface_plot_available = True
            else:
                grid_z_field, norm_grid_mag_field = np.full((100,100), np.nan), np.full((100,100), np.nan)
                print(f"Not enough valid data points ({np.sum(valid_griddata_indices_field)}) for surface interpolation for {filename}. Skipping surface plot.")


            # --- Create Subplots Figure (Removed subplot_titles) ---
            fig_combined = make_subplots(
                rows=1, cols=2,
                specs=[[{'type': 'scene'}, {'type': 'scene'}]], # Both are 3D plots
                horizontal_spacing=0.01 # Minimal spacing, as scene domains will control placement
            )

            # --- Add Surface Plot to First Subplot ---
            if surface_plot_available:
                fig_combined.add_trace(
                    go.Surface(
                        x=grid_x_field, y=grid_y_field, z=grid_z_field,
                        surfacecolor=norm_grid_mag_field,
                        colorscale=yellow_colorscale,
                        cmin=0, cmax=1,
                        colorbar=dict(title="Magnetic Field Magnitude", x=0.45),
                        lighting=dict(ambient=0.9),
                        showscale=True,
                        name="Magnetic Field Components"
                    ),
                    row=1, col=1
                )
            else:
                fig_combined.add_annotation(
                    text="No valid data to plot field component surface",
                    xref="x domain", yref="y domain",
                    x=0.5, y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="red"),
                    row=1, col=1
                )
                print(f"Skipping Plotly surface plot for {filename}: Insufficient valid data for interpolation or plot is all NaN.")


            # --- Add Stem Plot to Second Subplot ---
            valid_indices_stem = ~np.isnan(x_measurement_location) & ~np.isnan(x_field) & ~np.isnan(y_field) & ~np.isnan(z_field)

            x_loc_valid_stem = x_measurement_location[valid_indices_stem]
            x_field_valid_stem = x_field[valid_indices_stem]
            y_field_valid_stem = y_field[valid_indices_stem]
            z_field_valid_stem = z_field[valid_indices_stem]
            stem_plot_available = len(x_loc_valid_stem) > 0


            if stem_plot_available:
                fig_combined.add_trace(go.Scatter3d(
                    x=x_loc_valid_stem,
                    y=np.zeros_like(x_loc_valid_stem),
                    z=np.zeros_like(x_loc_valid_stem),
                    mode='markers',
                    marker=dict(size=3, color='black', symbol='circle'),
                    name='Measurement Locations'
                ), row=1, col=2)

                stem_x_coords = []
                stem_y_coords = []
                stem_z_coords = []

                for i in range(len(x_loc_valid_stem)):
                    current_dist = x_loc_valid_stem[i]
                    stem_x_coords.extend([current_dist, current_dist + x_field_valid_stem[i], np.nan])
                    stem_y_coords.extend([0, y_field_valid_stem[i], np.nan])
                    stem_z_coords.extend([0, z_field_valid_stem[i], np.nan])

                fig_combined.add_trace(go.Scatter3d(
                    x=stem_x_coords,
                    y=stem_y_coords,
                    z=stem_z_coords,
                    mode='lines',
                    line=dict(color='blue', width=2),
                    name='Magnetic Field Vectors'
                ), row=1, col=2)

                fig_combined.add_trace(go.Scatter3d(
                    x=x_loc_valid_stem + x_field_valid_stem,
                    y=y_field_valid_stem,
                    z=z_field_valid_stem,
                    mode='markers',
                    marker=dict(size=5, color='red', symbol='diamond'),
                    name='Vector Heads'
                ), row=1, col=2)

            else:
                fig_combined.add_annotation(
                    text="No valid data to plot spatial field vectors",
                    xref="x domain", yref="y domain",
                    x=0.5, y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="red"),
                    row=1, col=2
                )
                print(f"Skipping Plotly stem plot for {filename}: No valid (non-NaN) data points to plot after filtering.")

            # --- Update Layout for Combined Figure (Corrected domain placement for scenes, added manual titles) ---
            fig_combined.update_layout(
                height=700,
                width=1600, # Increased overall figure width
                title=dict(
                    text=f"{os.path.splitext(filename)[0]}",
                    font=dict(
                        size=20,
                        color="black"
                    ),
                    x=0.5,
                    xanchor='center',
                    y=0.98,
                    yanchor='top',
                    pad=dict(t=20, b=10)
                ),
                showlegend=True,
                scene1=dict(
                    xaxis=dict(title="X Field Component", autorange=True),
                    yaxis=dict(title="Y Field Component", autorange=True),
                    zaxis=dict(title="Z Field Component", autorange=True),
                    aspectmode='data',
                    domain=dict(x=[0.02, 0.40], y=[0.0, 1.0]) # Left plot
                ),
                scene2=dict(
                    xaxis=dict(title="Distance Along Pipe (inches)", autorange=True),
                    yaxis=dict(title="Y Field Component (Offset from Pipe)", autorange=True),
                    zaxis=dict(title="Z Field Component (Offset from Pipe)", autorange=True),
                    aspectmode='data',
                    camera=dict(
                        eye=dict(x=1.75, y=1.75, z=1.75)
                    ),
                    domain=dict(x=[0.48, 0.78], y=[0.0, 1.0]) # Vector plot moved left, made narrower to create space
                )
            )

            # Manually add subplot titles as annotations
            fig_combined.add_annotation(
                text="3D Magnetic Field",
                xref="paper", yref="paper",
                x=0.21, # (0.02 + 0.40) / 2
                y=0.9,
                showarrow=False,
                font=dict(size=16, color="black")
            )

            fig_combined.add_annotation(
                text="Magnetic Vector Field",
                xref="paper", yref="paper",
                x=0.63, # (0.48 + 0.78) / 2
                y=0.9,
                showarrow=False,
                font=dict(size=16, color="black")
            )

            # --- Add Interactive Help Box to the RIGHT of the vector plot ---
            fig_combined.add_annotation(
                text="<b>Interactive Plot Controls:</b><br>"
                     "- &nbsp;Rotate: Left-click & Drag<br>"
                     "- &nbsp;Pan (move): Right-click & Drag<br>"
                     "&nbsp; &nbsp; &nbsp; (or Shift + Left-click & Drag)<br>"
                     "- &nbsp;Zoom: Scroll Wheel<br>"
                     "- &nbsp;Reset View: Double-click",
                xref="paper",
                yref="paper",
                x=0.80,          # Start annotation just after scene2 ends (0.78), a small gap
                y=0.5,           # Center vertically
                showarrow=False,
                font=dict(
                    size=12, # Slightly smaller font for better fit in tighter space
                    color="black"
                ),
                align="left",    # Align text within the annotation box
                bordercolor="gray",
                borderwidth=1,
                borderpad=10,    # Padding around the text within the border
                bgcolor="lightgray",
                opacity=0.8,
                xanchor='left' # IMPORTANT: Anchor the left side of the box to the x-coordinate
            )

            # Save the combined plot to an HTML file
            fig_combined.write_html(combined_plotly_save_path)
            print(f"✅ Saved combined Plotly plot: {combined_plotly_save_path}")

        except Exception as e:
            print(f"❌ Error with {filename}: {e}")