import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# --- Configuration ---
# IMPORTANT: Replace 'YourUserName' with your actual Windows username or 'your_data_folder_name'
# with the exact name of the folder on your desktop containing your CSV files.
# Example for Windows: desktop_path = os.path.join("C:", "Users", "YourUserName", "Desktop")
# Example for macOS/Linux: desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Determine the desktop path based on the operating system
if sys.platform.startswith('win'):
    # For Windows
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
elif sys.platform.startswith('darwin'):
    # For macOS
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
else:
    # For Linux/Other Unix-like systems
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# --- USER INPUT REQUIRED ---
# 1. Enter the EXACT name of the folder on your desktop where your CSV files are located.
data_folder_name = "MagneticCSVs" # <--- REPLACED THIS with your folder name (e.g., "MySensorData")

# Full path to the folder containing your CSV data files
data_folder_path = os.path.join(desktop_path, data_folder_name)

# Name of the output folder for plots (will be created on the desktop)
output_folder_name = "2DPlots"
output_folder_path = os.path.join(desktop_path, output_folder_name)

# Define the columns to be plotted.
# 'timestamp' will always be the x-axis.
# The following list defines the y-axis columns for each subplot.
y_columns = ['x', 'y', 'z', 'mag']

# Define colors for each data series (corresponding to y_columns)
plot_colors = ['blue', 'green', 'red', 'purple'] # You can change these colors

# --- Script Logic ---

def create_plots_from_csv(file_path):
    """
    Reads a CSV file, generates a 4-subplot figure, and saves it.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Ensure required columns exist
        required_columns = ['timestamp'] + y_columns
        if not all(col in df.columns for col in required_columns):
            print(f"Skipping '{os.path.basename(file_path)}': Missing one or more required columns ({required_columns}).")
            return

        # Create a figure and a set of subplots (2 rows, 2 columns)
        # figsize (width, height) in inches. Adjust as needed.
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        # Flatten the axes array for easy iteration
        axes = axes.flatten()

        # Get the base filename without extension for the plot title
        base_filename = os.path.splitext(os.path.basename(file_path))[0]

        # Iterate through the y_columns and plot each one
        for i, col in enumerate(y_columns):
            ax = axes[i] # Get the current subplot axis
            color = plot_colors[i % len(plot_colors)] # Cycle through colors if more y_columns than colors

            ax.plot(df['timestamp'], df[col], marker='o', linestyle='', markersize=3, color=color, label=f'{col} Data')
            ax.set_xlabel("Timestamp")
            ax.set_ylabel(f"{col.capitalize()} Data") # Capitalize for label
            ax.set_title(f"{col.capitalize()} Data Plot - {base_filename}")
            ax.grid(True)
            ax.legend() # Show legend for the data series

        # Adjust layout to prevent titles/labels from overlapping
        plt.tight_layout()

        # Construct the output plot filename
        plot_filename = f"{base_filename}_2DPlots.png"
        output_plot_path = os.path.join(output_folder_path, plot_filename)

        # Check if the plot already exists to prevent duplicates
        if os.path.exists(output_plot_path):
            print(f"Plot '{plot_filename}' already exists. Skipping generation.")
        else:
            # Save the figure
            plt.savefig(output_plot_path)
            print(f"Generated plot for '{os.path.basename(file_path)}' saved to '{output_plot_path}'")

        # Close the figure to free up memory
        plt.close(fig)

    except pd.errors.EmptyDataError:
        print(f"Skipping '{os.path.basename(file_path)}': File is empty.")
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while processing '{os.path.basename(file_path)}': {e}")

def main():
    """
    Main function to orchestrate the plotting process.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"Created output folder: '{output_folder_path}'")
    else:
        print(f"Output folder already exists: '{output_folder_path}'")

    # Check if the data folder exists
    if not os.path.exists(data_folder_path):
        print(f"Error: Data folder '{data_folder_path}' not found.")
        print("Please ensure the folder name and desktop path are correct in the script.")
        return

    # Get a list of all CSV files in the data folder
    csv_files = [f for f in os.listdir(data_folder_path) if f.endswith('.csv')]

    if not csv_files:
        print(f"No CSV files found in '{data_folder_path}'.")
        return

    print(f"Found {len(csv_files)} CSV file(s) in '{data_folder_path}'.")

    # Process each CSV file
    for csv_file in csv_files:
        full_file_path = os.path.join(data_folder_path, csv_file)
        create_plots_from_csv(full_file_path)

    print("\nPlotting process complete.")

if __name__ == "__main__":
    main()