import customtkinter as ctk
from PIL import Image
from tkinter import ttk


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")  # blue, green, dark-blue, etc.

states = []
modes =[]
table_row_id = None

app = ctk.CTk()
app.title("Data Simulation GUI")
app.attributes('-zoomed', True)

for col in range(3):
    app.grid_columnconfigure(col, weight=1)

log_window = ctk.CTkToplevel()
log_window.title("Log of state changes")
log_window.geometry("550x100")

plot_window = ctk.CTkToplevel()
plot_window.title("Data Plot")
plot_window.geometry("550x600")
plot_label = ctk.CTkLabel(plot_window, text="Magnetometer Plot")
plot_label.pack()

app.withdraw()
log_window.withdraw()
plot_window.withdraw()

instructions_window = ctk.CTkToplevel()
instructions_window.title("Before you begin")
instructions_window.geometry("500x500")


instructions = (
    "Make sure to fill out and post the Magnetometer Logs"
)

instructions_label = ctk.CTkLabel(instructions_window, text=instructions, wraplength=350)
instructions_label.pack(pady=20, padx=20)

def continue_main():
    instructions_window.destroy()
    app.deiconify()

continue_button = ctk.CTkButton(instructions_window, text="Continue", command=continue_main)
continue_button.pack(pady=10)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=("Arial", 12), rowheight=5)
style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.grid(row=0, column=0, columnspan=3)

header_label = ctk.CTkLabel(header_frame, text="Maggy", font=("Arial", 30))
header_label.pack(pady=10)

magis_logo = Image.open('magis_logo_2.png')
ctk_image = ctk.CTkImage(light_image=magis_logo, dark_image=magis_logo, size=(600, 100))
image_label = ctk.CTkLabel(master=header_frame, image=ctk_image, text="") 
image_label.pack(pady=5) 

time_created = ctk.CTkLabel(header_frame, text="Time created: ", font=("Arial", 30))
time_created.pack()

table_frame = ctk.CTkFrame(app, fg_color='transparent')
table_frame.grid(row=1, column=0, columnspan=3, sticky='n')

data_table = ttk.Treeview(table_frame, columns=('timestamp', 'x', 'y', 'z'), show='headings')
for col in ['timestamp', 'x', 'y', 'z']:
    data_table.heading(col, text=col.capitalize())
    data_table.column(col, width=180, anchor='center')
data_table.grid(row=0, column=0, padx=50, pady=30)

exit_label = ctk.CTkLabel(table_frame, text="Plots created for Magnetometer run!", font=("Arial", 30))
exit_label.grid(row=1, column=0)

command_frame = ctk.CTkFrame(app, fg_color="transparent")
command_frame.grid(row=1, column=0, pady=30)

start_button = ctk.CTkButton(command_frame, text="Start", font=("Arial", 30, "bold"), fg_color="#00A36C", text_color="white")
start_button.pack(pady=40)

reset_button = ctk.CTkButton(command_frame, text="Reset", font=("Arial", 30, "bold"), fg_color="#FFDB58", text_color="white")
reset_button.pack(pady=40)

stop_button = ctk.CTkButton(command_frame, text="Stop", font=("Arial", 30, "bold"), fg_color="#F73942", text_color="white")
stop_button.pack(pady=40)



window_frame = ctk.CTkFrame(app, fg_color="transparent")
window_frame.grid(row=1, column=2, pady=30)

log_changes_button = ctk.CTkButton(window_frame, text="State Changes", font=("Arial", 30, "bold"), fg_color="#6495ED", text_color="white")
log_changes_button.pack(pady=40)

data_plot_button = ctk.CTkButton(window_frame, text="Plot", font=("Arial", 30, "bold"), fg_color="#FF69B4", text_color="white")
data_plot_button.pack(pady=40)

end_button = ctk.CTkButton(window_frame, text="Exit App", font=("Arial", 30, "bold"), fg_color="#A41CF3", text_color="white")
end_button.pack(pady=40)

state_frame = ctk.CTkFrame(app, fg_color="transparent")
state_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')



state_var = ctk.StringVar()
state_var_label = ctk.CTkLabel(log_window, textvariable=state_var)
state_var_label.pack()

mode_frame = ctk.CTkFrame(app, fg_color="transparent")
mode_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='e')

mode_var = ctk.StringVar()
mode_var_label = ctk.CTkLabel(mode_frame,textvariable=mode_var, font=("Arial", 20))
mode_var_label.grid(row=1, column=0, columnspan=3, sticky='n')

mode_var.set("check_mode: current mode is")

trolley_modes = ["init", "normal", "continuous"]

mode_buttons = {}

for j, mode_name in enumerate(trolley_modes):

    # style_name = "State.RED.TButton"
    mode_button = ctk.CTkButton(mode_frame, text=f"Mode: {mode_name}",font=("Arial", 25, "bold"), fg_color="#F73942", text_color="white")
    mode_button.grid(row=j // 3, column = j % 3, padx=20, pady=20)
    mode_buttons[mode_name] = mode_button

mode_frame.grid_rowconfigure(0, weight=1)
mode_frame.grid_rowconfigure(1, weight=2)
mode_frame.grid_rowconfigure(2, weight=1)

trolley_states = ["INIT", "HOME_OFF", "MOVING_AWAY", "AWAY_OFF", "MOVING_HOME", "ERROR"]

buttons = {}

for i, name in enumerate(trolley_states):

    # style_name = "State.RED.TButton"
    button = ctk.CTkButton(state_frame, text=f"State: {name}", font=("Arial", 25, "bold"), fg_color="#F73942", text_color="white")
    button.grid(row=i // 3, column = i % 3, padx=20, pady=20)
    buttons[name] = button

state_frame.grid_rowconfigure(0, weight=1)
state_frame.grid_rowconfigure(1, weight=2)
state_frame.grid_rowconfigure(2, weight=1)



app.mainloop()
