
import requests
import time
import random
import uuid

WEBHOOK_URL = "http://127.0.0.1:8000/api/webhook"

SCENARIOS = [
    {
        "name": "Email Automation",
        "workflow": "Email Automation",
        "events": [
            "USER_REGISTERED",
            "WELCOME_EMAIL_SENT"
        ]
    },
    {
        "name": "Order Processing",
        "workflow": "Order Processing",
        "events": [
            "ORDER_PLACED",
            "PAYMENT_CONFIRMED",
            "ORDER_PACKED",
            "ORDER_SHIPPED"
        ]
    },
    {
        "name": "Payment Automation",
        "workflow": "Payment Automation",
        "events": [
            "PAYMENT_INITIATED",
            "PAYMENT_FAILED",
            "PAYMENT_RETRY",
            "PAYMENT_INITIATED",
            "PAYMENT_FAILED",
            "PAYMENT_RETRY",
            "PAYMENT_INITIATED",
            "PAYMENT_FAILED",
            "PAYMENT_RETRY",
            "PAYMENT_INITIATED",
            "PAYMENT_FAILED",
            "PAYMENT_RETRY"
        ]
    },
    {
        "name": "Inventory Automation",
        "workflow": "Inventory Automation",
        "events": [
            "STOCK_CHECKED",
            "STOCK_UPDATED",
            "STOCK_CHECKED",
            "STOCK_UPDATED",
            "STOCK_CHECKED",
            "STOCK_UPDATED"
        ]
    },
    {
        "name": "Notification Automation",
        "workflow": "Notification Automation",
        "events": [
            "NOTIFICATION_CREATED",
            "NOTIFICATION_SENT",
            "NOTIFICATION_CREATED",
            "NOTIFICATION_SENT",
            "NOTIFICATION_CREATED",
            "NOTIFICATION_SENT",
            "NOTIFICATION_CREATED",
            "NOTIFICATION_SENT",
            "NOTIFICATION_CREATED",
            "NOTIFICATION_SENT"
        ]
    },
    {
        "name": "User Registration",
        "workflow": "User Registration",
        "events": [
            "USER_REGISTERED",
            "WELCOME_EMAIL_SENT",
            "USER_REGISTERED",
            "WELCOME_EMAIL_SENT",
            "USER_REGISTERED",
            "WELCOME_EMAIL_SENT",
            "USER_REGISTERED",
            "WELCOME_EMAIL_SENT"
        ]
    }
]


def run_scenario():

    scenario = random.choice(SCENARIOS)

    execution_id = str(uuid.uuid4())

    print("\n" + "=" * 55)
    print("                 FLOWGUARD DEMO")
    print("=" * 55)

    print("Selected Workflow :", scenario["name"])
    print("Execution ID      :", execution_id)
    print("Total Events      :", len(scenario["events"]))

    print("-" * 55)
    print("Sending events...\n")

    final_analysis = None

    for index, event in enumerate(scenario["events"], start=1):

        payload = {
            "workflow_name": scenario["workflow"],
            "event": event,
            "execution_id": execution_id,
            "source": "FlowGuard Demo Application"
        }

        try:
            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            # Display the analysis calculated by the backend
            final_analysis = result.get("analysis", {})

            print(
                f"{index}. {event} | "
                f"Risk: {final_analysis.get('risk_score')} | "
                f"Severity: {final_analysis.get('severity')}"
            )

        except requests.exceptions.RequestException as error:
            print(f"\nError sending event {event}: {error}")
            return

        time.sleep(0.5)

    if not final_analysis:
        print("No analysis received from backend.")
        return

    print("\n" + "=" * 55)
    print("                FLOWGUARD ANALYSIS")
    print("=" * 55)

    print("Workflow       :", final_analysis.get("workflow_name"))
    print("Total Events   :", final_analysis.get("total_events"))
    print("Loop Detected  :", final_analysis.get("loop_detected"))
    print("Pattern        :", final_analysis.get("pattern"))
    print("Repetitions    :", final_analysis.get("repetitions"))
    print("Risk Score     :", final_analysis.get("risk_score"))
    print("Severity       :", final_analysis.get("severity"))
    print("Alert Generated:", final_analysis.get("alert"))

    print("\nAnalysis Message:")
    print(final_analysis.get("alert_message"))

    print("=" * 55)
    print("Demo completed!")


if __name__ == "__main__":
    run_scenario()
