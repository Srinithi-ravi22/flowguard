
import json
from pathlib import Path
from threading import Lock

# Store events in a local JSON file
EVENTS_FILE = Path(__file__).parent / "events.json"

# Prevent simultaneous requests from writing at the same time
lock = Lock()


def save_event(event_data):
    with lock:
        if EVENTS_FILE.exists():
            with open(EVENTS_FILE, "r", encoding="utf-8") as file:
                events = json.load(file)
        else:
            events = []

        events.append(event_data)

        with open(EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump(events, file, indent=4)

    return event_data


def get_all_events():
    with lock:
        if not EVENTS_FILE.exists():
            return []

        with open(EVENTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)


def clear_events():
    with lock:
        with open(EVENTS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
