import tkinter as tk
from gui.pages.register_page import RegisterPage
from gui.pages.detection_page import DetectionPage

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Hand Fistula detection")
        self.geometry("800x700")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        pages = (RegisterPage, DetectionPage)
        for F in pages:
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("RegisterPage")
        # self.show_frame("re")
    
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
