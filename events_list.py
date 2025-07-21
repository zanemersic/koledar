import json
import os
from datetime import datetime
from tkinter import Toplevel, Frame, Label, Button, Scrollbar, Canvas, messagebox, RIGHT, Y, LEFT, BOTH

def show_events_window(parent):
    def load_events():
        file = "events.json"
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def delete_event(event_id):
        response = messagebox.askyesno("Potrditev", "Ali res želite izbrisati ta dogodek?")
        if not response:
            return

        all_events = load_events()
        updated_events = [e for e in all_events if e["id"] != event_id]
        with open("events.json", "w", encoding="utf-8") as f:
            json.dump(updated_events, f, indent=4, ensure_ascii=False)

        refresh_event_list()

    def refresh_event_list():
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        events = load_events()

        def parse_datetime(event):
            try:
                return datetime.strptime(f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M")
            except ValueError:
                return datetime.min

        events.sort(key=parse_datetime)

        if not events:
            Label(scroll_frame, text="Ni shranjenih dogodkov.", fg="white", bg="#2a2a2a", font=("Arial", 11)).pack(pady=10)
            return

        for event in events:
            frame = Frame(scroll_frame, bg="#3a3a3a", bd=1, relief="solid")
            frame.pack(fill="x", pady=5)

            Label(frame, text=f"{event['title']}", font=("Arial", 12, "bold"),
                  bg="#3a3a3a", fg="white", anchor="w").pack(fill="x", padx=10, pady=(5, 0))

            Label(frame, text=f"{event['date']} ob {event['time']}", font=("Arial", 10),
                  bg="#3a3a3a", fg="white", anchor="w").pack(fill="x", padx=10)

            Label(frame, text=event["description"], font=("Arial", 10),
                  bg="#3a3a3a", fg="white", anchor="w").pack(fill="x", padx=10, pady=(0, 5))

            Button(frame, text="Izbriši", bg="white", font=("Arial", 10),
                   command=lambda eid=event["id"]: delete_event(eid)).pack(pady=(0, 5))

    window = Toplevel(parent)
    window.title("Koledar : Ogled dogodkov")
    window.geometry("390x480")
    window.config(background="#2a2a2a")
    window.resizable(False, False)

    canvas = Canvas(window, bg="#2a2a2a", highlightthickness=0)
    scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg="#2a2a2a")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    refresh_event_list()
