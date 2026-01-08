import tkinter as tk
from tkinter import ttk
import pyperclip
import requests
import subprocess
import sys
from tkinter import messagebox, Tk
LOCAL_VERSION = "1.0.0"  # Change this whenever you release a new version
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/version.txt"
GITHUB_EXE_URL = "https://github.com/yourusername/yourrepo/releases/latest/download/yourapp.exe"

def check_update():
    try:
        r = requests.get(GITHUB_VERSION_URL, timeout=5)
        r.raise_for_status()
        latest_version = r.text.strip()
        if latest_version != LOCAL_VERSION:
            # Ask user to update
            root_check = Tk()
            root_check.withdraw()  # hide main window
            if messagebox.askyesno("Update Available", f"Version {latest_version} is available. Update now?"):
                root_check.destroy()
                # Launch updater script
                subprocess.Popen([sys.executable, "updater.py"])
                sys.exit()  # close current app to allow update
            root_check.destroy()
    except Exception as e:
        print("Update check failed:", e)

check_update()


# ================= DATA =================

AIRPORTS = {
    # Greater Rockford International — 3 runways (parallel 07/25 L, C, R)
    "IRFD": ["07L", "07C", "07R", "25L", "25C", "25R"],

    # Perth International — typically 15/33 & 11/29
    "IPPH": ["15", "33", "11", "29"],

    # Tokyo International (Orenji) — 02/20 and 13/31
    "ITKO": ["02", "20", "13", "31"],

    # Izolirani International — single long runway (around 10/28)
    "IZOL": ["10", "28"],

    # Mellor — one runway (07/25)
    "IMLR": ["07", "25"],

    # Larnaca Airport — often portrayed on PTFS (similar to Larnaca LCLK)
    "ILAR": ["04", "22"],

    # Paphos Airport — one runway (typically 04/22)
    "IPAP": ["04", "22"],

    # Saint Barthélemy Airport — single runway 09/27
    "IBTH": ["09", "27"],

    # Saba — tiny runway (often similar to real-life Saba runway)
    "IDCS": ["10", "28"],

    # (Optional) Training Centre — runway 18/36
    "ITRC": ["18", "36"]
}


CALLSIGNS = ["AAL", "DAL", "UAL", "SWA", "JBU", "ASA", "FFT"]

ROLE_ACTIONS = {
    "Tower": ["Cleared for Takeoff", "Cleared to Land"],
    "Ground": ["Taxi to Runway", "Hold Short"],
    "Center": [
        "Climb and Maintain",
        "Descend and Maintain",
        "Turn Heading",
        "Cleared ILS Approach"
    ]
}

GLOBAL_MESSAGES = {
    "ATC Online":
        "ATC online.\n\nVoice Chat / ATC Radio available and preferred; "
        "text requests may be delayed or missed.",

    "Runway Caution":
        "Use caution, runway may be occupied.",

    "Heavy Traffic":
        "Attention all {airport} traffic: ATC is currently handling heavy traffic. "
        "Expect possible delays. Continue operations as normal and maintain safe separation.",

    "ATC Signing Off (Uncontrolled)":
        "{airport} ATC signing off. ATC services no longer available; "
        "uncontrolled operations in effect. Thanks everyone, and safe flights.",

    "ATC Signing Off (Handoff)":
        "{airport} ATC signing off. ATC services will continue with the next controller."
}

# ================= APP =================

root = tk.Tk()
root.title("PTFS ATC Helper")
root.geometry("420x540")

selected_role = tk.StringVar()
selected_airport = tk.StringVar()

# ================= FRAMES =================

role_frame = tk.Frame(root)
airport_frame = tk.Frame(root)
menu_frame = tk.Frame(root)
action_frame = tk.Frame(root)

def show(frame):
    for f in (role_frame, airport_frame, menu_frame, action_frame):
        f.pack_forget()
    frame.pack(fill="both", expand=True)

def back_to_role():
    show(role_frame)

# ================= ROLE SELECT =================

tk.Label(role_frame, text="Select ATC Role", font=("Arial", 16)).pack(pady=20)

