import tkinter as tk
from tkinter import ttk
import importlib
import GUI_Simu
importlib.reload(GUI_Simu)


print("✅ THIS is the GUI file being run!")
print("Imported from:", GUI_Simu.__file__)
print("✅ I am running: ", __file__)

root = tk.Tk()
root.title("MAGIS-100 Simulation")


root.geometry("600x600")

content = ttk.Frame(root, padding=(10, 10, 10, 10))
content.pack(expand=True, fill="both") 


frame = ttk.Frame(content, borderwidth=5, relief='ridge')
frame.pack(expand=True, fill="both", padx=10, pady=10)  


button = ttk.Button(content, text="HELOOO")
button.pack(pady=10)

root.mainloop()