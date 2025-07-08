import tkinter as tk
from tkinter import ttk
# from trolley_data_sub2 import UserData
# from trolley_data_sub2 import on_connect, on_message
# import get_args as ga
from PIL import Image, ImageTk


# A place for me to play around with design 


'''
Top frame - center
Middle grid - command buttons, data table, window toggle buttons
Bottom rows - states (left), modes (right)

'''

states = []

modes =[]

table_row_id = None



gui_App = tk.Tk()
gui_App.title("Data Simulation GUI")
# gui_App.geometry("1000x1000")
gui_App.attributes('-zoomed', True)


gui_App.grid_columnconfigure(0, weight=1)
gui_App.grid_columnconfigure(1, weight=2)
gui_App.grid_columnconfigure(2, weight=1)

# gui_App.grid_rowconfigure(0, weight=1)
# gui_App.grid_rowconfigure(1, weight=1)
# gui_App.grid_rowconfigure(2, weight=1)


# Logo in GUI, will be added to repo 



log_window = tk.Toplevel()
log_window.title("Log of state changes")
log_window.geometry("550x100")

log_change_label = ttk.Label(log_window, text=f"Log change arrived: ")
log_change_label.pack()

plot_window = tk.Toplevel()
plot_window.title("Data Plot")
plot_window.geometry("550x600")

plot_label = ttk.Label(plot_window, text=f"Magnetometer Plot")
plot_label.pack()


gui_App.withdraw()
log_window.withdraw()
plot_window.withdraw()

instructions_window = tk.Toplevel()
instructions_window.title("Before You Begin")
instructions_window.geometry("500x500")

instructions = (
    "Make sure to fill out and post the Magnetometer Logs"
)

instructions_label = tk.Label(instructions_window, text=instructions, justify="left", wraplength=350)
instructions_label.pack(padx=20, pady=20)

def continue_main():
    instructions_window.destroy()
    gui_App.deiconify()

continue_button = tk.Button(instructions_window, text="Continue", command=continue_main)
continue_button.pack(pady=10)

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview", font=("Arial", 16), rowheight=5)
style.configure("Treeview.Heading", font=("Arial", 20, "bold"))

style.configure("State.RED.TButton", font=('Arial', 16, 'bold'),foreground='white', background="red")
style.map("State.RED.TButton", background=[("active", "#f52020")])

style.configure("State.GREEN.TButton", font=('Arial', 16, 'bold'),foreground='white', background="green")
style.map("State.RED.TButton", background=[("active", "#009900")])

style.configure("Cmd.START.TButton", font=('Arial', 20, 'bold'),foreground='black', background="#00A36C")
style.map("State.RED.TButton", background=[("active", "#00A36C")])

style.configure("Cmd.RESET.TButton", font=('Arial', 20, 'bold'),foreground='black', background="#FFDB58")
style.map("State.RED.TButton", background=[("active", "#FFDB58")])

style.configure("Cmd.STOP.TButton", font=('Arial', 20, 'bold'),foreground='black', background="red")
style.map("State.RED.TButton", background=[("active", "#F73942")])

style.configure("Logs.TButton", font=('Arial', 20, 'bold'),foreground='black', background="#6495ED")
style.map("State.RED.TButton", background=[("active", "#6495ED")])

style.configure("Plot.TButton", font=('Arial', 20, 'bold'),foreground='black', background="#FF69B4")
style.map("State.RED.TButton", background=[("active", "#FF69B4")])

# Main frame - logo, title, and time 

header_frame = tk.Frame(gui_App)
# header_frame.grid(row=0, column=0)
header_frame.grid(row=0, column=0, columnspan=3)


# header_frame.pack(pady=10)
header_label = tk.Label(header_frame, text="Maggy", font=("Arial", 20))
header_label.pack(pady=10)

magis_logo = Image.open('magis_logo_2.png')
# magis_logo = magis_logo.resize((200,200), Image.Resampling.LANCZOS)

tk_image = ImageTk.PhotoImage(magis_logo)

magis_label = tk.Label(header_frame, image=tk_image)

