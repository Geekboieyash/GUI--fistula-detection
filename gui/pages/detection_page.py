import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil
import subprocess
import sys

class DetectionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.uploaded_image_path = None
        
        self.create_widgets()
        
    def create_widgets(self):
        style = ttk.Style()
        style.configure("HandFistula.TFrame", background="#f9f9f9", borderwidth=1, relief="solid")
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TEntry", padding=8, borderwidth=1, relief="solid")
        style.configure("TButton", padding=(10, 20), background="#4CAF50", foreground="white")
        style.map("TButton", background=[("active", "#45a049")])

        container = ttk.Frame(self, style="HandFistula.TFrame")
        container.pack(padx=20, pady=20)

        label_title = ttk.Label(container, text="Choose Detection Type", style="TLabel")
        label_title.grid(row=0, column=0, columnspan=2, pady=10)

        veins_button = tk.Button(container, text="Veins Detection", command=self.veins_detection, bg='#4CAF50', fg='#ffffff')
        veins_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        upload_button = tk.Button(container, text="Upload Image", command=self.upload_image, bg='#4CAF50', fg='#ffffff')
        upload_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    
        self.image_label = tk.Label(self)
        self.image_label.pack()

    def veins_detection(self):
        if self.uploaded_image_path:
            image_name = os.path.basename(self.uploaded_image_path)
            destination_path = os.path.join("model", image_name)
            if not os.path.exists("model"):
                os.makedirs("model")
            shutil.copyfile(self.uploaded_image_path, destination_path)
            model_file = "model/fistula_detection.py"  # Assuming the model is stored in this file
            self.execute_ml_model(model_file, destination_path)
        else: 
            messagebox.showerror("Error", "Please upload an image first.")  

    def upload_image(self):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")))
        if file_path:
            print("Selected file:", file_path)
            self.uploaded_image_path = file_path
        
    def execute_ml_model(self, model_file, image_file):
        try:
            # Build the command to execute the model script with the image file as an argument
            command = [sys.executable, model_file, image_file]

            # Execute the command and capture output
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for the process to finish
            stdout, stderr = process.communicate()

            # Check the return code of the process
            return_code = process.returncode

            if return_code == 0:
                print("Model execution successful.")
                print("Output:")
                print(stdout.decode())
            else:
                print("Model execution failed.")
                print("Error:")
                print(stderr.decode())

        except Exception as e:
            print(f"An error occurred: {e}")

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Hand Fistula detection")
        self.geometry("1000x700")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        pages = (DetectionPage,)
        for F in pages:
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("DetectionPage")
    
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
