import tkinter as tk
from tkinter import ttk
import subprocess

class DetectionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.create_widgets()
        
    def create_widgets(self):
        style = ttk.Style()
        style.configure("HandFistula.TFrame", background="#f9f9f9", borderwidth=1, relief="solid")
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", padding=(10, 20), background="#4CAF50", foreground="white")
        style.map("TButton", background=[("active", "#45a049")])

        container = ttk.Frame(self, style="HandFistula.TFrame")
        container.pack(padx=20, pady=20)

        label_title = ttk.Label(container, text="Choose Detection Type", style="TLabel")
        label_title.grid(row=0, column=0, columnspan=2, pady=10)

        veins_button = ttk.Button(container, text="Veins Detection", command=self.veins_detection, style="TButton")
        veins_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        fistula_button = ttk.Button(container, text="Fistula Detection", command=self.fistula_detection, style="TButton")
        fistula_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        file_button = ttk.Button(container, text="Upload File", command=self.upload_file, style="TButton")
        file_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def veins_detection(self):
        # Implement Veins Detection functionality
        self.execute_ml_model("veins_model.py")  # Change to the name of your ML model file
        
    def fistula_detection(self):
        # Implement Fistula Detection functionality
        self.execute_notebook("fistula_detection.ipynb")  # Change to the name of your IPython Notebook file

    def upload_file(self):
        # Implement file upload functionality
        pass
    
    def execute_ml_model(self, model_file):
        subprocess.Popen(["python", model_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def execute_notebook(self, notebook_file):
        subprocess.Popen(["jupyter", "notebook", notebook_file])

# Remaining code for creating the GUI and other pages
