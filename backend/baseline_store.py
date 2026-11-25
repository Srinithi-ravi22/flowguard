import json
from pathlib import Path
from threading import Lock

BASELINES_FILE = Path(__file__).parent / "baselines.json"
lock = Lock()


DEFAULT_BASELINES = {
    "Email Automation": {
        "expected_events": 2,
        "max_repetitions": 1,
        "allowed_retries": 0
    },
    "Payment Automation": {
        "expected_events": 3,
        "max_repetitions": 3,
        "allowed_retries": 2
    }
}


def get_all_baselines():
    with lock:
        if not BASELINES_FILE.exists():
            with open(BASELINES_FILE, "w", encoding="utf-8") as file:
                json.dump(DEFAULT_BASELINES, file, indent=4)

        with open(BASELINES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)


def get_baseline(workflow_name):
    baselines = get_all_baselines()
    return baselines.get(workflow_name)


def save_baseline(workflow_name, baseline_data):
    with lock:
        if BASELINES_FILE.exists():
            with open(BASELINES_FILE, "r", encoding="utf-8") as file:
                baselines = json.load(file)
        else:
            baselines = DEFAULT_BASELINES.copy()

        baselines[workflow_name] = baseline_data

        with open(BASELINES_FILE, "w", encoding="utf-8") as file:
            json.dump(baselines, file, indent=4)

        return baseline_data