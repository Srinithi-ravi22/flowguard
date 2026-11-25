
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from datetime import datetime, timezone
from typing import Optional

from detector import analyze_workflow, simulate_protection

from event_store import (
    save_event,
    get_all_events,
    clear_events
)

from monitor import detect_loop, calculate_risk

from baseline_store import (
    get_baseline,
    get_all_baselines,
    save_baseline
)

from alerts_store import (
    save_or_update_alert,
    get_all_alerts,
    resolve_active_alert
)


app = FastAPI(title="FlowGuard API")


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Event input model
class FlowGuardEvent(BaseModel):
    workflow_name: str
    event: str
    execution_id: Optional[str] = None
    timestamp: Optional[str] = None
    source: Optional[str] = "unknown"
    details: dict = Field(default_factory=dict)


# Baseline input model
class BaselineConfig(BaseModel):
    expected_events: int = Field(ge=1)
    max_repetitions: int = Field(ge=1)
    allowed_retries: int = Field(ge=0)


# Manual workflow analysis input
class WorkflowInput(BaseModel):
    workflow_name: str = "Unknown Workflow"
    events: list[str] = Field(default_factory=list)
    executions: int = Field(ge=0)
    expected_executions: int = Field(default=1, ge=0)
    api_calls_per_execution: int = Field(default=0, ge=0)
    no_state_change_count: int = Field(default=0, ge=0)
    execution_time_ms: float = Field(default=0, ge=0)


# --------------------------------------------------
# EXECUTION-AWARE WORKFLOW ANALYSIS
# --------------------------------------------------

def analyze_workflow_events(workflow_name, execution_id=None):

    all_events = get_all_events()

    # Only analyze events belonging to this workflow
    # AND this particular execution.
    workflow_events = [
        event for event in all_events
        if (
            event["workflow_name"] == workflow_name
            and event.get("execution_id") == execution_id
        )
    ]

    # Detect repeating patterns within this execution
    analysis = detect_loop(workflow_events)

    # Retrieve workflow baseline
    baseline = get_baseline(workflow_name)

    # Default baseline when none exists
    effective_baseline = baseline or {
        "expected_events": 2,
        "max_repetitions": 1,
        "allowed_retries": 0
    }

    # Calculate risk using the existing risk engine
    risk = calculate_risk(
        analysis,
        effective_baseline
    )

    analysis.update(risk)

    # Calculate permitted and excess repetitions
    permitted_repetitions = (
        effective_baseline["max_repetitions"]
        + effective_baseline["allowed_retries"]
    )

    excess_repetitions = max(
        0,
        analysis["repetitions"] - permitted_repetitions
    )

    # Monitoring information
    analysis["baseline"] = effective_baseline

    analysis["observed_repetitions"] = (
        analysis["repetitions"]
    )

    analysis["permitted_repetitions"] = (
        permitted_repetitions
    )

    analysis["excess_repetitions"] = (
        excess_repetitions
    )

    analysis["workflow_name"] = workflow_name
    analysis["execution_id"] = execution_id

    # Alert message
    if analysis["alert"]:
        analysis["alert_message"] = (
            f"{analysis['severity']} RISK: Suspicious repetitive "
            f"activity detected in {workflow_name}"
        )
    else:
        analysis["alert_message"] = (
            f"No high-risk alert for {workflow_name}"
        )

    return analysis


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "FlowGuard API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# MANUAL WORKFLOW ANALYSIS
# --------------------------------------------------

@app.post("/api/analyze")
def analyze(data: WorkflowInput):

    workflow_data = data.model_dump()

    result = analyze_workflow(workflow_data)

    return result


# --------------------------------------------------
# PROTECTION SIMULATION
# --------------------------------------------------

@app.post("/api/protect")
def protect(data: WorkflowInput):

    workflow_data = data.model_dump()

    analysis = analyze_workflow(workflow_data)

    protection = simulate_protection(
        workflow_data,
        analysis
    )

    return {
        "analysis": analysis,
        "protection": protection
    }


# --------------------------------------------------
# WEBHOOK - RECEIVE EXTERNAL EVENTS
# --------------------------------------------------

@app.post("/api/webhook")
def receive_event(data: FlowGuardEvent):

    event_data = data.model_dump()

    if not event_data["timestamp"]:
        event_data["timestamp"] = (
            datetime.now(timezone.utc).isoformat()
        )

    # Save incoming event
    save_event(event_data)

    # Analyze only this execution
    analysis = analyze_workflow_events(
        data.workflow_name,
        data.execution_id
    )

    alert_record = None

    if analysis["alert"]:

        alert_record = save_or_update_alert(analysis)

    else:

        alert_record = resolve_active_alert(
            data.workflow_name,
            data.execution_id
        )

    return {
        "message": "Event received and analyzed",
        "event": event_data,
        "analysis": analysis,
        "alert_record": alert_record
    }


# --------------------------------------------------
# VIEW ALL EVENTS
# --------------------------------------------------

@app.get("/api/events")
def view_events():

    events = get_all_events()

    return {
        "total_events": len(events),
        "events": events
    }


# --------------------------------------------------
# CLEAR EVENTS
# --------------------------------------------------

@app.delete("/api/events")
def reset_events():

    clear_events()

    return {
        "message": "All events cleared successfully"
    }


# --------------------------------------------------
# MONITOR ALL WORKFLOWS AND EXECUTIONS
# --------------------------------------------------

@app.get("/api/monitor")
def monitor_all_workflows():

    all_events = get_all_events()

    # Group execution IDs by workflow
    executions = {}

    for event in all_events:

        workflow_name = event["workflow_name"]
        execution_id = event.get("execution_id")

        if workflow_name not in executions:
            executions[workflow_name] = set()

        executions[workflow_name].add(execution_id)

    results = []

    # Analyze each execution separately
    for workflow_name, execution_ids in executions.items():

        for execution_id in execution_ids:

            analysis = analyze_workflow_events(
                workflow_name,
                execution_id
            )

            results.append(analysis)

    return {
        "monitored_workflows": len(executions),
        "monitored_executions": len(results),
        "results": results
    }


# --------------------------------------------------
# ALERTS
# --------------------------------------------------

@app.get("/api/alerts")
def view_alerts():

    alerts = get_all_alerts()

    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }


# --------------------------------------------------
# BASELINE MANAGEMENT
# --------------------------------------------------

@app.get("/api/baselines")
def view_baselines():

    return get_all_baselines()


@app.get("/api/baselines/{workflow_name}")
def view_baseline(workflow_name: str):

    baseline = get_baseline(workflow_name)

    if baseline is None:
        return {
            "message": f"No baseline found for {workflow_name}"
        }

    return {
        "workflow_name": workflow_name,
        "baseline": baseline
    }


@app.put("/api/baselines/{workflow_name}")
def update_baseline(
    workflow_name: str,
    config: BaselineConfig
):

    baseline_data = config.model_dump()

    saved_baseline = save_baseline(
        workflow_name,
        baseline_data
    )

    return {
        "message": "Baseline updated successfully",
        "workflow_name": workflow_name,
        "baseline": saved_baseline
    }
