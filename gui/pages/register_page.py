import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# from tkinter import filedialog

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        style = ttk.Style()
        style.configure("HandFistula.TFrame", background="#f9f9f9", borderwidth=1, relief="solid")
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TEntry", padding=8, borderwidth=1, relief="solid")
        style.configure("TButton", padding=(10, 20), background="#4CAF50", foreground="white")
        style.map("TButton", background="#4CAF50", foreground="white")

        container = ttk.Frame(self, style="HandFistula.TFrame")
        container.pack(padx=20, pady=20)

        label_user = ttk.Label(container, text="Username:")
        label_user.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        label_pw = ttk.Label(container, text="Password:")
        label_pw.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_user = ttk.Entry(container, width=20, cursor="xterm", style="TEntry")
        self.entry_user.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.entry_pw = ttk.Entry(container, width=20, cursor="xterm", show="*", style="TEntry")
        self.entry_pw.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        login_button = tk.Button(container, text="Login", command=self.login, bg='#4CAF50', fg='#ffffff')
        login_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        button = tk.Button(container, text="Register", command=lambda: SignupPage(), bg='#4CAF50', fg='#ffffff')
        button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.image_label = tk.Label(self)
        self.image_label.pack()

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pw.get()
        validation = self.validate_user(username, password)
        if validation:
            messagebox.showinfo("Login Successful", f"Welcome {username}")
            self.controller.show_frame("DetectionPage")  # Show the DetectionPage after successful login
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def validate_user(self, username, password):
        # Checks the text file for a username/password combination.
        try:
            with open("credentials.txt", "r") as credentials:
                for line in credentials:
                    line = line.strip().split(",")
                    if len(line) >= 4 and line[1] == username and line[3] == password:
                        return True
            return False
        except FileNotFoundError:
            print("Validation false")
            return False
        

class SignupPage(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
        # pack_propagate prevents the window resizing to match the widgets
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")

        self.geometry("250x150")
        self.resizable(0, 0)

        self.title("Registration")

        text_styles = {"font": ("Verdana", 10),
                       "background": "#3F6BAA",
                       "foreground": "#E1FFFF"}

        label_user = tk.Label(main_frame, text_styles, text="New Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(main_frame, text_styles, text="New Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(main_frame, width=20, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(main_frame, width=20, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(main_frame, text="Create Account", command=lambda: signup())
        button.grid(row=4, column=1)

        def signup():
            # Creates a text file with the Username and password
            user = entry_user.get()
            pw = entry_pw.get()
            validation = validate_user(user)
            if not validation:
                tk.messagebox.showerror("Information", "That Username already exists")
            else:
                if len(pw) > 3:
                    credentials = open("credentials.txt", "a")
                    credentials.write(f"Username,{user},Password,{pw},\n")
                    credentials.close()
                    tk.messagebox.showinfo("Information", "Your account details have been stored.")
                    SignupPage.destroy(self)

                else:
                    tk.messagebox.showerror("Information", "Your password needs to be longer than 3 values.")

        def validate_user(username):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username:
                            return False
                return True
            except FileNotFoundError:
                return True
