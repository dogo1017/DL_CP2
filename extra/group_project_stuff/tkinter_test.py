import customtkinter as ctk
import csv
import os
import login
import user_registration
DB_FILE = "extra/group_project_stuff/users.csv"
MIN_PASSWORD_LENGTH = 5
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance")
        self.geometry("400x450")
        self.wm_minsize(280,350)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_mode = "login"
        self.error_labels = []

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.frame.grid_columnconfigure(0, weight=1)

        self.render_screen()

    def clear_errors(self):
        for label in self.error_labels:
            label.destroy()
        self.error_labels.clear()

    def show_error(self, text, row):
        lbl = ctk.CTkLabel(self.frame, text=text, text_color="#ff4444", font=("Arial", 11))
        lbl.grid(row=row, column=0, pady=(0, 5))
        self.error_labels.append(lbl)

    def toggle_mode(self):
        self.current_mode = "signup" if self.current_mode == "login" else "login"
        self.render_screen()

    def handle_submit(self, user_ent, pass_ent):
        self.clear_errors()
        username = user_ent.get()
        password = pass_ent.get()
        has_error = False

        if not username or username == "Username":
            self.show_error("Username required", 2)
            has_error = True
        
        if not password or password == "Password":
            self.show_error("Password required", 4)
            has_error = True
        elif len(password) < MIN_PASSWORD_LENGTH:
            self.show_error(f"Password must be > {MIN_PASSWORD_LENGTH} chars", 4)
            has_error = True

        if has_error: return

        users = user_registration.load_csv()
        if self.current_mode == "login":
            if login.log_in(username,password):
                print("Logged in successfully!")
            else:
                self.show_error("Invalid username or password", 7)
        else:
            if username in users:
                self.show_error("Username already exists", 2)
            else:
                user_registration.save_changes(user_registration.register(user_registration.load_csv(),password,username))
                self.toggle_mode()

    def render_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.clear_errors()

        title_text = "Login" if self.current_mode == "login" else "Sign Up"
        btn_text = "Login" if self.current_mode == "login" else "Sign Up"
        toggle_text = "Need an account? Sign Up" if self.current_mode == "login" else "Have an account? Login"

        ctk.CTkLabel(self.frame, text=title_text, font=("Arial", 24, "bold")).grid(row=0, column=0, pady=20)

        entry_user = ctk.CTkEntry(self.frame, placeholder_text="Username", width=250, height=40)
        entry_user.grid(row=1, column=0, pady=10)

        entry_pass = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*", width=250, height=40)
        entry_pass.grid(row=3, column=0, pady=10)

        submit = ctk.CTkButton(self.frame, text=btn_text, 
                               command=lambda: self.handle_submit(entry_user, entry_pass), width=150)
        submit.grid(row=5, column=0, pady=25)

        toggle_btn = ctk.CTkButton(self.frame, text=toggle_text, fg_color="transparent", 
                                   text_color="#aaa", hover=False, command=self.toggle_mode, font=("Arial", 10))
        toggle_btn.grid(row=6, column=0)

app = App()
app.mainloop()
