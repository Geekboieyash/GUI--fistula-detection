import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label_user = tk.Label(self, text="New Username:")
        label_user.grid(row=0, column=0, padx=10, pady=10)

        label_pw = tk.Label(self, text="New Password:")
        label_pw.grid(row=1, column=0, padx=10, pady=10)

        self.entry_user = ttk.Entry(self, width=20, cursor="xterm")
        self.entry_user.grid(row=0, column=1, padx=10, pady=10)

        self.entry_pw = ttk.Entry(self, width=20, cursor="xterm", show="*")
        self.entry_pw.grid(row=1, column=1, padx=10, pady=10)

        button = ttk.Button(self, text="Create Account", command=self.signup)
        button.grid(row=2, column=1, padx=10, pady=10)

    def signup(self):
        user = self.entry_user.get()
        pw = self.entry_pw.get()
        validation = self.validate_user(user)
        if not validation:
            messagebox.showerror("Error", "That username already exists")
        else:
            if len(pw) > 3:
                with open("credentials.txt", "a") as credentials:
                    credentials.write(f"Username,{user},Password,{pw},\n")
                messagebox.showinfo("Success", "Your account has been created")
                self.controller.show_frame("LoginPage")
            else:
                messagebox.showerror("Error", "Your password needs to be longer than 3 characters")

    def validate_user(self, username):
        try:
            with open("credentials.txt", "r") as credentials:
                for line in credentials:
                    line = line.split(",")
                    if line[1] == username:
                        return False
            return True
        except FileNotFoundError:
            return True
