
import requests
from datetime import datetime, timezone


class FlowGuardClient:

    def __init__(self, webhook_url, workflow_name, source="external_application"):
        self.webhook_url = webhook_url
        self.workflow_name = workflow_name
        self.source = source

    def send_event(self, event_name, execution_id=None, details=None):

        payload = {
            "workflow_name": self.workflow_name,
            "event": event_name,
            "execution_id": execution_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": self.source,
            "details": details or {}
        }

        response = requests.post(
            self.webhook_url,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        return response.json()
