import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import cv2

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
        style.map("TButton", background="#4CAF50", foreground="white")

        container = ttk.Frame(self, style="HandFistula.TFrame", width=300, height=200)
        container.pack(padx=20, pady=20)

        label_title = ttk.Label(container, text="Choose Detection Type", style="TLabel")
        label_title.grid(row=0, column=0, columnspan=2, pady=10)
        
        veins_button = tk.Button(container, text="Veins Detection", command=lambda: self.veins_detection(), bg='#4CAF50', fg='#ffffff')
        veins_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        upload_button = tk.Button(container, text="Upload Image", command=self.upload_image, bg='#4CAF50', fg='#ffffff')
        upload_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    
        self.image_label = tk.Label(self)
        self.image_label.pack()

    def veins_detection(self):
        if self.uploaded_image_path:
            # Perform vein detection on the uploaded image
            result_image = self.detect_veins(self.uploaded_image_path)
            
            # Display the result image
            self.display_image(result_image)
        
    def detect_veins(self, image_path):
        # Read the image
        org_image = cv2.imread(image_path)
        
        # Your vein detection logic here
        
        # For demonstration, return the original image
        return org_image
        
    def display_image(self, image):
        # Convert the image from OpenCV format to PIL format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image)
        
        # Resize the image to fit the window if necessary
        max_width = 800
        if image_pil.width > max_width:
            image_pil.thumbnail((max_width, max_width), Image.ANTIALIAS)
        
        # Convert the image to tkinter format
        image_tk = ImageTk.PhotoImage(image_pil)
        
        # Update the label to display the image
        self.image_label.configure(image=image_tk)
        self.image_label.image = image_tk
            
    def upload_image(self):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")))
        if file_path:
            self.uploaded_image_path = file_path
        
# Create the GUI
root = tk.Tk()
detection_page = DetectionPage(root, None)
detection_page.pack(fill="both", expand=True)
root.mainloop()
