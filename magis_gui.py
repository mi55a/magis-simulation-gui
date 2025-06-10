# GUI for the Magnetometer, easier for user!!

'''
Goals for GUI:
- Display data, message, state, timestamps
- Include log of state changes messages and their timestamps
- Display current state
- User can issue start, stop, and reset commands
- Showcase state of the switches (open/closed) and information
- Be able to resuse functions in command_pub.py and trolley_data_sub.py
'''

import tkinter as tk
from tkinter import ttk
from trolley_data_sub import UserData
import command_pub
import msg_handling as mh
import sys
import get_args as ga
import paho.mqtt.client as mqtt

gui_App = tk.Tk()
gui_App.title("Magnetometer GUI")

gui_App.geometry("600x600")

header_frame = tk.Frame(gui_App, height=50)
header_frame.pack(pady=10)
header_label = tk.Label(header_frame, text="Magnetometer GUI", font=("Arial", 20))
header_label.pack(pady=10)

content = ttk.Frame(gui_App, padding=(10,10,10,10))
content.pack()

 # padding=(10,10,10,10)

object_1 = UserData()
# Display buttons for user to send commands like stop, reset, and start

def command_send(command_value):
    sys.argv = ['command_pub.py', command_value]
    p_ = ga.get_args(add_command_args=True)
    print("It works!!")

start_button = ttk.Button(content, text="Start", command=lambda: command_send("--start"))
start_button.pack()
reset_button = ttk.Button(content, text="Reset", command=lambda: command_send("--reset"))
reset_button.pack()
stop_button = ttk.Button(content, text="Stop", command=lambda: command_send("--stop"))
stop_button.pack()

# Display current state
current_state = object_1.mode
current_state_label = ttk.Label(content, text=f"check_mode: current mode is {current_state}")
current_state_label.pack()
# Trolley/state (timestamp, State,  Location)
trolley_data = object_1.data
trolley_state_label = ttk.Label(content, text=f"Trolley State: {trolley_data}")
trolley_state_label.pack()


# Display data (position), message, state, and timestamp

# Display state of switches (open or closed)
switch_state = object_1.writer.curr_state
switch_state_label = ttk.Label(content, text=f"State of Switch: {switch_state}")
switch_state_label.pack()

# Log of state change message
def open_state_changes_log():
    log_window = tk.Toplevel()
    log_window.title("Log of state changes")
    log_window.geometry("300x200")
    log_change_label = ttk.Label(log_window, text=f"Log change arrived: {switch_state}")
    log_change_label.pack()

log_state_changes_bttn = ttk.Button(content, text="Open log of state changes", command=open_state_changes_log)
log_state_changes_bttn.pack()



gui_App.mainloop()