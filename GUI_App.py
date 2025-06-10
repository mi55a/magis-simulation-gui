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
magnetic_field_label = ttk.Label(frame, text="Magnetic field: ")
magnetic_field_label.pack()

position_label = ttk.Label(frame, text="Position: --m")
position_label.pack()
time_label = ttk.Label(frame, text="Time: --s")
time_label.pack()



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

    submit_field_button.config(state="disabled")



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




# csv_enabled = False

# def csv_button_on():
#     global csv_enabled
#     csv_enabled = True



def run_simulation():
    simu_1 = Simulation(velocity, start_1, end_1, start_2, end_2)
    def update_labels(curr_time, position):
        position_label.config(text=f"Position: {position:.2f} m")
        time_label.config(text=f"Time: {curr_time:.1f} s")
        frame.update_idletasks()
        
    simu_1.start(update_callback=update_labels)
    # info = simu_1.get_variables()

    data_label = ttk.Label(frame, text=f"{simu_1.atom_continuesText}")
    data_label.pack()
    data_label2 = ttk.Label(frame, text= f"{simu_1.atom_stopsText}")
    data_label2.pack()

    # WIP: Create CSV file


    # csv_button = ttk.Button(content, text="Create CSV", command=csv_button_on)
    # csv_button.pack()

    # if csv_enabled == True:
    #     name_label = ttk.Label(content, text="Provide a name for the file: ")
    #     name_label.pack()
    #     name_entry = ttk.Entry(content, width=10)
    #     name_entry.pack()
    #     def save_csv():
    #         name = name_entry.get().strip()
    #         if name:
    #             simu_1.create_csv(name)
    #     save_button = ttk.Button(content, text="Save CSV", command=save_csv)
    #     save_button.pack()

    
button = ttk.Button(content, text="Start Simulation", command=run_simulation)
button.pack(pady=10)

root.mainloop()
