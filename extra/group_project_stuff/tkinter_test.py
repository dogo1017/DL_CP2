import tkinter as tk
from tkinter import messagebox
import csv
import os
import user_registration

DB_FILE = "users.csv"
MIN_PASSWORD_LENGTH = 5

users=["hello"]

def load_users():
    print("load")

def save_user(users,username, password):
    user_registration(users,username, password)

root = tk.Tk()
root.title("Secure Login")
root.minsize(400, 400)
root.configure(bg="#302B27")
root.grid_columnconfigure(0, weight=1)

frame = tk.Frame(root, bg="#302B27")
frame.pack(expand=True)

current_mode = "login" 
error_labels = []

def clear_errors():
    for label in error_labels:
        label.destroy()
    error_labels.clear()

def show_error(text, row):
    lbl = tk.Label(frame, text=text, bg="#302B27", fg="#ff4444", font=("Arial", 8))
    lbl.grid(row=row, column=0, pady=0)
    error_labels.append(lbl)

def on_key_press(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, tk.END)
        event.widget.config(fg="#F5F3F5")
        if placeholder == "Password":
            event.widget.config(show="*")

def on_focusout(event, placeholder):
    if event.widget.get() == "":
        event.widget.insert(0, placeholder)
        event.widget.config(fg="grey")
        if placeholder == "Password":
            event.widget.config(show="")

def on_entry_click(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, tk.END)
        event.widget.config(fg="#F5F3F5")
        if placeholder == "Password":
            event.widget.config(show="*")

def toggle_mode():
    global current_mode
    current_mode = "signup" if current_mode == "login" else "login"
    render_screen()

def handle_submit(user_ent, pass_ent):
    clear_errors()
    username = user_ent.get()
    password = pass_ent.get()
    
    has_error = False
    if not username or username == "Username":
        show_error("Username required", 2)
        has_error = True
    
    if not password or password == "Password":
        show_error("Password required", 4)
        has_error = True
    elif len(password) < MIN_PASSWORD_LENGTH:
        show_error(f"Password must be > {MIN_PASSWORD_LENGTH} chars", 4)
        has_error = True
        
    if has_error: return

    users = load_users()
    
    if current_mode == "login":
        if users.get(username) == password:
            print("Logged in successfully!")
        else:
            show_error("Invalid username or password", 5)
    else:
        if username in users:
            show_error("Username already exists", 2)
        else:
            save_user(username, password)
            toggle_mode()

def render_screen():
    for widget in frame.winfo_children():
        widget.destroy()
    clear_errors()

    title_text = "Login" if current_mode == "login" else "Sign Up"
    btn_text = "Login" if current_mode == "login" else "Sign Up"
    toggle_text = "Need an account? Sign Up" if current_mode == "login" else "Have an account? Login"

    tk.Label(frame, text=title_text, bg="#302B27", fg="#f5f3f5", font=("Arial", 20, "bold")).grid(column=0, row=0, pady=20)

    entry_user = tk.Entry(frame, fg="grey", bg="#4a443f", insertbackground="white", relief="flat", font=("Arial", 10))
    entry_user.insert(0, "Username")
    entry_user.bind("<FocusIn>", lambda e: on_entry_click(e, "Username"))
    entry_user.bind("<FocusOut>", lambda e: on_focusout(e, "Username"))
    entry_user.grid(row=1, column=0, pady=5, ipadx=10, ipady=5)

    entry_pass = tk.Entry(frame, fg="grey", bg="#4a443f", insertbackground="white", relief="flat", font=("Arial", 10))
    entry_pass.insert(0, "Password")
    entry_pass.bind("<FocusIn>", lambda e: on_entry_click(e, "Password"))
    entry_pass.bind("<FocusOut>", lambda e: on_focusout(e, "Password"))
    entry_pass.grid(row=3, column=0, pady=5, ipadx=10, ipady=5)

    submit = tk.Button(frame, text=btn_text, bg="#6b5b4e", fg="#f5f3f5", font=("Arial", 10, "bold"), 
                       relief="raised", width=15, command=lambda: handle_submit(entry_user, entry_pass))
    submit.grid(row=5, column=0, pady=20)

    toggle_btn = tk.Button(frame, text=toggle_text, bg="#302B27", fg="#aaa", font=("Arial", 8), 
                           relief="flat", command=toggle_mode)
    toggle_btn.grid(row=6, column=0)

render_screen()
root.mainloop()
