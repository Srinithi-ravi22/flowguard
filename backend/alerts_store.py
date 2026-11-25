
import json
import uuid
from pathlib import Path
from threading import Lock
from datetime import datetime, timezone

ALERTS_FILE = Path(__file__).parent / "alerts.json"

lock = Lock()


def get_all_alerts():
    with lock:
        if not ALERTS_FILE.exists():
            return []

        with open(ALERTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)


def save_or_update_alert(analysis):
    with lock:
        if ALERTS_FILE.exists():
            with open(ALERTS_FILE, "r", encoding="utf-8") as file:
                alerts = json.load(file)
        else:
            alerts = []

        workflow_name = analysis["workflow_name"]
        execution_id = analysis.get("execution_id")

        existing_alert = next(
            (
                alert for alert in alerts
                if alert["workflow_name"] == workflow_name
                and alert.get("execution_id") == execution_id
                and alert["status"] == "ACTIVE"
            ),
            None
        )

        alert_data = {
            "workflow_name": workflow_name,
            "execution_id": execution_id,
            "risk_score": analysis["risk_score"],
            "severity": analysis["severity"],
            "pattern": analysis["pattern"],
            "repetitions": analysis["repetitions"],
            "message": analysis["alert_message"],
            "last_detected": datetime.now(timezone.utc).isoformat(),
            "status": "ACTIVE"
        }

        if existing_alert:
            existing_alert.update(alert_data)
            alert_data = existing_alert
        else:
            alert_data["alert_id"] = str(uuid.uuid4())
            alert_data["created_at"] = datetime.now(timezone.utc).isoformat()
            alerts.append(alert_data)

        with open(ALERTS_FILE, "w", encoding="utf-8") as file:
            json.dump(alerts, file, indent=4)

        return alert_data


def resolve_active_alert(workflow_name, execution_id=None):
    with lock:
        if not ALERTS_FILE.exists():
            return None

        with open(ALERTS_FILE, "r", encoding="utf-8") as file:
            alerts = json.load(file)

        resolved_alert = None

        for alert in alerts:
            if (
                alert["workflow_name"] == workflow_name
                and alert.get("execution_id") == execution_id
                and alert["status"] == "ACTIVE"
            ):
                alert["status"] = "RESOLVED"
                alert["resolved_at"] = datetime.now(timezone.utc).isoformat()
                resolved_alert = alert

        with open(ALERTS_FILE, "w", encoding="utf-8") as file:
            json.dump(alerts, file, indent=4)

        return resolved_alert
