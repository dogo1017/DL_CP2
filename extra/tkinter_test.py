import tkinter as tk

root = tk.Tk()
root.title("Tkinter Test")
root.minsize(700,500)

tk.Label(root,text="Login").pack()

def return_pressed(event):
    print(event.widget.get())

def on_entry_click(event):
    if entry.get() == 'Enter your name here...':
        entry.delete(0, tk.END)
        entry.config(fg='black')

def on_focusout(event):
    """Function to re-insert placeholder if the entry is left empty."""
    if entry.get() == '':
        entry.insert(0, 'Enter your name here...')
        entry.config(fg='grey')

entry = tk.Entry(root)
entry.insert(0, "Username")
entry.bind("<Return>", return_pressed)
entry.pack(padx=250, pady=5, fill="x")
entry2 = tk.Entry(root)
entry2.insert(0, "Password")
entry2.bind("<Return>", return_pressed)
entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_focusout)
entry2.pack(padx=250, pady=5, fill="x")

root.mainloop()

