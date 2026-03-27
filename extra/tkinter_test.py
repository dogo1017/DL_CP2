import tkinter as tk

root = tk.Tk()
root.title("Tkinter Test")
root.minsize(700, 500)
root.configure(bg='#302B27')

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(5, weight=1)

frame = tk.Frame(root, bg='#302B27')
frame.grid(row=1, column=0)

tk.Label(frame, text="Login", bg='#302B27', fg='#f5f3f5', font=("Arial", 16)).grid(column=0, row=0, pady=10)

def on_enter(e):
    sign_in['background'] = 'green'

def on_enter(e):
    submit['background'] = 'red'

def on_entry_click(event):
    if event.widget.get() == "Username":
        event.widget.delete(0, tk.END)
        event.widget.config(fg="#F5F3F5")

def on_focusout(event):
    if event.widget.get() == "":
        event.widget.insert(0, "Username")
        event.widget.config(fg="#F5F3F5")

entry = tk.Entry(frame, fg="#F5F3F5", bg='#302B27', highlightthickness=0, bd=5)
entry.insert(0, "Username")
entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_focusout)
entry.grid(row=1, column=0, pady=5)

entry2 = tk.Entry(frame, show="*", fg="#F5F3F5",bg='#302B27', highlightthickness=0, bd=5)
entry2.insert(0, "Password")
entry2.grid(row=2, column=0, pady=5)

button_frame = tk.Frame(frame, bg='#302B27')
button_frame.grid(row=3, column=0, pady=10)

sign_in = tk.Button(button_frame, text="sign up", bg='#302B27', fg='#f5f3f5', highlightthickness=1, bd=0).bind("<Enter>", on_enter).bind("<Leave>", on_leave)
submit = tk.Button(button_frame, text="enter", bg='#302B27', fg='#f5f3f5', highlightthickness=1, bd=0).bind("<Enter>", on_enter).bind("<Leave>", on_leave)


sign_in.grid(row=0, column=0, padx=5)
submit.grid(row=0, column=1, padx=5)

root.mainloop()
