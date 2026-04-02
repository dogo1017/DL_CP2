import tkinter as tk

root = tk.Tk()
root.title("Tkinter Test")
root.minsize(700, 500)
root.configure(bg="#302B27")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(5, weight=1)

frame = tk.Frame(root, bg="#302B27")
frame.grid(row=1, column=0)

tk.Label(frame, text="Login", bg="#302B27", fg="#f5f3f5", font=("Arial", 16)).grid(column=0, row=0, pady=10)

def on_key_press(event, placeholder):
    """Deletes placeholder only when the user starts typing."""
    if event.widget.get() == placeholder:
        event.widget.delete(0, tk.END)
        event.widget.config(fg="#F5F3F5")
        if placeholder == "Password":
            event.widget.config(show="*")

def on_entry_click(event, placeholder):
    """Highlights existing text on click; does not delete yet."""
    if event.widget.get() == placeholder:
        event.widget.selection_range(0, tk.END)
        event.widget.icursor(0)

def on_focusout(event, placeholder):
    """Restores placeholder if empty."""
    if event.widget.get() == "":
        event.widget.insert(0, placeholder)
        event.widget.config(fg="#F5F3F5")
        if placeholder == "Password":
            event.widget.config(show="")

def deselect_all(event):
    """Removes focus from entries if clicking on the background."""
    if event.widget == root or event.widget == frame:
        root.focus_set()

entry = tk.Entry(frame, fg="#F5F3F5", bg="#302B27", highlightthickness=1, bd=2)
entry.insert(0, "Username")
entry.bind("<FocusIn>", lambda e: on_entry_click(e, "Username"))
entry.bind("<FocusOut>", lambda e: on_focusout(e, "Username"))
entry.bind("<KeyPress>", lambda e: on_key_press(e, "Username"))
entry.grid(row=1, column=0, pady=5)

entry2 = tk.Entry(frame, fg="#F5F3F5", bg="#302B27", highlightthickness=1, bd=2, show="")
entry2.insert(0, "Password")
entry2.bind("<FocusIn>", lambda e: on_entry_click(e, "Password"))
entry2.bind("<FocusOut>", lambda e: on_focusout(e, "Password"))
entry2.bind("<KeyPress>", lambda e: on_key_press(e, "Password"))
entry2.grid(row=2, column=0, pady=5)

def on_enter(e): e.widget.config(background="#f5f3f5", fg="#302B27")
def on_leave(e): e.widget.config(background="#302B27", fg="#f5f3f5")

button_frame = tk.Frame(frame, bg="#302B27")
button_frame.grid(row=3, column=0, pady=10)

sign_in = tk.Button(button_frame, text="sign up", bg="#302B27", fg="#f5f3f5", bd=1, relief="flat")
sign_in.bind("<Enter>", on_enter)
sign_in.bind("<Leave>", on_leave)
sign_in.grid(row=0, column=0, padx=5)

submit = tk.Button(button_frame, text="enter", bg="#302B27", fg="#f5f3f5", bd=1, relief="flat")
submit.bind("<Enter>", on_enter)
submit.bind("<Leave>", on_leave)
submit.grid(row=0, column=1, padx=5)

root.bind("<Button-1>", deselect_all)

root.mainloop()