magis_label.pack(pady=5)

# command buttons (left)

command_frame = tk.Frame(gui_App)
command_frame.grid(row=1, column=0, padx=20, pady=30, sticky='n')
start_button = ttk.Button(command_frame, text="Start", style="Cmd.START.TButton")
start_button.pack(pady=30)
reset_button = ttk.Button(command_frame, text="Reset", style="Cmd.RESET.TButton")
reset_button.pack(pady=30)
stop_button = ttk.Button(command_frame, text="Stop", style="Cmd.STOP.TButton")
stop_button.pack(pady=30)

# Data table frame

table_frame = tk.Frame(gui_App)
# table_frame.grid(row=1, column=1, padx=50, pady=40)
# table_frame.pack(pady=50)
table_frame.grid(row=1, column=1, sticky='n')


# Window toggle buttons (right)

window_frame = tk.Frame(gui_App)
window_frame.grid(row=1, column=2, padx=10, pady=10)

log_changes_button = ttk.Button(window_frame, text="Show State Changes", style="Logs.TButton")
log_changes_button.pack(pady=30)

data_plot_button = ttk.Button(window_frame, text="WIP: Show Plot", style="Plot.TButton")
data_plot_button.pack(pady=30)

# states frame (bottom left)

state_frame = tk.Frame(gui_App)
state_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')


time_created = tk.Label(header_frame, text="Time created: ", font=("Arial", 20))
time_created.pack()

# States and mode

state_var = tk.StringVar()
state_var_label = tk.Label(log_window, textvariable=state_var)
state_var_label.pack()

mode_frame = tk.Frame(gui_App)
mode_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='e')


mode_var = tk.StringVar()
mode_var_label = ttk.Label(mode_frame,textvariable=mode_var, font=("Arial", 15))
mode_var_label.grid(row=1, column=0, columnspan=3, sticky='n')

mode_var.set("check_mode: current mode is")


trolley_modes = ["init", "normal", "continuous"]

mode_buttons = {}

for j, mode_name in enumerate(trolley_modes):

    style_name = "State.RED.TButton"
    mode_button = ttk.Button(mode_frame, text=f"Mode: {mode_name}", style=style_name)
    mode_button.grid(row=j // 3, column = j % 3, padx=20, pady=20)
    mode_buttons[mode_name] = mode_button

mode_frame.grid_rowconfigure(0, weight=1)
mode_frame.grid_rowconfigure(1, weight=2)
mode_frame.grid_rowconfigure(2, weight=1)

trolley_states = ["INIT", "HOME_OFF", "MOVING_AWAY", "AWAY_OFF", "MOVING_HOME", "ERROR"]

buttons = {}

data_table = ttk.Treeview(table_frame, columns=('timestamp', 'x', 'y', 'z'), show='headings')
# data_table.place(relx=.5, rely=.5, anchor=tk.CENTER)

data_table.heading('timestamp', text="Timestamp")
data_table.heading('x', text="x")
data_table.heading('y', text="y")
data_table.heading('z', text="z")

data_table.column('timestamp', width= 200,anchor='center')
data_table.column('x', width =200,anchor='center')
data_table.column('y', width=200,anchor='center')
data_table.column('z', width=200, anchor='center')

# data_table.grid(row=0, column=0, padx=(0,60), sticky="nsew")
data_table.grid(row=0, column=0, padx=50, pady=30)


data_var = tk.StringVar()
data_var_label = tk.Label(table_frame, textvariable=data_var, font=("Arial", 16))
# data_var_label.pack(padx=10)

# data_table.pack(padx=30, pady=30)


for i, name in enumerate(trolley_states):

    style_name = "State.RED.TButton"
    button = ttk.Button(state_frame, text=f"State: {name}", style=style_name)
    button.grid(row=i // 3, column = i % 3, padx=20, pady=20)
    buttons[name] = button

state_frame.grid_rowconfigure(0, weight=1)
state_frame.grid_rowconfigure(1, weight=2)
state_frame.grid_rowconfigure(2, weight=1)


gui_App.mainloop()
