
from collections import Counter
import json

# Import our own FlowGuard modules
from risk_engine import calculate_risk, calculate_risk_breakdown, get_severity
from waste_calculator import calculate_waste
from recommendations import (
    generate_root_cause,
    generate_recommendation
)


# =========================================
# 1. REPEATED PATTERN DETECTION
# =========================================

def detect_repeated_pattern(events):

    best_pattern = []
    best_repetitions = 1

    n = len(events)

    for pattern_length in range(1, n // 2 + 1):

        for start in range(n - pattern_length):

            pattern = events[start:start + pattern_length]

            repetitions = 1
            next_position = start + pattern_length

            while (
                next_position + pattern_length <= n
                and events[next_position:next_position + pattern_length]
                == pattern
            ):
                repetitions += 1
                next_position += pattern_length

            if repetitions >= 2:

                if (
                    repetitions > best_repetitions
                    or (
                        repetitions == best_repetitions
                        and pattern_length > len(best_pattern)
                    )
                ):
                    best_pattern = pattern
                    best_repetitions = repetitions

    return {
        "loop_detected": best_repetitions >= 2,
        "pattern": best_pattern,
        "repetitions": best_repetitions
    }


# =========================================
# 2. REPEATED EVENT ANALYSIS
# =========================================

def analyze_events(events):

    counts = Counter(events)

    return {
        event: count
        for event, count in counts.items()
        if count > 1
    }


# =========================================
# 3. COMPLETE WORKFLOW ANALYSIS
# =========================================

def analyze_workflow(data):

    events = data.get("events", [])

    executions = data.get("executions", 0)

    expected_executions = data.get(
        "expected_executions", 1
    )

    api_calls_per_execution = data.get(
        "api_calls_per_execution", 0
    )

    no_state_change_count = data.get(
        "no_state_change_count", 0
    )

    execution_time_ms = data.get(
        "execution_time_ms", 0
    )

    # Detect repeated patterns
    loop_result = detect_repeated_pattern(events)

    # Analyze repeated event names
    repeated_events = analyze_events(events)

    # Risk calculation
    risk_score = calculate_risk(
        loop_result["repetitions"],
        no_state_change_count,
        executions,
        loop_result["loop_detected"]
    )

    # Explainable risk breakdown
    risk_breakdown = calculate_risk_breakdown(
        loop_result["repetitions"],
        no_state_change_count,
        executions,
        loop_result["loop_detected"]
    )

    severity = get_severity(risk_score)

    # Waste calculation
    waste = calculate_waste(
        executions,
        expected_executions,
        api_calls_per_execution,
        execution_time_ms
    )

    # Explanation
    root_cause = generate_root_cause(
        loop_result,
        no_state_change_count,
        executions
    )

    # Prevention suggestion
    recommendation = generate_recommendation(
        loop_result["loop_detected"],
        no_state_change_count,
        executions
    )

    return {
        "workflow_name": data.get(
            "workflow_name", "Unknown Workflow"
        ),

        "loop_detected": loop_result["loop_detected"],

        "pattern": loop_result["pattern"],

        "repetitions": loop_result["repetitions"],

        "repeated_events": repeated_events,

        "risk_score": risk_score,

        "risk_breakdown": risk_breakdown,

        "severity": severity,

        "estimated_wasted_api_calls":
            waste["estimated_wasted_api_calls"],

        "estimated_wasted_time_seconds":
            waste["estimated_wasted_time_seconds"],

        "excess_executions":
            waste["excess_executions"],

        # NEW: Execution waste percentage
        "waste_percentage":
            waste["waste_percentage"],

        "root_cause": root_cause,

        "recommendation": recommendation
    }


# =========================================
# 4. PROTECTION SIMULATION
# =========================================

def simulate_protection(data, analysis):

    executions = data.get("executions", 0)

    expected_executions = data.get(
        "expected_executions", 1
    )

    api_calls_per_execution = data.get(
        "api_calls_per_execution", 0
    )

    execution_time_ms = data.get(
        "execution_time_ms", 0
    )

    prevented_executions = max(
        0,
        executions - expected_executions
    )

    api_calls_prevented = (
        prevented_executions * api_calls_per_execution
    )

    time_saved = (
        prevented_executions * execution_time_ms / 1000
    )

    return {
        "protection_enabled": True,

        "original_executions": executions,

        "allowed_executions": min(
            executions, expected_executions
        ),

        "prevented_executions": prevented_executions,

        "api_calls_prevented": api_calls_prevented,

        "execution_time_saved_seconds": round(
            time_saved, 2
        ),

        "original_risk_score": analysis["risk_score"],

        "message": (
            "Protection simulation complete. "
            "Excess executions were suppressed in this simulation."
        )
    }


# =========================================
# 5. DEMO INPUT
# =========================================

if __name__ == "__main__":

    demo_data = {
        "workflow_name": "Invoice Automation",

        "events": [
            "ORDER_UPDATED",
            "INVOICE_GENERATED",
            "ORDER_UPDATED",
            "INVOICE_GENERATED",
            "ORDER_UPDATED",
            "INVOICE_GENERATED"
        ],

        "executions": 84,

        "expected_executions": 1,

        "api_calls_per_execution": 3,

        "no_state_change_count": 74,

        "execution_time_ms": 800
    }

    analysis = analyze_workflow(demo_data)

    protection = simulate_protection(
        demo_data,
        analysis
    )

    print("\n========== FLOWGUARD ANALYSIS ==========\n")
    print(json.dumps(analysis, indent=4))

    print("\n========== PROTECTION SIMULATION ========\n")
    print(json.dumps(protection, indent=4))

    print("\n======================================")