for r in ["Tower", "Ground", "Center", "All"]:
    tk.Button(role_frame, text=r, command=lambda x=r: (
        selected_role.set(x),
        show(airport_frame)
    )).pack(fill="x", padx=70, pady=5)

# ================= AIRPORT =================

tk.Label(airport_frame, text="Select Airport", font=("Arial", 16)).pack(pady=20)

ttk.Combobox(
    airport_frame,
    textvariable=selected_airport,
    values=list(AIRPORTS.keys())
).pack()

tk.Button(
    airport_frame,
    text="Continue",
    command=lambda: show(menu_frame)
).pack(pady=20)

tk.Button(
    airport_frame,
    text="Change ATC Role",
    command=back_to_role
).pack()

# ================= MAIN MENU =================

tk.Label(menu_frame, text="Select Menu", font=("Arial", 16)).pack(pady=20)

def build_menu():
    for w in menu_frame.winfo_children()[1:]:
        w.destroy()

    roles = ["Tower", "Ground", "Center"] if selected_role.get() == "All" else [selected_role.get()]

    for r in roles:
        tk.Button(
            menu_frame,
            text=r,
            command=lambda x=r: open_role_menu(x)
        ).pack(fill="x", padx=70, pady=5)

    tk.Button(
        menu_frame,
        text="Global / ATC Messages",
        command=open_global
    ).pack(fill="x", padx=70, pady=10)

    tk.Button(
        menu_frame,
        text="Change Airport",
        command=lambda: show(airport_frame)
    ).pack(pady=5)

    tk.Button(
        menu_frame,
        text="Change ATC Role",
        command=back_to_role
    ).pack(pady=5)

menu_frame.bind("<Visibility>", lambda e: build_menu())

# ================= ROLE ACTIONS =================

def open_role_menu(role):
    clear(action_frame)
    tk.Label(action_frame, text=f"{role} Actions", font=("Arial", 15)).pack(pady=10)

    for act in ROLE_ACTIONS[role]:
        tk.Button(
            action_frame,
            text=act,
            command=lambda a=act: open_details(role, a)
        ).pack(fill="x", padx=60, pady=4)

    global_back(action_frame)
    show(action_frame)

# ================= GLOBAL =================

def open_global():
    clear(action_frame)
    tk.Label(action_frame, text="Global ATC Messages", font=("Arial", 15)).pack(pady=10)

    status = tk.Label(action_frame, text="")
    status.pack()

    def copy(msg):
        pyperclip.copy(msg)
        status.config(text="✔ Copied to clipboard")

    for name, template in GLOBAL_MESSAGES.items():
        tk.Button(
            action_frame,
            text=name,
            command=lambda t=template: copy(
                t.format(airport=selected_airport.get())
            )
        ).pack(fill="x", padx=40, pady=4)

    global_back(action_frame)
    show(action_frame)

# ================= DETAILS =================

# ===== GLOBAL STORAGE =====
recent_callsigns = []  # store last N full callsigns
recent_winds = []      # store last N wind entries as tuples (dir, spd)
MAX_CALLSIGNS = 10

