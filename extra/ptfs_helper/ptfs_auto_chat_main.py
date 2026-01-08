import tkinter as tk
from tkinter import ttk
import pyperclip

# ================= DATA =================

AIRPORTS = {
    "IRFD": ["07L", "07C", "07R", "25L", "25C", "25R"],
    "IPPH": ["15", "33", "11", "29"],
    "ITKO": ["02", "20", "13", "31"],
    "IZOL": ["10", "28"],
    "IMLR": ["07", "25"],
    "ILAR": ["04", "22"],
    "IPAP": ["04", "22"],
    "IBTH": ["09", "27"],
    "IDCS": ["10", "28"],
    "ITRC": ["18", "36"]
}

recent_callsigns = []
recent_wind = {"dir": "", "spd": ""}
MAX_RECENT = 8


CALLSIGNS = ["AAL", "DAL", "UAL", "SWA", "JBU", "ASA", "FFT"]

ROLE_ACTIONS = {
    "Tower": [
        "Cleared for Takeoff",
        "Cleared to Land",
        "Line Up and Wait"
    ],
    "Ground": ["Taxi Instructions"],
    "Center": [
        "Climb and Maintain",
        "Descend and Maintain",
        "Turn Heading",
        "Cleared ILS Approach"
    ]
}

GLOBAL_MESSAGES = {
    "ATC Online":
        "ATC online.\n\nVoice chat preferred; text requests accepted but may be missed or delayed.",
    "Runway Caution":
        "Use caution, runway may be occupied.",
    "Heavy Traffic":
        "Attention all {airport} traffic: ATC is experiencing heavy traffic. Expect delays.",
    "ATC Signing Off (Uncontrolled)":
        "{airport} ATC signing off. Uncontrolled operations in effect.",
    "ATC Signing Off (Handoff)":
        "{airport} ATC signing off. ATC services will continue with the next controller."
}

# ================= APP =================

root = tk.Tk()
root.title("PTFS ATC Helper")
root.geometry("460x650")

selected_role = tk.StringVar()
selected_airport = tk.StringVar()

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
    tk.Button(
        role_frame,
        text=r,
        command=lambda x=r: (selected_role.set(x), show(airport_frame))
    ).pack(fill="x", padx=80, pady=6)

# ================= AIRPORT =================

tk.Label(airport_frame, text="Select Airport", font=("Arial", 16)).pack(pady=20)

ttk.Combobox(
    airport_frame,
    textvariable=selected_airport,
    values=list(AIRPORTS.keys())
).pack()

tk.Button(airport_frame, text="Continue", command=lambda: show(menu_frame)).pack(pady=15)
tk.Button(airport_frame, text="Change Role", command=back_to_role).pack()

# ================= MAIN MENU =================

tk.Label(menu_frame, text="Menu", font=("Arial", 16)).pack(pady=20)

def build_menu():
    for w in menu_frame.winfo_children()[1:]:
        w.destroy()

    roles = (
        ["Tower", "Ground", "Center"]
        if selected_role.get() == "All"
        else [selected_role.get()]
    )

    for r in roles:
        tk.Label(menu_frame, text=r, font=("Arial", 13, "bold")).pack(pady=(10, 2))

        for act in ROLE_ACTIONS[r]:
            tk.Button(
                menu_frame,
                text=act,
                command=lambda a=act, role=r: open_action(role, a)
            ).pack(fill="x", padx=80, pady=4)

    tk.Button(
        menu_frame,
        text="Global / ATC Messages",
        command=open_global
    ).pack(fill="x", padx=80, pady=10)

    tk.Button(menu_frame, text="Change Airport", command=lambda: show(airport_frame)).pack(pady=4)
    tk.Button(menu_frame, text="Change Role", command=back_to_role).pack()

menu_frame.bind("<Visibility>", lambda e: build_menu())

# ================= GLOBAL =================

def open_global():
    clear(action_frame)
    tk.Label(action_frame, text="Global ATC Messages", font=("Arial", 15)).pack(pady=10)

    status = tk.Label(action_frame, text="")
    status.pack()

    def copy(msg):
        pyperclip.copy(msg)
        status.config(text="✔ Copied")

    for name, template in GLOBAL_MESSAGES.items():
        tk.Button(
            action_frame,
            text=name,
            command=lambda t=template: copy(t.format(airport=selected_airport.get()))
        ).pack(fill="x", padx=60, pady=4)

    tk.Button(action_frame, text="Back", command=lambda: show(menu_frame)).pack(pady=10)
    show(action_frame)

# ================= ACTION ROUTER =================

def open_action(role, action):
    if action == "Taxi Instructions":
        open_taxi(role)
    else:
        open_generic(role, action)

# ================= TAXI (UNCHANGED) =================

