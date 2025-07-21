import json
import os
import subprocess
import uuid
from tkinter import Toplevel, Label, Entry, Button, Frame, messagebox, IntVar, StringVar

months = [
    "Januar", "Februar", "Marec", "April", "Maj", "Junij",
    "Julij", "Avgust", "September", "Oktober", "November", "December"
]

def create_event_window(parent, selected_day, month, year):
    def save_event():
        name = event_name.get().strip()
        description = event_description.get().strip()
        hour = hour_var.get()
        minute = minute_var.get()
        seconds = 0

        if not name:
            messagebox.showwarning("Napaka", "Ime dogodka je obvezno.")
            return

        date = f"{int(day):02d}-{month:02d}-{year:04d}"
        time = f"{hour:02d}:{minute:02d}:{seconds:02d}"

        new_event = {
            "id": str(uuid.uuid4()),
            "title": name,
            "description": description,
            "date": date,
            "time": time
        }

        file = "events.json"
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                try:
                    events = json.load(f)
                except json.JSONDecodeError:
                    events = []
        else:
            events = []

        events.append(new_event)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Uspeh", "Dogodek uspešno shranjen.")
        new_window.destroy()
        try:
            subprocess.Popen(["python", "reminder.py"])
        except Exception as e:
            print(f"Napaka pri zagonu reminder.py: {e}")

    new_window = Toplevel(parent)
    new_window.title("Koledar : Dodajanje dogodka")
    new_window.geometry("390x480")
    new_window.config(background="#2a2a2a")
    new_window.resizable(False, False)

    content_frame = Frame(new_window, bg="#2a2a2a")
    content_frame.pack(expand=True, fill="both", padx=20, pady=20)

    month_name = months[month - 1]
    day = selected_day.get()

    title = Label(
        content_frame,
        text=f"Dodaj dogodek za {day}. {month_name} {year}",
        font=("Arial", 14, "bold"),
        bg="#2a2a2a", fg="white"
    )
    title.pack(pady=(0, 20))

    name_label = Label(content_frame, text="Ime dogodka", font=("Arial", 11), bg="#2a2a2a", fg="white")
    name_label.pack(anchor="w", pady=(0, 5))

    event_name = Entry(content_frame, font=("Arial", 11), relief="solid", bd=1)
    event_name.pack(fill="x", pady=(0, 15))

    description_label = Label(content_frame, text="Opis dogodka", font=("Arial", 11), bg="#2a2a2a", fg="white")
    description_label.pack(anchor="w", pady=(0, 5))

    event_description = Entry(content_frame, font=("Arial", 11), relief="solid", bd=1)
    event_description.pack(fill="x", pady=(0, 15))

    time_label = Label(content_frame, text="Izberi čas dogodka", font=("Arial", 11), bg="#2a2a2a", fg="white")
    time_label.pack(anchor="w", pady=(10, 5))

    hour_var = IntVar(value=12)
    minute_var = IntVar(value=00)

    time_frame = Frame(content_frame, bg="#2a2a2a")
    time_frame.pack(pady=(5, 5))

    formatted_time = StringVar()

    def update_time_label():
        formatted_time.set(f"{hour_var.get():02d}:{minute_var.get():02d}")

    def increment_hour():
        hour_var.set((hour_var.get() + 1) % 24)
        update_time_label()

    def decrement_hour():
        hour_var.set((hour_var.get() - 1) % 24)
        update_time_label()

    def increment_minute():
        minute_var.set((minute_var.get() + 1) % 60)
        update_time_label()

    def decrement_minute():
        minute_var.set((minute_var.get() - 1) % 60)
        update_time_label()

    update_time_label()

    Label(time_frame, textvariable=formatted_time, font=("Arial", 24, "bold"), fg="white", bg="#2a2a2a").grid(
        row=1, column=1, columnspan=3, pady=10
    )
    arrow_style = {"font": ("Arial", 16, "bold"), "bg": "white", "width": 2, "height": 1}

    Frame(time_frame, bg="#2a2a2a").grid(row=0, column=0)
    Button(time_frame, text="↑", command=increment_hour, **arrow_style).grid(row=0, column=1)
    Frame(time_frame, bg="#2a2a2a").grid(row=0, column=2)

    Button(time_frame, text="↑", command=increment_minute, **arrow_style).grid(row=0, column=3)
    Frame(time_frame, bg="#2a2a2a").grid(row=0, column=4)

    Button(time_frame, text="↓", command=decrement_hour, **arrow_style).grid(row=2, column=1)
    Button(time_frame, text="↓", command=decrement_minute, **arrow_style).grid(row=2, column=3)


    button = Button(content_frame, text="Shrani dogodek", font=("Arial", 11, "bold"),
                    bg="white", activebackground="#ffc97d", relief="raised", bd=2,
                    command=save_event)
    button.pack(ipadx=10, ipady=5)
