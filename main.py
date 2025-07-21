from tkinter import *
from datetime import datetime
from add_event import create_event_window
from events_list import show_events_window

window = Tk()
window.title("Koledar")
window.config(background="#2a2a2a")

icon = PhotoImage(file='assets/logo.png')
window.iconphoto(True, icon)

window.geometry("390x480")
window.minsize(390, 480)
window.maxsize(390, 480)

main_frame = Frame(window, bg="#2a2a2a")
main_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

selected_day = StringVar()
action_button = None
selected_cell = None


current_month = datetime.now().month
current_year = datetime.now().year

timeLabel = Label(main_frame, font=("Arial", 40), bg="#2a2a2a", fg="white")
timeLabel.pack(pady=(10, 0))

dayLabel = Label(main_frame, font=("Arial", 16), bg="#2a2a2a", fg="white")
dayLabel.pack(pady=(0, 10))

def update():
    current_time = datetime.now().strftime('%H:%M:%S')
    timeLabel.config(text=current_time)
    current_day = datetime.now().strftime('%A, %B %d, %Y')
    dayLabel.config(text=current_day)
    window.after(1000, update)

update()

month_nav_frame = Frame(main_frame, bg="#2a2a2a")
month_nav_frame.pack(pady=(0, 10))

prev_button = Button(month_nav_frame, text="<", command=lambda: change_month(-1))
prev_button.pack(side=LEFT)

month_label = Label(month_nav_frame, font=("Arial", 14, "bold"), bg="#2a2a2a", fg="white", width=15, anchor="center")
month_label.pack(side=LEFT, padx=10)

def change_month(delta):
    global current_month, current_year
    current_month += delta
    if current_month < 1:
        current_month = 12
        current_year -= 1
    elif current_month > 12:
        current_month = 1
        current_year += 1
    draw_calendar()

next_button = Button(month_nav_frame, text=">", command=lambda: change_month(1))
next_button.pack(side=LEFT)

calendar_frame = Frame(main_frame, bg="#2a2a2a")
calendar_frame.pack()

dni = ["Pon", "Tor", "Sre", "Čet", "Pet", "Sob", "Ned"]
for i, dan in enumerate(dni):
    lbl = Label(calendar_frame, text=dan, font=("Arial", 10, "bold"), bg="#2a2a2a", fg="white", width=5)
    lbl.grid(row=0, column=i, padx=1, pady=3)

event_button_frame = Frame(main_frame, bg="#2a2a2a")
event_button_frame.pack(pady=(10, 0))

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_days_in_month(month, year):
    if month == 2:
        return 29 if is_leap_year(year) else 28
    if month in [4, 6, 9, 11]:
        return 30
    return 31

def get_first_weekday_of_month(year, month):
    return datetime(year, month, 1).isoweekday()

day_cells = {}

def draw_calendar():
    global day_cells, selected_cell
    today = datetime.now()

    month_names = ["Januar", "Februar", "Marec", "April", "Maj", "Junij",
                   "Julij", "Avgust", "September", "Oktober", "November", "December"]
    month_label.config(text=f"{month_names[current_month - 1]} {current_year}")

    for widget in calendar_frame.winfo_children()[7:]:
        widget.destroy()

    day_cells = {}
    days_in_month = get_days_in_month(current_month, current_year)
    first_weekday = get_first_weekday_of_month(current_year, current_month)

    prev_month = current_month - 1 if current_month > 1 else 12
    prev_year = current_year if current_month > 1 else current_year - 1
    prev_month_days = get_days_in_month(prev_month, prev_year)

    day_counter = 1
    next_month_day = 1
    filled_days = 0
    selected_cell = None

    for row in range(1, 7):
        for col in range(7):
            index = filled_days + 1
            if index < first_weekday:
                day = prev_month_days - (first_weekday - index - 1)
                bg = "#2a2a2a"
                fg = "#666666"
                text = str(day)
            elif day_counter <= days_in_month:
                is_today = (day_counter == today.day and current_month == today.month and current_year == today.year)
                bg = "#b8b8b8" if is_today else "white"
                fg = "black"
                text = str(day_counter)
                day_counter += 1
            else:
                bg = "#2a2a2a"
                fg = "#666666"
                text = str(next_month_day)
                next_month_day += 1

            cell = Label(calendar_frame, text=text, font=("Arial", 11), bg=bg, fg=fg,
                         width=5, height=2, relief="ridge", borderwidth=1)
            cell.grid(row=row, column=col, padx=1, pady=1)

            if fg == "black":
                cell.bind("<Button-1>", lambda e, d=text, c=cell: on_day_click(d, c))
                day_cells[text] = cell

            filled_days += 1

def on_day_click(day, cell):
    global action_button, selected_cell
    selected_day.set(f"{day}")

    if selected_cell and selected_cell != cell:
        today = datetime.now()
        if (int(selected_cell.cget("text")) == today.day and
            current_month == today.month and
            current_year == today.year):
            selected_cell.config(bg="#b8b8b8")
        else:
            selected_cell.config(bg="white")

    cell.config(bg="#e6e6e6")
    selected_cell = cell

    if action_button is None:
        button_container = Frame(event_button_frame, bg="#2a2a2a")
        button_container.pack()

        view_button = Button(button_container, text="Ogled dogodkov",
                             command=lambda: show_events_window(window),
                             bg="white", activebackground="#dcdcdc", font=("Arial", 10), width=15)
        view_button.pack(side=LEFT, padx=(0, 10))

        action_button = Button(button_container, text="Dodaj dogodek",
                               command=lambda: create_event_window(window, selected_day, current_month, current_year),
                               bg="white", activebackground="#ffc97d", font=("Arial", 10), width=15)
        action_button.pack(side=LEFT)
    else:
        action_button.config(command=lambda: create_event_window(window, selected_day, current_month, current_year))


if __name__ == "__main__":
    draw_calendar()
    window.mainloop()