def open_taxi(role):
    clear(action_frame)
    tk.Label(action_frame, text="Taxi Instructions", font=("Arial", 15)).pack(pady=10)

    callsign = tk.StringVar()
    flight = tk.StringVar()

    ttk.Label(action_frame, text="Callsign").pack()
    ttk.Combobox(action_frame, values=CALLSIGNS, textvariable=callsign).pack()

    ttk.Label(action_frame, text="Flight Number").pack()
    ttk.Entry(action_frame, textvariable=flight).pack()

    tk.Label(action_frame, text="Taxi Route").pack(pady=6)
    route_box = tk.Listbox(action_frame, height=5)
    route_box.pack()

    route_entry = tk.StringVar()
    ttk.Entry(action_frame, textvariable=route_entry).pack()

    def add():
        if route_entry.get():
            route_box.insert(tk.END, route_entry.get())
            route_entry.set("")

    def remove():
        if route_box.curselection():
            route_box.delete(route_box.curselection())

    tk.Button(action_frame, text="Add Taxiway", command=add).pack(pady=2)
    tk.Button(action_frame, text="Remove Selected", command=remove).pack(pady=2)

    target_type = tk.StringVar()
    ttk.Combobox(
        action_frame,
        textvariable=target_type,
        values=[
            "Holding Point (Short of Runway)",
            "Gate",
            "Cargo Apron",
            "Fuel Stand",
            "Custom"
        ]
    ).pack(pady=6)

    runway = tk.StringVar()
    hold = tk.StringVar()
    gate = tk.StringVar()
    custom = tk.StringVar()

    dynamic = tk.Frame(action_frame)
    dynamic.pack()

    def refresh(*_):
        for w in dynamic.winfo_children():
            w.destroy()

        if "Holding" in target_type.get():
            ttk.Label(dynamic, text="Runway").pack()
            ttk.Entry(dynamic, textvariable=runway).pack()
            ttk.Label(dynamic, text="Holding Point").pack()
            ttk.Entry(dynamic, textvariable=hold).pack()

        elif target_type.get() == "Gate":
            ttk.Label(dynamic, text="Gate").pack()
            ttk.Entry(dynamic, textvariable=gate).pack()

        elif target_type.get() == "Custom":
            ttk.Label(dynamic, text="Destination").pack()
            ttk.Entry(dynamic, textvariable=custom).pack()

    target_type.trace_add("write", refresh)

    def generate():
        cs = f"{callsign.get()}{flight.get()}"
        route = ", ".join(route_box.get(0, tk.END))

        if "Holding" in target_type.get():
            msg = f"{cs}, taxi to holding point {hold.get()}, hold short of runway {runway.get()} via {route}."
        elif target_type.get() == "Gate":
            msg = f"{cs}, taxi to gate {gate.get()} via {route}."
        elif target_type.get() == "Cargo Apron":
            msg = f"{cs}, taxi to the cargo apron via {route}."
        elif target_type.get() == "Fuel Stand":
            msg = f"{cs}, taxi to the fuel stand via {route}."
        else:
            msg = f"{cs}, taxi to {custom.get()} via {route}."

        pyperclip.copy(msg)
        show(menu_frame)

    tk.Button(action_frame, text="Generate & Copy", command=generate).pack(pady=10)
    tk.Button(action_frame, text="Back", command=lambda: show(menu_frame)).pack()
    show(action_frame)

# ================= GENERIC (RUNWAY-AWARE) =================

def open_generic(role, action):
    clear(action_frame)

    callsign = tk.StringVar()
    flight = tk.StringVar()
    runway = tk.StringVar()
    wind_dir = tk.StringVar(value=recent_wind["dir"])
    wind_spd = tk.StringVar(value=recent_wind["spd"])

    tk.Label(action_frame, text=action, font=("Arial", 15)).pack(pady=10)

    # Callsign
    ttk.Label(action_frame, text="Callsign").pack()
    ttk.Combobox(action_frame, values=CALLSIGNS, textvariable=callsign).pack()

    ttk.Label(action_frame, text="Flight Number").pack()
    ttk.Entry(action_frame, textvariable=flight).pack()

    # Runway (Tower only)
    if role == "Tower":
        ttk.Label(action_frame, text="Runway").pack()
        ttk.Combobox(
            action_frame,
            values=AIRPORTS[selected_airport.get()],
            textvariable=runway
        ).pack()

    # Wind (Takeoff / Landing only)
    if role == "Tower" and action in ["Cleared for Takeoff", "Cleared to Land"]:
        ttk.Label(action_frame, text="Wind Direction").pack()
        ttk.Entry(action_frame, textvariable=wind_dir).pack()

        ttk.Label(action_frame, text="Wind Speed (kt)").pack()
        ttk.Entry(action_frame, textvariable=wind_spd).pack()

    # Recent callsigns
    ttk.Label(action_frame, text="Recent Callsigns").pack(pady=6)
    cs_box = tk.Listbox(action_frame, height=5)
    cs_box.pack()

    for cs in recent_callsigns:
        cs_box.insert(tk.END, cs)

    def fill_recent(_):
        if cs_box.curselection():
            full = cs_box.get(cs_box.curselection())
            for c in CALLSIGNS:
                if full.startswith(c):
                    callsign.set(c)
                    flight.set(full[len(c):])
                    break

    cs_box.bind("<<ListboxSelect>>", fill_recent)

    def generate():
        full_cs = f"{callsign.get()}{flight.get()}"

        if full_cs and full_cs not in recent_callsigns:
            recent_callsigns.append(full_cs)
            if len(recent_callsigns) > MAX_RECENT:
                recent_callsigns.pop(0)

        # Save wind
        if role == "Tower" and action in ["Cleared for Takeoff", "Cleared to Land"]:
            recent_wind["dir"] = wind_dir.get()
            recent_wind["spd"] = wind_spd.get()

        # Message build
        if action == "Cleared for Takeoff":
            msg = (
                f"{full_cs}, cleared for takeoff Runway {runway.get()}, "
                f"wind {wind_dir.get()} at {wind_spd.get()} knots."
            )

        elif action == "Cleared to Land":
            msg = (
                f"{full_cs}, cleared to land Runway {runway.get()}, "
                f"wind {wind_dir.get()} at {wind_spd.get()} knots."
            )

        else:
            msg = f"{full_cs}, {action.lower()}."

        pyperclip.copy(msg)
        show(menu_frame)

    tk.Button(action_frame, text="Generate & Copy", command=generate).pack(pady=10)
    tk.Button(action_frame, text="Back", command=lambda: show(menu_frame)).pack()
    show(action_frame)


# ================= HELPERS =================

def clear(frame):
    for w in frame.winfo_children():
        w.destroy()

# ================= START =================

show(role_frame)
root.mainloop()
