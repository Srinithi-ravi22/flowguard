# FlowGuard – Intelligent Workflow Monitoring & Protection

## Overview

FlowGuard is a Python-based workflow monitoring system designed to detect abnormal workflow behavior, identify repetitive execution patterns, calculate risk scores, and estimate resource wastage.

It helps identify potentially inefficient or uncontrolled automated workflows before they cause unnecessary execution and resource consumption.

## Key Features

- **Webhook-Based Event Monitoring:** Receives workflow events through a FastAPI endpoint.
- **Loop Detection:** Identifies repeating event patterns in workflow executions.
- **Risk Analysis:** Calculates risk scores and assigns severity levels (LOW, MEDIUM, HIGH, CRITICAL).
- **Execution-Level Monitoring:** Analyzes individual workflow executions separately.
- **Alert Management:** Creates, updates, and resolves workflow alerts.
- **Baseline Configuration:** Allows expected workflow behavior to be configured and updated.
- **Resource Waste Estimation:** Estimates excess executions, API calls, and execution time.
- **Protection Simulation:** Demonstrates how excess executions could be suppressed.
- **Recommendations:** Provides possible root causes and preventive suggestions.
- **Reusable Python Client:** Allows external Python applications to send events to FlowGuard.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- Requests

## Project Structure

```text
FlowGuard/
│
├── backend/
│   ├── api.py
│   ├── detector.py
│   ├── monitor.py
│   ├── risk_engine.py
│   ├── waste_calculator.py
│   ├── recommendations.py
│   ├── event_store.py
│   ├── alerts_store.py
│   ├── baseline_store.py
│   ├── events.json
│   ├── alerts.json
│   └── baselines.json
│
├── event_sender.py
├── flowguard_client.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FlowGuard
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the backend server

```bash
python -m uvicorn api:app --app-dir backend --reload
```

### 4. Open API documentation

Visit:

http://127.0.0.1:8000/docs

FastAPI Swagger UI provides an interface to explore and test the available endpoints.

### 5. Run the demo

Keep the backend server running. Open another terminal in the project directory and execute:

```bash
python event_sender.py
```

The demo sender randomly selects a predefined workflow scenario, generates an execution ID, and sends its events to FlowGuard for analysis.

## Supported Demo Workflows

- Email Automation
- Order Processing
- Payment Automation
- Inventory Automation
- Notification Automation
- User Registration

## Reusable Client

External Python applications can integrate with FlowGuard using `flowguard_client.py`.

Example:

```python
from flowguard_client import FlowGuardClient

client = FlowGuardClient(
    webhook_url="http://127.0.0.1:8000/api/webhook",
    workflow_name="My Workflow"
)

client.send_event("TASK_STARTED")
client.send_event("TASK_COMPLETED")
```

## Important Notes

- Risk scores are calculated using rule-based analysis.
- Resource wastage values are estimates based on supplied execution parameters.
- Protection is demonstrated through simulation; it does not directly block executions in external applications.
- External applications must send their workflow events to FlowGuard for monitoring.

## Project Goal

To make automated workflows more observable, identify abnormal execution patterns, and help reduce unnecessary resource consumption through intelligent monitoring and preventive insights.