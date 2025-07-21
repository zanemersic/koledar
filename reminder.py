import time
import json
import os
from datetime import datetime
from plyer import notification

path = "events.json"
finished_events = set()

def load_events():
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def validate_events():
    events = load_events()
    date_now = datetime.now()
    current_time = date_now.strftime("%d-%m-%Y %H:%M:%S")

    for event in events:
        time_of_event = f"{event['date']} {event['time']}"

        if time_of_event == current_time and event["id"] not in finished_events:
            title = event.get("title", "Dogodek")
            description = event.get("description", "")

            notification.notify(
                title=f"Opomnik: {title}",
                message=description or f"Dogodek ob {event['time']}",
                timeout=10
            )

            finished_events.add(event["id"])

if __name__ == "__main__":
    while True:
        validate_events()
        time.sleep(1)
