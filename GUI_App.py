import tkinter as tk
from tkinter import ttk
import random
from GUI_Simu import Simulation

root = tk.Tk()
root.title("MAGIS-100 Simulation")
root.geometry("600x600")

content = ttk.Frame(root, padding=(10, 10, 10, 10))
content.pack(expand=True, fill="both")

frame = ttk.Frame(content, borderwidth=5, relief='ridge', width=50, height=50)
frame.pack(expand=True, fill="both", padx=5, pady=5)
# magnetic_field_label = ttk.Label(frame, text="Magnetic field: ")
# magnetic_field_label.pack()
data_label = ttk.Label(frame, text="Data Info: ")
data_label.pack()

def submitVelocity():
    global velocity 
    velocity = float(velocity_input.get())

    print("Success")


velocity_label = ttk.Label(content, text="Velocity (can't be 0 or negative): ")
velocity_label.pack()
velocity_input = ttk.Entry(content, width=10)
velocity_input.pack()



submit_velocity = ttk.Button(content, text="Submit Velocity", command=submitVelocity)
submit_velocity.pack()

def submit_Fields():
    global start_1, end_1, start_2, end_2

    start_1 = int(start1_label.get())
    end_1 = int(end1_label.get())
    start_2 = int(start2_label.get())
    end_2 = int(end2_label.get())

    magnetic_field_label = ttk.Label(frame, text=f"Magnetic field: [({start_1},{end_1}), ({start_2},{end_2})] ")
    magnetic_field_label.pack()



    print("Success!")


magneticFieldInput_label = ttk.Label(content, text="Insert Magnetic Field Starts and Ends")
magneticFieldInput_label.pack()

start1_label = ttk.Entry(content, width=10)
start1_label.pack()
end1_label = ttk.Entry(content, width=10)
end1_label.pack()
start2_label = ttk.Entry(content, width=10)
start2_label.pack()
end2_label = ttk.Entry(content, width=10)
end2_label.pack()

submit_field_button = ttk.Button(content, text="Submit Magnetic Fields", command=submit_Fields)
submit_field_button.pack()

def generate_magnetic_field():
    global start1, end1, start2, end2


    start1, end1 = sorted([random.randint(1, 10),random.randint(1,10)])
    start2, end2 = sorted([random.randint(1, 10),random.randint(1,10)])

    start1_label.delete(0, tk.END)
    end1_label.delete(0, tk.END)
    start2_label.delete(0, tk.END)
    end2_label.delete(0, tk.END)

    start1_label.insert(0, start1)
    end1_label.insert(0, end1)
    start2_label.insert(0, start2)
    end2_label.insert(0, end2)

randomField_label = ttk.Label(content, text="Or Generate Random Magnetic Fields!")
randomField_label.pack()

generate_field = ttk.Button(content, text="Generate Magnetic Fields", command=generate_magnetic_field)
generate_field.pack()




def run_simulation():
    simu_1 = Simulation(velocity, start_1, end_1, start_2, end_2)
    simu_1.start()

button = ttk.Button(content, text="Start Simulation", command=run_simulation)
button.pack(pady=10)

root.mainloop()