def open_details(role, action):
    clear(action_frame)

    runway = tk.StringVar()
    callsign = tk.StringVar()
    flight = tk.StringVar()
    wind_dir = tk.StringVar()
    wind_spd = tk.StringVar()
    turn_dir = tk.StringVar()
    heading = tk.StringVar()

    tk.Label(action_frame, text=f"{role} – {action}", font=("Arial", 14)).pack(pady=10)

    # Runway
    ttk.Label(action_frame, text="Runway").pack()
    ttk.Combobox(action_frame, textvariable=runway, values=AIRPORTS[selected_airport.get()]).pack()

    # Callsign
    ttk.Label(action_frame, text="Callsign").pack()
    callsign_entry = ttk.Combobox(action_frame, values=CALLSIGNS, textvariable=callsign)
    callsign_entry.pack()

    # Flight #
    ttk.Label(action_frame, text="Flight #").pack()
    flight_entry = ttk.Entry(action_frame, textvariable=flight)
    flight_entry.pack()

    # Tower winds
    if role == "Tower" and action in ["Cleared for Takeoff", "Cleared to Land"]:
        ttk.Label(action_frame, text="Wind Direction").pack()
        wind_dir_entry = ttk.Entry(action_frame, textvariable=wind_dir)
        wind_dir_entry.pack()

        ttk.Label(action_frame, text="Wind Speed (knots)").pack()
        wind_spd_entry = ttk.Entry(action_frame, textvariable=wind_spd)
        wind_spd_entry.pack()

        # Button to use last wind
        if recent_winds:
            last_wind_dir, last_wind_spd = recent_winds[-1]
            wind_dir.set(last_wind_dir)
            wind_spd.set(last_wind_spd)

        tk.Button(action_frame, text="Use Last Wind", command=lambda: (
            wind_dir.set(recent_winds[-1][0] if recent_winds else ""),
            wind_spd.set(recent_winds[-1][1] if recent_winds else "")
        )).pack(pady=2)

    # Turn Heading
    if action == "Turn Heading":
        ttk.Label(action_frame, text="Turn Direction").pack()
        ttk.Combobox(action_frame, values=["Left", "Right"], textvariable=turn_dir).pack()
        ttk.Label(action_frame, text="Heading").pack()
        ttk.Entry(action_frame, textvariable=heading).pack()

    # Recent full callsigns
    tk.Label(action_frame, text="Recent Callsigns").pack()
    cs_listbox = tk.Listbox(action_frame, height=5)
    cs_listbox.pack()
    for cs in recent_callsigns:
        cs_listbox.insert(tk.END, cs)

    # Fill all fields when clicked
    def fill_recent(event):
        if cs_listbox.curselection():
            full_cs = cs_listbox.get(cs_listbox.curselection()[0])

            # Split callsign and number
            for code in CALLSIGNS:
                if full_cs.startswith(code):
                    callsign.set(code)
                    flight.set(full_cs[len(code):])
                    break

            # Fill last wind if stored
            for item in reversed(recent_winds):
                # match this callsign? optional, or just last wind
                wind_dir.set(item[0])
                wind_spd.set(item[1])
                break  # take most recent

    cs_listbox.bind('<<ListboxSelect>>', fill_recent)

    # Generate button
    def generate():
        full_callsign = f"{callsign.get()}{flight.get()}"
        # Save full callsign
        if full_callsign not in recent_callsigns:
            recent_callsigns.append(full_callsign)
            if len(recent_callsigns) > MAX_CALLSIGNS:
                recent_callsigns.pop(0)

        # Save wind
        if role == "Tower" and action in ["Cleared for Takeoff", "Cleared to Land"]:
            recent_winds.append((wind_dir.get(), wind_spd.get()))
            if len(recent_winds) > MAX_CALLSIGNS:
                recent_winds.pop(0)

        # Build message
        if action == "Cleared for Takeoff":
            msg = f"{full_callsign}, cleared for takeoff Runway {runway.get()}, wind {wind_dir.get()} at {wind_spd.get()} knots. Have a good flight."
        elif action == "Cleared to Land":
            msg = f"{full_callsign}, cleared to land Runway {runway.get()}, wind {wind_dir.get()} at {wind_spd.get()} knots."
        elif action == "Turn Heading":
            msg = f"{full_callsign}, turn {turn_dir.get().lower()} heading {heading.get()}."
        elif action == "Cleared ILS Approach":
            msg = f"{full_callsign}, cleared ILS approach Runway {runway.get()}."
        else:
            msg = f"{full_callsign}, {action.lower()}."

        pyperclip.copy(msg)
        open_role_menu(role)

    tk.Button(action_frame, text="Generate & Copy", command=generate).pack(pady=10)
    global_back(action_frame)
    show(action_frame)




# ================= HELPERS =================

def clear(frame):
    for w in frame.winfo_children():
        w.destroy()

def global_back(frame):
    tk.Button(frame, text="Change ATC Role", command=back_to_role).pack(pady=5)
    tk.Button(frame, text="Back", command=lambda: show(menu_frame)).pack()

# ================= START =================

show(role_frame)
root.mainloop()
